import logging
import pytest
from api_client import MetMuseumClient


def pytest_configure():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s'
    )


@pytest.fixture(scope="session")
def client():
    return MetMuseumClient()
