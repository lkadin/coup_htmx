import pytest
from coup import Card
from coup import Deck
from coup import Player


@pytest.fixture
def player():
    return Player("1")


@pytest.fixture
def card():
    return Card("contessa")


@pytest.fixture
def deck():
    return Deck()
