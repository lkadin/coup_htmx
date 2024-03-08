from coup import Player


class TestGame:

    def test_initialization(self, game):
        assert game.players == {}
        assert game.NUM_OF_CARDS == 2
        assert game.status == "Not started"
        assert game.actions == []

    def test_add_all_players(self, game):
        player_ids = [("1", "Alice"), ("2", "Bob")]
        game.add_all_players(player_ids)
        assert len(game.players) == 2
        assert "1" in game.players
        assert "2" in game.players

    def test_next_turn(self, game):
        player_ids = [("1", "Alice"), ("2", "Bob")]
        game.add_all_players(player_ids)
        assert game.whose_turn() == 0
        game.next_turn()
        assert game.whose_turn() == 1

    def test_whose_turn_name(self, game):
        player_ids = [("1", "Alice"), ("2", "Bob")]
        game.add_all_players(player_ids)
        assert game.whose_turn_name() == game.player_ids[game.current_player_index][1]

    def test_add_all_actions(self, game):
        game.add_all_actions()
        assert len(game.actions) == 6

    def enable_all_actions(self, game):
        game.enable_all_actions()
        for action in game.actions:
            assert action.status == "enabled"

    def test_wait(self, game):
        game.wait()
        assert game.status == "Waiting"

    def test_start(self, game):
        game.start()
        assert game.deck is not None
        assert len(game.actions) > 0

    def test_player(self, game, player):
        player_ids = [("1", "Alice"), ("2", "Bob")]
        game.add_all_players(player_ids)
        game.start()
        assert isinstance(game.player("1"), Player)
