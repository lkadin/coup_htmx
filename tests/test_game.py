from coup import Player
from coup import Action


class TestGame:

    def test_initialization(self, game):
        assert game.players == {}
        assert game.NUM_OF_CARDS == 2
        assert game.status == "Not started"
        assert game.actions == []

    def test_add_all_players(self, game, ids):
        game.add_all_players(ids)
        assert len(game.players) == 2
        assert "1" in game.players
        assert "2" in game.players

    def test_next_turn(self, game, ids):
        game.add_all_players(ids)
        assert game.whose_turn() == 0
        game.next_turn()
        assert game.whose_turn() == 1

    def test_whose_turn_name(self, game, ids):
        game.add_all_players(ids)
        assert game.whose_turn_name() == game.player_ids[game.current_player_index][1]

    def test_whose_turn(self, game, ids):
        game.add_all_players(ids)
        assert isinstance(game.whose_turn(), int)

    def test_add_all_actions(self, game):
        game.add_all_actions()
        assert len(game.actions) == 9

    def test_enable_all_actions(self, game):
        game.add_all_actions()
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

    def test_your_turn(self, game, ids):
        user_id = "1"
        game.start()
        game.add_all_players(ids)
        assert isinstance(game.your_turn(user_id), bool)

    def test_player(self, game, ids):
        game.add_all_players(ids)
        game.start()
        assert isinstance(game.player("1"), Player)

    def test_initial_deal(self, game, ids):
        game.add_all_players(ids)
        game.start()
        for player in game.players.values():
            assert len(player.hand) == 2

    def test_action_from_action_name(self, game):
        game.add_all_actions()
        for action in game.actions:
            assert isinstance(game.action_from_action_name(action.name), Action)
        assert game.action_from_action_name(None) is None
        assert game.action_from_action_name("FRED") is None
        assert isinstance(game.action_from_action_name("Assassinate"), Action)

    def test_process_actions(self, game, ids):
        game.add_all_players(ids)
        game.add_all_actions()
        user_id = "1"
        for action in game.actions:
            assert game.process_action(action, user_id) is None

    def test_steal(self, game, ids):
        game.add_all_players(ids)
        game.start()
        coins1 = game.players["1"].coins
        coins2 = game.players["2"].coins
        game.steal(give_to=game.players["1"].id, steal_from=game.players["2"].id)
        assert game.players["1"].coins == coins1 + 2
        assert game.players["2"].coins == coins2 - 2

    def test_player_id(self, game, ids):
        game.add_all_players(ids)
        assert game.player_id("Lee") == "1"
