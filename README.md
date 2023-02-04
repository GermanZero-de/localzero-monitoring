# klimaschutzmonitor

## Dev notes

You need python 3.10 or greater!

Quick overview:
	- We use poetry (so pyproject.toml lists the requirements, and poetry.lock the exact versions used to fulfill those requirements).
	- To make sure that exactly those are installed we use a python virtual environment
	- black is used to format the code
	- a pre-commit hook is used to keep commits clean

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

We roughly follow some of the project layout / config layout ideas of the Two Scoops of Django book.

So the configuration lives in `config/settings/<what>.py`.  Most importantly that means when testing
locally you want to do this:

```shell
# (inside your poetry shell)
python manage.py runserver --settings=config.settings.local
```

The main app is called `cpmonitor` short for `climate projection monitor`. As that needs to be a python
package / module name it follows python style conventions of being short and all in one lowercase word.
