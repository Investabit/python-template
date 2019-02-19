# README


## Setup.py

Start by updating the setup.py for your project. The variables to change for your project are specified at the top, such as `NAME`, it is recommended to leave the `VERSION = None` and have it specified in your `__version__.py` file.

Generally only `Python >= 3.6.0` should be used for any new projects, but if you must support older versions of Python then `Python >= 3.5.0` will also be supported.


## Requirements Files

Review and specify your requirements files, if you are using any of the same packages you should at least use the versions provided or newer, as many of them have been updated and are known to work well with `Python >= 3.6.0`

For the `requirements-dev.txt` file you must leave the initial dependencies, newer versions of dependencies are acceptable. All Python projects are expected to use `pytest` for testing, code formatting, and typing you must follow the [Python Style Guideline](https://github.com/Investabit/documentation/wiki/Python-Style-Guide).

The default `requirements.txt` file includes a number of widely used libraries across all Investabit Python projects. All projects should use `investabit-python` which provides a unified library for RabbitMQ, PostgreSQL, and logging. There are a number of additional libraries included in `requirements.txt` such as for NumPy, Pandas, and plotting which can be removed if not needed.

Any new dependencies added should use the `~=` notation for versions of dependencies, in order to ensure that there are no breaking changes from major version upgrades. For NumPy and Pandas it is recommended to use the exact dependency version provided in the `requirements.txt` file, as newer versions of Pandas (0.24.0) are known to have bugs and other regressions which are currently not resolved.


## Development and Testing

When doing local development it's recommended to install the project using `setup.py` as this will also install all dependencies for code linting and formatting. Install the project using `python setup.py develop`, which will create symbol links to your code and include all dependencies from the requirements files.

All projects are required to use `pytest` for testing, `unittest`, `nose`, etc. are not supported. Furthermore, if possible you should also aim to run your tests locally using `pytest-xdist`, as this will allow for parallel testing and significantly reduces build times on Jenkins.

Any additional dependencies required for testing are fine to include, and it is recommended to be sensible and prefer smaller data files for the purposes of testing. Any testing data should be placed in a `data/` directory within `tests/`.


## Code Linting and Formatting

All Python code is expected to follow the [Python Style Guideline](https://github.com/Investabit/documentation/wiki/Python-Style-Guide). The CI/CD Jenkins platform will build and analyze your code and report any Flake8 or MyPy errors, it is expected that you ensure that your code meets the guidelines before pushing to the master branch.


## Code Structure

The provided template includes a directory `project`, this should be renamed appropriately for your own project and include all of the source code.

Any collection of files that can be logically grouped together should be placed into a package, it's preferable to have multiple packages (directories) containing the source files rather than having all Python source files in the root project folder.


## Production Deployment

Any code that is placed in the `master` branch is expected to be run in production, exceptions can be made for the initial development of a new project. But once the initial version of the project is completed and it is being used in production, no code should be placed in master unless it's also expected to be run in production.

All versioning of your project should be done using the `__version__.py` file, any code that is meant for production and is pushed to the `master` branch **must have the version updated**. The versioning is expected to follow [Semantic Versioning](https://semver.org) and made to ensure the version is [compatible with Python/Pip](https://www.python.org/dev/peps/pep-0440/#public-version-identifiers).

Once your code has been merged to master and is ready to be deployed in production ensure that you create a tag with `git` that has the same version as in the `__version__.py` file.
