from coup import Game
from content import Content


def test_show_hand(deck):
    ids = [("1", "Lee"), ("2", "Adina"), ("3", "Joey"), ("9", "Jamie")]
    game = Game()
    game.add_all_players(ids)
    game.start()
    content = Content(game, "1")
    assert len(content.show_table()) >= 100
