import pytest
from app import app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_terms_search():
    client = app.test_client()
    response = client.get("/?terms=Football,Rugby,Tennis")
    assert response.status_code == 200
    assert b"<h1> Football,Rugby,Tennis </h1>" in response.data
