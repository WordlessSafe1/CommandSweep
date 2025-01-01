#!/bin/bash

PYTHON_EXEC=python3

which python3 >/dev/null
if [[ $? -eq 0 ]]; then
    PYTHON_EXEC=python3
else
    which python >/dev/null
    if [[ $? -eq 0 ]]; then
        PYTHON_EXEC=python
    else
        echo "No python or python3 found. Exiting... sorry!"
        exit 1
    fi
fi

echo "Creating src and tests directories."
mkdir src
mkdir tests
echo "Creating virtual environment 'env'."
$PYTHON_EXEC -m venv env

# Is this Mac/Linux or Windows?
BIN_DIR=env/bin
if [[ -d env/Scripts ]]; then
    BIN_DIR=env/Scripts
fi

echo "Installing Python libraries."
source $BIN_DIR/activate && python -m pip install --upgrade pip >/dev/null && python -m pip install black mypy pytest pylint >/dev/null  && python -m pip freeze >requirements.txt

if [[ $? -ne 0 ]]; then
    echo "ERROR: Library installation failed.  Exiting..."
    exit 1
fi

echo "Creating .pylintrc."
cat >.pylintrc <<EOPL
[DESIGN]
disable=missing-function-docstring,missing-module-docstring
argument-rgx=[a-z\_][a-z0-9_]{0,39}$
good-names=a,b,c,i,j,k,e,m,n,p,q,r,s,t,u,v,w,x,y,z,_,pk,st,rev
EOPL

echo "Creating Makefile."
cat >Makefile <<EOM
.PHONY: all
all: codestyle typecheck lint test build

.PHONY: codestyle
codestyle:
	python -m black -l 79 src/ tests/

.PHONY: typecheck
typecheck:
	python -m mypy --ignore-missing-imports src/

.PHONY: lint
lint:
	python -m pylint src/

.PHONY: test
test:
	python -m pytest tests/

.PHONY: build
build:
	pip install -e .

.PHONY: clean
clean:
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr
EOM

echo "Creating setup.py.  BE SURE TO MODIFY THIS FILE."
cat >setup.py <<EOSETUP
from setuptools import find_packages, setup

setup(
    name="FIXME",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "FIXME=FIXME.__main__:main",
        ]
    },
)
EOSETUP

echo ""
echo ""
echo "*****************************************************************"
echo "**************************** DONE! ******************************"
echo "*****************************************************************"
echo ""
echo ""
echo ""
echo "           vvvvv HEY!!! LOOK BELOW AND DO THIS!!!! vvvvv         "
echo ""
echo " --> Use 'source $BIN_DIR/activate' to enter new environment."
echo " --> Do this before typing 'make' or 'make all'."
echo ""
