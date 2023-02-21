# klimaschutzmonitor

## Quick overview

- We use poetry (so pyproject.toml lists the requirements, and poetry.lock the exact versions used to fulfill those requirements).
- To make sure that exactly those are installed we use a python virtual environment
- black is used to format the code
- a pre-commit hook is used to keep commits clean
- We use pyright to get a little bit of type checking. Currently this is just in basic mode and without any special handling for the django ORM. I expect both things to potentially need tweaking (for example: <https://github.com/sbdchd/django-types> looks potentially useful).
- [Yarn](https://classic.yarnpkg.com/en/) is used to manage node dependencies that are needed to include
  [Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/)

## How to install the dev environment

- Install git as described here: <https://git-scm.com/downloads>.
- Windows: git includes a bash shell. Use it for the following commands.
- Windows: Settings -> Apps -> Apps and Features -> “manage app execution aliases” / "Aliase für die App-Ausführung": Deactivate for `python.exe` and `python3.exe`.
- Install python version 3.10 or greater. Linux: `sudo apt install python3`, Windows via <https://pyenv-win.github.io/pyenv-win/>.
- If not present, install python venv. Linux: `sudo apt install python3-venv` (the version needs to match the python version).
- Install poetry with `curl -sSL https://install.python-poetry.org | python3 -` (See <https://python-poetry.org/docs/>.)
- Windows: Add the shown path in the `PATH` variable. (Search fpr "env" in Windows settings.)
- Install `sudo apt install python-is-python3` so that poetry can run python3 with the python command.
- Install Yarn version 3 as described here: <https://yarnpkg.com/getting-started/install>.

The above steps are needed only once per machine.

Then run the following commands:

```shell
git clone https://github.com/GermanZero-de/klimaschutzmonitor.git
cd klimaschutzmonitor # Or `code klimaschutzmonitor` to open it with vscode.
python -m venv .venv
poetry shell
poetry install --sync
pre-commit install
```

This will

- clone this repository,
- create a python virtual environment in the sub-directory `.venv` of the cloned repository,
- install all the dependencies of the project as specified in `pyproject.toml` and `poetry.lock` into this virtual environment, and
- install a pre-commit hook in the cloned repository. (Will be run before each commit and check the code.)

Whenever you work with the project, call "`poetry shell`" first. Windows only: Do this within the WSL shell.
In this shell python points to the python virtual environment in `.venv`.

Whenever dependencies changed, call "`poetry install --sync`" first.

Otherwise, these commands need only be repeated when a new clone is created.

## Tips for vscode

After cloning the repository, open the new directory with vscode.

Windows: As terminal choose "Git Bash".

Recommended extensions should be offered. If not, got to the "Extensions" side-bar and enter `@recommended`. Then select "Install Workspace Recommended Extensions".

## How to run the development server

We roughly follow some of the project layout / config layout ideas of the Two Scoops of Django book (<https://www.feldroy.com/books/two-scoops-of-django-3-x>).

So the configuration lives in `config/settings/<what>.py`. Most importantly that means when testing
locally you want to do this:

```shell
# (inside your poetry shell)

# prepare database
python manage.py migrate --settings=config.settings.local

# (optional) install example data
python manage.py loaddata --settings=config.settings.local e2e_tests/database/test_database.json

# install css and javascript libraries
yarn install

# start the server
python manage.py runserver --settings=config.settings.local
```
The admin user for development is:
* user name: admin
* password: password

or create a new admin user with: `python manage.py createsuperuser --settings=config.settings.local` (Windows: prepend `winpty`)

The main app is called `cpmonitor` short for `climate protection monitor`. As that needs to be a python
package / module name it follows python style conventions of being short and all in one lowercase word.

## Testing
All tests are written in [pytest](https://docs.pytest.org/en/7.2.x/index.html).
End-to-end tests are written with the [playwright plugin of pytest](https://playwright.dev/python/docs/intro).
To provide a test-database for some tests we use [pytest-django](https://pytest-django.readthedocs.io/en/latest/index.html)

*Start the dev server in the background*, then execute tests with

```shell
# run all tests
pytest

# run a single test
pytest <path-to-test>

# run e2e test in headed mode
pytest --headed <path-to-e2e-test>
```

- New test files have to be named according to the convention: `*_test.py`.
- Test names should follow the convention: `test_should_do_x_when_given_y`.

## Styling

We use [Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/) as a css framework.
Custom scss can be written in [main.scss](cpmonitor/static/css/main.scss). Whenever this file has changed it has to be compiled with sass

```shell
yarn run compile:css
```

to generate a static css file that can be used in base.html.

To save this manual step, you can also run

```shell
yarn run compile:css:watch

# or on WSL2 if the project is on the Windows file system (eats CPU...):
yarn run compile:css:poll
```

in the background to keep compiling SCSS to CSS automatically upon changing the SCSS file.

To use the javascript from Bootstrap the relevant dependencies need to be installed in the node_modules folder. Run

```shell
yarn install
```

to do that.

## Changing the database model
When the database model in models.py is changed a new migration has to be created specifying how to change to the new
database format. This can be done by
```
python manage.py makemigrations --settings=config.settings.local
```

Afterwards the test database has to be updated as well. Use the dumpdata command to generate a test database from the
currently running database:
```
python manage.py dumpdata --settings=config.settings.local > e2e_tests/database/test_database.json
```

## Containerization and Deployment

The application is deployed to the server as a pair of Docker containers:

- container 1 runs the gunicorn webserver to host the django app itself,
- container 2 runs nginx, a proxy that hosts the static files while providing stability and security.

Only the port of nginx is exposed, which will forward requests to the django app or provide any requested static files directly.

### Building the Django app Docker image and running the container

The Dockerfile for the django app is based on the following resources:

- [DigitalOcean blog post](https://www.digitalocean.com/community/tutorials/how-to-build-a-django-and-gunicorn-application-with-docker)
- [Stackoverflow answer](https://stackoverflow.com/a/57886655)
- [Sample Repo](https://github.com/mgnisia/Boilerplate-Docker-Django-Gunicorn-Nginx)

It uses a multi-stage build to prevent shipping unnecessary files which would increase image size and attack surface.

To build the image, run the following command in the repository root directory (containing the Dockerfile):

```shell
docker build . -t cpmonitor
```

**Important:** Since static files are served by a separate nginx container, static files will be missing when you run the app container on its own. To run both the app and nginx, see the section [Deployment including nginx](#deployment-including-nginx).

To run just the app container, run (replacing directory of `db.sqlite3` and SECRET_KEY placeholders):

```shell
docker run --rm -it -p 8000:8000 -v <absolute path of directory containing db.sqlite3>:/db -e SECRET_KEY=<...> cpmonitor
```

By default, the container will run the app using the production configuration.
To use the local configuration, run:

```shell
docker run --rm -it -p 8000:8000 -e DJANGO_SETTINGS_MODULE=config.settings.local-container -v <absolute path of directory containing db.sqlite3>:/db cpmonitor
```

Instead of passing the absolute path to this repo, you may instead use

- in a Linux shell:

    ```shell
    -v "$PWD":/db
    ```

- in Powershell:

    ```powershell
    -v ${pwd}:db
    ```

- in a WSL Linux shell, if you decided to store your projects outside the WSL file system (otherwise see above):

    ```shell
    -v "${PWD/\/mnt/}":/db
    ```

### Deployment including nginx

To run both containers together, run the following command in the repository root directory (the app container will be built automatically if necessary):

```shell
# using production config
docker compose --env-file .env.production up --detach
```

```shell
# using local config
docker compose --env-file .env.local up --detach
```

This will start both the Django app and the nginx containers *in the background*. The website can then be reached at <http://localhost:80>.

To stop the containers from running in the background, run:

```shell
# using production config
docker compose --env-file .env.local down --volumes
```

```shell
# using local config
docker compose --env-file .env.local down --volumes
```

The `--volumes` flag is important to make sure that at the next start, the latest static resources from the app container are served instead of potentially outdated files from the previous run cached by Docker.
