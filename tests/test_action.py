def test_action(action):
    assert action.name == "Coup"
    assert action.coins_required == 7
    assert action.status == "disabled"
    assert action.second_player_required is True
    assert repr(action) == "Coup"
