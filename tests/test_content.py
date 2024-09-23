def test_show_hand(content, game_ready):
    player = game_ready.player("1")
    assert len(content.show_hand(player)) >= 100
    assert """<img src='/static/jpg""" in content.show_hand(player)


def test_show_table(content):
    assert len(content.show_table()) >= 100
    assert """<div hx-swap-oob="innerHTML:#cards">""" in content.show_table()


def test_show_turn(content):
    assert """<div id="turn""" in content.show_turn()


def test_show_history(content):
    assert """<div id="history""" in content.show_history()


# def test_show_game_status(content):
#     assert len(content.show_game_status()) > 10


def test_show_alert(content):
    assert len(content.show_game_alert()) > 10


def test_hide_second_player(content):
    assert len(content.hide_second_player()) > 10


def test_pick_second_player(content, game_ready):
    game_ready.players[game_ready.user_id].id = game_ready.player_index_to_id(
        game_ready.whose_turn()
    )
    assert len(content.pick_second_player()) > 10


def test_show_actions(content):
    assert len(content.show_actions()) > 10
