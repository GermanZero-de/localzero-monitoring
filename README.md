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
- Install node.js from <https://nodejs.org/en/download>.
- Install [Docker Desktop](https://www.docker.com/) or [Docker Engine and Docker Compose without Docker Desktop](https://docs.docker.com/engine/install/), if you prefer and are on Linux/macOS.

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
cp -r e2e_tests/database/test_database_uploads/. cpmonitor/images/uploads

# install css and javascript libraries
yarn install

# start the server
python manage.py runserver --settings=config.settings.local
```

Whenever you have problems make sure that you have activated the virtual environment correctly. You may have to
deactivate it with "`deactivate`" and activate it with "`source .venv/bin/activate`" (Windows "`.venv/bin/activate.bat`").

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
rm db/db.sqlite3
poetry run python manage.py migrate --settings=config.settings.local
poetry run python manage.py loaddata --settings=config.settings.local e2e_tests/database/test_database.json
cp -r e2e_tests/database/test_database_uploads/. cpmonitor/images/uploads
docker compose up -d --build
docker compose -f docker/reverseproxy/docker-compose.yml up -d --build
pytest e2e_tests/test_deployed.py
docker compose -f docker/reverseproxy/docker-compose.yml down --volumes
docker compose down --volumes

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
python -Xutf8 manage.py dumpdata -e contenttypes -e auth.Permission -e admin.LogEntry -e sessions --indent 2 --settings=config.settings.local > cpmonitor/fixtures/example_fixture.json
```

(The `-Xutf8` and `--indent 2` options ensure consistent and readable output on all platforms.)

The arguments `-e contenttypes -e auth.Permission -e admin.LogEntry -e sessions` exclude tables which are pre-filled
by django or during usage by django and whose content may change depending on the models in the project. If they are
included, everything works fine at first, since loaddata will silently accept data already there. However, as soon as
the data to load clashes with existing content, it will fail. `-e admin.LogEntry` excludes references to content types
which may otherwise be inconsistent.`-e sessions` excludes unneeded data which otherwise would clog the JSON file.

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
rm db/db.sqlite3
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
python -Xutf8 manage.py dumpdata -e contenttypes -e auth.Permission -e admin.LogEntry -e sessions --indent 2 --settings=config.settings.local > e2e_tests/database/test_database.json
```

Cheat-sheet to make sure the correct data is dumped:

```shell
git checkout right-before-model-change
rm db/db.sqlite3
python manage.py migrate --settings=config.settings.local
python manage.py loaddata --settings=config.settings.local e2e_tests/database/test_database.json
cp -r e2e_tests/database/test_database_uploads/. cpmonitor/images/uploads
git checkout after-model-change-including-migration
python manage.py migrate --settings=config.settings.local
python -Xutf8 manage.py dumpdata -e contenttypes -e auth.Permission -e admin.LogEntry -e sessions --indent 2 --settings=config.settings.local > e2e_tests/database/test_database.json
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

```mermaid
flowchart TB
    user-device([visitor's device])-- visit site -->reverse-proxy
    subgraph localzero-monitoring-vm
        subgraph testing
            nginx-testing-- forward -->djangoapp-testing
            nginx-testing-- forward -->dbeaver-testing
            dbeaver-testing
        end
        subgraph production
            nginx-production-- forward -->djangoapp-production
            nginx-production-- forward -->dbeaver-production
            dbeaver-production
        end
        subgraph exposed [exposed to web]
            reverse-proxy-- forward if HOST==monitoring-test.localzero.net -->nginx-testing
            reverse-proxy-- forward if HOST==monitoring.localzero.net -->nginx-production
            acme.sh-. configure updated certs .->reverse-proxy
        end
    end
```

The application is deployed to the server in the form of three Docker compositions:
- reverse-proxy
- testing environment
- production environment

Each environment consists of:
- the "djangoapp" container that run the gunicorn webserver to host the django app itself,
- its own nginx (a proxy that hosts the static files while providing stability and security),
- a server for the database web client (DBeaver),

Outside the environments and exposed to the web, there's a third "reverse-proxy" composition containing:
- acme.sh, which handles SSL certificate renewal ([see further down](#tls-certificate-and-renewal)),
- the top-level reverse proxy nginx, which forwards requests to the environments based on the HOST header, or to acme.sh.

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

#### Issues when building the Docker image on Apple CPU Macs (M1, M2)

You might run into errors building the Docker image on a Mac, getting messages like `No working compiler found` and `Building wheel for cffi (setup.py): finished with status 'error'`.

This is usually caused by certain Python packages not being available prebuilt for download for arm64-based macOS, because the macOS version gets encoded into package names on pypi. This leads to packages not being found after macOS updates until the package authors update their files.

A workaround is to add `--platform linux/amd64` to the failing Docker command to simulate an amd64 architecture, so that generic linux packages are downloaded instead of the Apple CPU specific ones.

See also [#45](https://github.com/GermanZero-de/klimaschutzmonitor/issues/45).

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
rm db/db.sqlite3
scp lzm:testing/db/db.sqlite3 db/
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
python -Xutf8 manage.py dumpdata -e contenttypes -e auth.Permission -e admin.LogEntry -e sessions --indent 2 --settings=config.settings.local > e2e_tests/database/${SNAPSHOT_NAME}.json
cp -r cpmonitor/images/uploads e2e_tests/database/${SNAPSHOT_NAME}_uploads
echo "Some useful information, e.g. the migration state of the snapshot" > e2e_tests/database/${SNAPSHOT_NAME}.README
du -hs e2e_tests/database/${SNAPSHOT_NAME}*
```

Commit the result.

### Deploying the reverse proxy initially

```sh
scp -C -r docker/reverseproxy/conf.d/ docker/reverseproxy/docker-compose.yml docker/reverseproxy/.env.server monitoring@monitoring.localzero.net:/tmp/reverseproxy

# Run the remaining commands on the server:

cd ~/reverseproxy
cp -r /tmp/reverseproxy .
mv .env.server .env

docker compose up -d
```

### Deploying a new version

Requirement: SSH access to the server.

Run [.github/workflows/deploy.sh](.github/workflows/deploy.sh) and provide the environment to deploy to as an argument:

```shell
./deploy.sh testing
```

Optionally, you can specify a suffix for the tags that will be created, e.g. to differentiate multiple deployments on the same day:

```shell
./deploy.sh testing hotfix-for-issue-123
```

View the script to see the exact steps that are executed.

### Database Client
In order to view, manipulate and export the database in any of the environments (local, testing, production), the database webclient
[Cloudbeaver](https://github.com/dbeaver/cloudbeaver) is started automatically together with the application.

The client can be accessed at http://localhost/dbeaver (or http://monitoring-test.localzero.net/dbeaver, http://monitoring.localzero.net/dbeaver depending on
the environment) and the credentials can be found in the .env.local file. For testing and production, the credentials should be
configured in the respective .env files on the server.

### TLS Certificate and Renewal
#### Overview
We currently use a single TLS certificate for both monitoring.localzero.org and monitoring-test.localzero.org. The certificate is issued by letsencrypt.org and requesting and renewal is performed using [acme.sh](https://github.com/acmesh-official/acme.sh), which runs in a container. This solution allows us to have almost all necessary code and config in the repo instead of only on the server.

#### Initial Issuance
The initial certificate was issued using the following command:
```sh
docker exec acme-sh  --issue -d monitoring-test.localzero.net  -d monitoring.localzero.net --standalone --server https://acme-v02.api.letsencrypt.org/directory --fullchain-file /acme.sh/fullchain.cer --key-file /acme.sh/ssl-cert.key
```

#### Renewal
Renewal is performed automatically by acme.sh's internal cron job, which...
- checks if a renewal is necessary, and if so:
- requests a new certificate from letsencrypt,
- performs the challenge-response-mechanism to verify ownership of the domain
- and exports the full certificate chain and key to where nginx can find it.

A reload of the nginx config is independently triggered every four hours by our own cron job which can be found in [crontab](crontab) or by executing the following on the server:
```sh
crontab -l
```
This job runs [a script](reload-cert.sh) which applies the latest certificate that acme.sh has produced. This means there can be some delay between renewal and application of the certificate, but since acme.sh performs renewal a few days before expiry, there should be enough time for nginx to reload the certificate.

#### acme-sh Configuration and Debugging

The configuration used by acme-sh's cronjob (not our nginx reload cronjob!), e.g. renewal interval, can be changed in `reverseproxy/ssl_certificates/monitoring-test.localzero.net_ecc/`` on the server.

The following commands might be executed on the server to debug and test the acme-sh configuration:
```shell
# view certificate creation date and next renew date
docker exec acme-sh --list

# tell acme-sh to run its cronjob now, using letsencrypt's test environment (to bypass rate limiting)
docker exec acme-sh --cron --staging

# tell acme-sh to run its cronjob now, using letsencrypt's PROD environment (affected by rate limiting - 5 certs every couple weeks...)
docker exec acme-sh --cron

# force a renewal via letsencrypt's PROD environment, even if renewal time hasn't been reached yet
docker exec acme-sh --cron --force

# change mail address that will receive expiry warnings (only one address supported as of acme.sh v3.0.6)
docker exec acme-sh --update-account --accountemail '<the-new-address@somewhere.net>' --debug 2 --server https://acme-v02.api.letsencrypt.org/directory
```

#### TLS Certificates and Running Locally
When running locally, we instead use a [certificate created for localhost](ssl_certificates_localhost). Since ownership of localhost cannot be certified, this is a single self-signed certificate instead of a full chain signed by a CA like on the server, and an exception must be added to your browser to trust it.
