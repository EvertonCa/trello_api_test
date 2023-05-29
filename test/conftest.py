import pytest

from trello_cli.utils.trello_api import TrelloAPI


@pytest.fixture(scope="session")
def trello_api():
    """Create TrelloAPI object"""
    trello_api = TrelloAPI()
    return trello_api
