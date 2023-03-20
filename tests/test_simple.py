# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import excelbudget.simple


def test_add_one():
    assert excelbudget.simple.add_one(5) == 6
