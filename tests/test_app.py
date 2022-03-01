import pytest
import sys
import os
from app import app


@pytest.mark.skip
def test_all_entries():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    configs = {"general": {"users": "recipients_0.db"}}
    client = app.test_client()
    get_db = get_db
    response = client.get("/all_entries")
    print(response.data)