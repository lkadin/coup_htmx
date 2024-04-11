def test_show_hand(content, game_ready):
    player = game_ready.player("1")
    assert len(content.show_hand(player)) >= 100
    assert """<img src='/static/jpg""" in content.show_hand(player)


def test_show_table(content):
    assert len(content.show_table()) >= 100
    assert """<div hx-swap-oob="innerHTML:#cards">""" in content.show_table()


def test_show_turn(content):
    assert """<div hx-swap-oob="innerHTML:#turn">""" in content.show_turn()


def test_show_history(content):
    assert """<div hx-swap-oob="innerHTML:#history">""" in content.show_history("Test")
