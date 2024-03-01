def test_show_hand(content, game_ready):
    player = game_ready.player("1")
    assert len(content.show_hand(player)) >= 100


def test_show_table(content):
    assert len(content.show_table()) >= 100


def test_show_actions(content):
    assert len(content.show_actions()) >= 100
