# klimaschutzmonitor

## Dev notes

Quick overview:

- We use poetry (so pyproject.toml lists the requirements, and poetry.lock the exact versions used to fulfill those requirements).
- To make sure that exactly those are installed we use a python virtual environment
- black is used to format the code
- a pre-commit hook is used to keep commits clean
- We use pyright to get a little bit of type checking. Currently this is just in basic mode and without any special handling for the django ORM. I expect both things to potentially need tweaking (for example: https://github.com/sbdchd/django-types looks potentially useful).

### How to install the dev environment

You need python 3.10 or greater already installed! These notes are from a Mac user. So linux
folks should be happy. Windows users might need to do some adjusting but in principle all the
tooling is available for Windows users as well (I just haven't tested this).

```shell
# in the checkout of the repository
# Create a python virtual environment (so that exactly the libraries we specify in the poetry file will be available)
python3 -m venv .venv
# Start the poetry shell (this is a shell where python points to the venv python)
poetry shell
# Make sure everything is installed as per the poetry.lock file
poetry install --sync
# Make sure the pre-commit hooks are installed in the git repo
 ./.venv/bin/pre-commit install
```

On Windows, poetry and venv somehow do not work well together. Do this in a fresh check-out, instead:

```shell
# If not already installed globally, install poetry:
pip install poetry
# Make sure everything is installed as per the poetry.lock file. This creates a virtual environment in a user directory.
python -m poetry install --sync
# Start a poetry shell in that environment. (Has to be done each time.)
python -m poetry shell
# Make sure the pre-commit hooks are installed in the git repo.
pre-commit install
```

### How to run the development server

We roughly follow some of the project layout / config layout ideas of the Two Scoops of Django book.

So the configuration lives in `config/settings/<what>.py`. Most importantly that means when testing
locally you want to do this:

```shell
# (inside your poetry shell)

#prepare database
python manage.py makemigrations --settings=config.settings.local
python manage.py migrate --settings=config.settings.local

#generate user for admin UI
python manage.py createsuperuser --settings=config.settings.local

#start the server
python manage.py runserver --settings=config.settings.local
```

The main app is called `cpmonitor` short for `climate protection monitor`. As that needs to be a python
package / module name it follows python style conventions of being short and all in one lowercase word.
