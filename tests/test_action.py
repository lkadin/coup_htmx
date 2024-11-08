def test_action(action):
    """
    Test that Action object is correctly initialized.
    """
    assert action.name == "Coup"
    assert action.coins_required == 7
    assert action.action_status == "disabled"
    assert action.second_player_required is True
    assert repr(action) == "Coup"
