import pytest
from coup import Card
from coup import Deck
from coup import Player
from coup import Game
from content import Content


@pytest.fixture
def player():
    return Player("1")


@pytest.fixture
def card():
    return Card("contessa")


@pytest.fixture
def deck():
    return Deck()


@pytest.fixture
def game():
    return Game()


@pytest.fixture
def game_ready(game):
    ids = [("1", "Lee"), ("2", "Adina"), ("3", "Joey"), ("9", "Jamie")]
    game.add_all_players(ids)
    game.start()
    return game


@pytest.fixture
def content(game_ready):
    return Content(game_ready, "1")
