# Tests will be written once the application is somewhat working.
from pytest import raises

from gustav_engine.main import cli


def test_main():
    with raises((TypeError, AttributeError)):
        cli(test=NotImplemented)