import pytest
from coup import Player, Deck, Card


@pytest.fixture
def player():
    return Player("1")


@pytest.fixture
def deck():
    return Deck()


@pytest.fixture
def card():
    return Card("countessa")


def test_init(player):
    assert player.id == "1"
    assert player.hand == []
    assert player.coins == 2


def test_draw(player, deck):
    player.draw(deck)
    assert player.hand == ["contessa"]


def test_play_card(player):
    player.hand = ["Card1", "Card2", "Card3"]
    played_card = player.play_card()
    assert played_card == "Card3"
    assert player.hand == ["Card1", "Card2"]


def test_add_remove_coins(player):
    player.add_remove_coins(3)
    assert player.coins == 5
    player.add_remove_coins(-2)
    assert player.coins == 3
