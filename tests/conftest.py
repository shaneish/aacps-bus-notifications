import os
import pytest
import pathlib
import sys


def pytest_sessionstart(session):
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))


@pytest.fixture
def current_dir():
    return pathlib.Path(__file__).parent


@pytest.fixture
def get_request(postfix="0"):
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), f"resources/test-site_{postfix}.html"), "r") as f:
        return f.read()
