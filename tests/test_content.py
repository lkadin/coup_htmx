def test_show_hand(content, game_ready):
    # content = Content(game_ready, "1")
    player = game_ready.player("1")
    assert len(content.show_hand(player)) >= 100
