#!/bin/bash

# Put the absolute path where the 'shared' python was installed
export PYTHONPATH=$PYTHONPATH:../../
NOSETESTS=/opt/mlc-python-3.6.2/bin/mlc_python

# Run Integration tests
$NOSETESTS integration_tests.py $@
