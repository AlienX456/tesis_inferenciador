import pytest
from sys import path

path.append('api')
path.append('adapa')
path.append('interfaz')

from api import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()