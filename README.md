# klimaschutzmonitor

## Quick overview

- We use poetry (so pyproject.toml lists the requirements, and poetry.lock the exact versions used to fulfill those requirements).
- To make sure that exactly those are installed we use a python virtual environment
- [black](https://github.com/psf/black) (for python) and [djlint](https://djlint.com/) (for django templates) are used to format code
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
- Install [Docker Desktop](https://www.docker.com/) or [Docker Engine and Docker Compose without Docker Desktop](https://docs.docker.com/engine/install/), if you prefer and are on Linux.

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
cp -r e2e_tests/database/test_database_uploads cpmonitor/images/uploads

# install css and javascript libraries
yarn install

# start the server
python manage.py runserver --settings=config.settings.local
```

The admin user for development is:

- user name: admin
- password: password

or create a new admin user with: `python manage.py createsuperuser --settings=config.settings.local` (Windows: prepend `winpty`)

The main app is called `cpmonitor` short for `climate protection monitor`. As that needs to be a python
package / module name it follows python style conventions of being short and all in one lowercase word.

## Testing

All tests are written in [pytest](https://docs.pytest.org/en/7.2.x/index.html).
End-to-end tests are written with the [playwright plugin of pytest](https://playwright.dev/python/docs/intro). <br>
The end-to-end tests use [pytest-django](https://pytest-django.readthedocs.io/en/latest/index.html) to set up a live server and
provide a test-database that is cleaned after each test. <br>
In order to automatically test the docker setup, there is also a smoke test in `e2e_tests/test_deployed` that requires starting the application with the local
configuration and creating the database with migrations applied and `e2e_tests/database/test_database.json` loaded.

#### Install playwright
The first time playwright is used, let it download the tools it needs with:

```shell
playwright install
```

#### Run the tests
```shell

# run all tests (exept the smoke test requiring a running server.)
pytest --ignore e2e_tests/test_deployed.py

# prepare external server and run smoke test against it (deletes DB):
rm db.sqlite3
poetry run python manage.py migrate --settings=config.settings.local
poetry run python manage.py loaddata --settings=config.settings.local e2e_tests/database/test_database.json
cp -r e2e_tests/database/test_database_uploads cpmonitor/images/uploads
docker compose up -d --build
pytest e2e_tests/test_deployed.py

# run a single test
pytest <path-to-test>

# run e2e test in headed mode
pytest --headed <path-to-e2e-test>
```

#### Test conventions
- New test files have to be named according to the convention: `*_test.py`.
- Test names should follow the convention: `test_should_do_x_when_given_y`.

### Fixtures for tests

From a local database filled with suitable data, generate a fixture named `example_fixture` with

```shell
python -Xutf8 manage.py dumpdata cpmonitor -e contenttypes --indent 2 --settings=config.settings.local > cpmonitor/fixtures/example_fixture.json
```

(The `-Xutf8` and `--indent 2` options ensure consistent and readable output on all platforms.)

This fixture may be loaded in a test with. (Similar in a pytest fixture.)

```python
@pytest.mark.django_db
def test_something(django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "example_fixture")
    # Test something here
```

This does not work when testing migrations, but there is a way: Use `read_fixture` in `cpmonitor/tests/migrations_test.py`.

## Manual tests with data from production

Occasionally, someone with access may provide a copy of the current production database. (See "Server Administration", below.)
This may be used as follows:

```sh
# Select the snapshot to use
SNAPSHOT_NAME=prod_database_<some date found in e2e_tests/database/>

# Remove previous data
rm db.sqlite3
rm -r cpmonitor/images/uploads

# Create DB
python manage.py migrate --settings=config.settings.local

# Optionally migrate back to suitable version (see the .README file corresponding to the snapshot you're about to load):
python manage.py migrate cpmonitor <some-earlier-migration> --settings=config.settings.local
python manage.py loaddata --settings=config.settings.local e2e_tests/database/${SNAPSHOT_NAME}.json
cp -r e2e_tests/database/${SNAPSHOT_NAME}_uploads cpmonitor/images/uploads
```

If snapshot you want to use is based on an older model version, migrations have to be applied and are tested:

```sh
python manage.py migrate --settings=config.settings.local
```

The E2E tests will most likely fail, since they are based on another DB dump, e.g. with other password settings.
But manual tests with the dev server or container-based should be possible and images should be visible:

```sh
python manage.py runserver --settings=config.settings.local
#or
docker compose --env-file .env.local up --detach --build
```

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

```shell
python manage.py makemigrations --settings=config.settings.local
```

The migration might have to be improved, e.g. by using `migrations.RunPython`.

Afterwards the test database has to be updated as well. Use the dumpdata command to generate a test database from the
currently running database:

```shell
python -Xutf8 manage.py dumpdata -e contenttypes --indent 2 --settings=config.settings.local > e2e_tests/database/test_database.json
```

Cheat-sheet to make sure the correct data is dumped:

```shell
git checkout right-before-model-change
rm db.sqlite3
python manage.py migrate --settings=config.settings.local
python manage.py loaddata --settings=config.settings.local e2e_tests/database/test_database.json
cp -r e2e_tests/database/test_database_uploads cpmonitor/images/uploads
git checkout after-model-change-including-migration
python manage.py migrate --settings=config.settings.local
python -Xutf8 manage.py dumpdata -e contenttypes --indent 2 --settings=config.settings.local > e2e_tests/database/test_database.json
# Only if additional images were uploaded:
cp -r cpmonitor/images/uploads e2e_tests/database/test_database_uploads
```

Check the diff of `e2e_tests/database/test_database.json` for any unexpected parts and adjust as necessary.

## When pre-commit hooks make trouble

E.g. the hook `check-untracked-migrations` is known to make trouble with detachted HEAD, e.g. during a rebase. Then it can be skipped:

```shell
SKIP=check-untracked-migrations git commit
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
docker compose build
```

### Deployment including nginx

To run both containers together, run the following command in the repository root directory (the app container will be built automatically if necessary):

```shell
docker compose up --detach
```

This will start both the Django app and the nginx containers *in the background*. The website can then be reached at <https://localhost>.
You'll have to tell your browser to make an exception for the [self-signed certificate](ssl_certificates_localhost) we use when running locally, or import it into your browser.

To stop the containers from running in the background, run:

```shell
docker compose down --volumes
```

The `--volumes` flag is important to make sure that at the next start, the latest static resources from the app container are served instead of potentially outdated files from the previous run cached by Docker.

## Set / change temporary password protection

The user / password for the development phase is stored in `config/nginx/htpasswd`. A new user / password may be set with

```shell
htpasswd -c config/nginx/htpasswd <username>
```

The `htpasswd` tool might have to be installed before, with (on Linux)

```shell
sudo apt install apache2-utils
```

## Server administration

### SSH access

Team members with their SSH keys installed on the server can add this to their `~/.ssh/config` file:

```.ssh/config
Host lzm
    HostName monitoring.localzero.net
    User monitoring
    IdentityFile ~/.ssh/<private_key_file>
```

This enables easy login:

```sh
ssh lzm
```

### Retrieve current DB from server

Replace your local DB with the current DB from the server with:

```sh
rm db.sqlite3
scp lzm:testing/db/db.sqlite3 .
rm -r cpmonitor/images/uploads
scp -r lzm:testing/cpmonitor/images/uploads cpmonitor/images/
```

To find out, on which migration version this database is based use:

```sh
ssh -tt lzm docker exec -it djangoapp-testing python manage.py showmigrations --settings=config.settings.container
# or
ssh -tt lzm docker exec -it djangoapp-production python manage.py showmigrations --settings=config.settings.container
```

Possibly migrate, test the data, and check that the size is reasonable. Then make it available to others with:

```sh
SNAPSHOT_NAME=prod_database_$(date -u +"%FT%H%M%SZ")
python -Xutf8 manage.py dumpdata -e contenttypes --indent 2 --settings=config.settings.local > e2e_tests/database/${SNAPSHOT_NAME}.json
cp -r cpmonitor/images/uploads e2e_tests/database/${SNAPSHOT_NAME}_uploads
echo "Some useful information, e.g. the migration state of the snapshot" > e2e_tests/database/${SNAPSHOT_NAME}.README
du -hs e2e_tests/database/${SNAPSHOT_NAME}*
```

Commit the result.

### Deploying a new version

1. Checkout the commit you want to deploy (usually the latest commit of main).
2. Tag that revision with

    ```sh
    DATESTR=$(date +%Y-%b-%d) && echo ${DATESTR}
    git tag -a deploy-prod-${DATESTR} -m "Deployment to production" && git push origin deploy-prod-${DATESTR}
    # and / or
    git tag -a deploy-test-${DATESTR} -m "Deployment to test" && git push origin deploy-test-${DATESTR}
    ```

3. Build the image for the Django app: `docker compose build`
4. Export the image: `docker save cpmonitor -o img.tar`
5. Copy the image and the compose file to the server: `scp -C img.tar docker-compose.yml monitoring@monitoring.localzero.net:/tmp/`
6. Login to the server: `ssh monitoring@monitoring.localzero.net`
7. Import the image into Docker on the server: `docker load -i /tmp/img.tar` (Docker should print "Loading layer".)
8. Tag the image with the current date in case we want to roll back:

    ```sh
    DATESTR=$(date +%Y-%b-%d) && echo ${DATESTR}
    docker tag cpmonitor:latest cpmonitor:${DATESTR}
    ```

9. Stop the server, apply the migrations, start the server:

    ```sh
    cd ~/<testing|production>/
    docker-compose down --volumes
    # backup the db
    cp -v db/db.sqlite3 /data/LocalZero/DB_BACKUPS/<testing|production>/db.sqlite3.${DATESTR}
    cp -vr cpmonitor/images/uploads /data/LocalZero/DB_BACKUPS/testing/uploads.${DATESTR}
    # apply migrations using a temporary container
    docker run --user=1007:1007 --rm -it -v $(pwd)/db:/db cpmonitor:latest sh
    DJANGO_SECRET_KEY=whatever DJANGO_CSRF_TRUSTED_ORIGINS=https://whatever DJANGO_DEBUG=False python manage.py migrate --settings=config.settings.container
    # exit and stop the temporary container
    exit
    # use the latest docker-compose.yml to start the app using the new image
    mv docker-compose.yml docker-compose.yml.bak && cp /tmp/docker-compose.yml .
    docker-compose up --detach
    ```

### Database Client
In order to view, manipulate and export the database in any of the environments (local, testing, production), the database webclient
[Cloudbeaver](https://github.com/dbeaver/cloudbeaver) is started automatically together with the application.

The client can be accessed at http://localhost/dbeaver (or http://monitoring-test.localzero.net/dbeaver, http://monitoring.localzero.net/dbeaver depending on
the environment) and the credentials can be found in the .env.local file. For testing and production, the credentials should be
configured in the respective .env files on the server.
