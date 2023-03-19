# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import sample.simple


def test_add_one():
    assert sample.simple.add_one(5) == 6
