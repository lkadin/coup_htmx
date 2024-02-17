import pytest
from coup import Card  # Replace 'your_module' with the actual name of your module


@pytest.fixture
def card():
    return Card("Ace")


def test_init(card):
    assert card.value == "Ace"
