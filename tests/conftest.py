import os
import pytest
import pathlib
import sys
import sqlite3


def pytest_sessionstart(session):
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))


@pytest.fixture()
def current_dir():
    return pathlib.Path(__file__).parent


@pytest.fixture()
def get_request(postfix="0"):
    with open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            f"resources/test-site_{postfix}.html",
        ),
        "r",
    ) as f:
        return f.read()


@pytest.fixture()
def get_db(postfix="0"):
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"resources/recipients_{postfix}.db")
    db = sqlite3.connect(db_path)
    return db
