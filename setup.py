import imp
import re
import subprocess
from os.path import abspath, dirname, join
from typing import List, Optional, Tuple

from setuptools import find_packages, setup

# Package meta-data
NAME = "project"
VERSION = None  # Will use version provided in __version__ if None
DESCRIPTION = "A python template project."
LONG_DESCRIPTION = open("README.md").read()
AUTHOR = "Jonathan Gillett"
EMAIL = "jonathan.gillett@investabit.com"
URL = "https://github.com/Investabit/python-template"
PYTHON_REQUIRES = ">=3.6.0"
PIP_VER = 18  # Pip version, default is 18 unless we're able to determine it


# HACK: Try to determine pip version in order to support backwards compatability
try:
    try:
        from pip import __version__ as pip_version

        PIP_VER = int(re.search(r"(\d+)\.", pip_version).group(1))
    except (ImportError, ModuleNotFoundError):  # HACK: Load the version directly!
        path = imp.find_module("pip")
        if path:
            pip_version = imp.load_source("pip", join(path[1], "_vendor/packaging/__init__.py"))
            PIP_VER = int(re.search(r"(\d+)\.", pip_version.__version__).group(1))
except Exception as e:  # Last ditch attempt
    print("Failed to import pip, trying subprocess, error: {}".format(e))
    try:
        res = subprocess.run(["pip", "--version"], stdout=subprocess.PIPE)
        PIP_VER = int(re.search(r"pip\s+(\d+).*?\s", res.stdout.decode("utf-8")).group(1))
    except Exception:
        print("Failed to determine pip version, assuming version {}!".format(PIP_VER))


def find_version(project: Optional[str] = None) -> str:
    """Searches the package init file for the version."""
    if not VERSION:
        version = dict()
        try:
            if project is None:
                project = NAME.lower().replace("-", "_").replace(" ", "_")
            with open(join(abspath(dirname(__file__)), project, "__version__.py")) as f:
                exec(f.read(), version)
            return str(version["__version__"])
        except Exception:
            raise RuntimeError("Unable to find package version.")
    else:
        return VERSION


def parse_requirements(filename: str) -> Tuple[List[str], List[str]]:
    """Parse the requirements file and ignore any lines starting with a hashtag comment."""
    try:
        with open(join(dirname(__file__), filename)) as f:
            requirements = [req.strip() for req in f.read().splitlines()]
    except IOError:
        raise RuntimeError("Could not find the requirements file")
    pkgs, links = [], []
    for req in requirements:
        if not req or re.findall(r"^(\#+)", req):
            continue
        # Fix for inline comments
        req = re.findall(r"^([^\s]+)\s*?\#*", req)[0]
        if any(r in req for r in ["https", "http", "git"]):
            res = re.findall(r"\#egg=([^\-]+)-(.+$)", req)
            if not res:
                # Try and just get it without version
                res = re.findall(r"\#egg=([^\-]+)", req)
                if res:
                    name, version = res[0].strip(), ""
                else:
                    # Just get the name from the URL
                    name, version = re.search(r"^(\w+).*?", req.split("/")[-1]).group(1), ""
            else:
                name, version = [x.strip() for x in res[0]]
            # Support for pip versions >= 18, which allows URL for install_requires
            if PIP_VER and PIP_VER >= 18:
                pkgs.append("{} @ {}".format(name, req))
            else:
                if version:
                    pkgs.append("{}=={}".format(name, version))
                else:
                    pkgs.append(name)
                links.append(req)
        else:
            pkgs.append(req)
    return pkgs, links


# Get the installation dependencies from requirements files
install_requires, install_links = parse_requirements("requirements.txt")
tests_require, tests_links = parse_requirements("requirements-dev.txt")
dependency_links = list(set(install_links + tests_links))


setup(
    name=NAME,
    version=find_version(),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    python_requires=PYTHON_REQUIRES,
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=install_requires,
    tests_require=tests_require,
    dependency_links=dependency_links,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
