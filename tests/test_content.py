def test_show_hand(deck, content, game):
    ids = [("1", "Lee"), ("2", "Adina"), ("3", "Joey"), ("9", "Jamie")]
    game.add_all_players(ids)
    game.start()
    # content = Content(game, "1")
    assert len(content.show_table()) >= 100
