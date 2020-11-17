import pytest

from apis.fulecard_api import FuelCardApi
from utils.db import LongTengServer


@pytest.fixture(scope='session')
def api(http, base_url):
    return FuelCardApi(http, base_url)


@pytest.fixture(scope='session')
def db(db):
    return LongTengServer(db)
