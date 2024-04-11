from coup import Player
from coup import Action
from coup import Card


class TestGame:

    def test_initialization(self, game):
        assert game.players == {}
        assert game.NUM_OF_CARDS == 2
        assert game.game_status == "Not started"
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
        game.next_turn()
        assert game.whose_turn() == 0

    def test_whose_turn_name(self, game_ready, ids):
        assert (
            game_ready.whose_turn_name()
            == game_ready.player_ids[game_ready.current_player_index][1]
        )

    def test_whose_turn(self, game_ready, ids):
        assert isinstance(game_ready.whose_turn(), int)

    def test_add_all_actions(self, game_ready):
        game_ready.set_game_status(None)
        game_ready.add_all_actions()
        assert len(game_ready.actions) == 9

        game_ready.set_game_status("Waiting")
        game_ready.add_all_actions()
        assert len(game_ready.actions) == 10

        game_ready.set_game_status("In Progress")
        game_ready.add_all_actions()
        assert len(game_ready.actions) == 9

    def test_enable_all_actions(self, game_ready):
        for action in game_ready.actions:
            assert action.action_status == "enabled"

    def test_wait(self, game):
        game.wait()
        assert game.game_status == "Waiting"

    def test_start(self, game):
        game.start()
        assert game.deck is not None
        assert len(game.actions) > 0

    def test_your_turn(self, game_ready):
        user_id = "1"
        assert isinstance(game_ready.your_turn(user_id), bool)

    def test_player(self, game_ready, ids):
        assert isinstance(game_ready.player("1"), Player)

    def test_initial_deal(self, game_ready, ids):
        for player in game_ready.players.values():
            assert len(player.hand) == 2

    def test_action_from_action_name(self, game_ready):
        for action in game_ready.actions:
            assert isinstance(game_ready.action_from_action_name(action.name), Action)
        assert game_ready.action_from_action_name(None) is None
        assert game_ready.action_from_action_name("FRED") is None
        assert isinstance(game_ready.action_from_action_name("Assassinate"), Action)

    def test_process_action(self, game_ready):
        user_id = str(int(game_ready.whose_turn()) + 1)
        for action in game_ready.actions:
            assert game_ready.process_action(action, user_id) is None
        # Take_3_coins
        coins1 = game_ready.players[user_id].coins
        game_ready.process_action("Take_3_coins", user_id)
        assert game_ready.players[user_id].coins == coins1

        # Steal
        coins1 = game_ready.players[user_id].coins
        coins2 = game_ready.players["1"].coins
        game_ready.second_player = user_id
        game_ready.process_action("Steal", user_id)
        assert game_ready.players[user_id].coins == coins1
        assert game_ready.players["1"].coins == coins2

        # Start

    def test_process_action_start(self, game_ready):
        action = Action("Start", 0, "enabled", False)
        user_id = game_ready.player_ids[game_ready.current_player_index][0]
        game_ready.set_game_status("Waiting")
        game_ready.process_action(action, user_id)
        assert game_ready.game_status == "In progress"

    def test_process_action_take_3_coins(self, game_ready):
        action = "Take_3_coins"
        user_id = game_ready.player_ids[game_ready.current_player_index][0]
        coins = game_ready.players[user_id].coins
        game_ready.process_action(action, user_id)
        assert game_ready.players[user_id].coins == coins + 3

    def test_process_action_income(self, game_ready):
        action = "Income"
        user_id = game_ready.player_ids[game_ready.current_player_index][0]
        coins = game_ready.players[user_id].coins
        game_ready.process_action(action, user_id)
        assert game_ready.players[user_id].coins == coins + 1

    def test_process_action_foreign_aid(self, game_ready):
        action = "Foreign_aid"
        user_id = game_ready.player_ids[game_ready.current_player_index][0]
        coins = game_ready.players[user_id].coins
        game_ready.process_action(action, user_id)
        assert game_ready.players[user_id].coins == coins + 2

    def test_steal(self, game_ready):
        coins1 = game_ready.players["1"].coins
        coins2 = game_ready.players["2"].coins
        game_ready.steal(
            give_to=game_ready.players["1"].id, steal_from=game_ready.players["2"].id
        )
        assert game_ready.players["1"].coins == coins1 + 2
        assert game_ready.players["2"].coins == coins2 - 2

    def test_player_id(self, game_ready, ids):
        assert game_ready.player_id("Lee") == "1"

    def test_exchange(self, game_ready):
        user_id = "1"
        game_ready.players[user_id].hand = [Card("captain"), Card("duke")]
        game_ready.exchange(user_id)
        assert len(game_ready.players[user_id].hand) == 4
        game_ready.cards_to_exchange = ["captain", "duke"]
        game_ready.exchange(user_id)
        assert len(game_ready.players["1"].hand) == 2

    def test_set_current_action(self, game_ready):
        game_ready.set_current_action("Steal", "1")
        assert game_ready.get_current_action().name == "Steal"

    def test_set_game_status(self, game_ready):
        assert game_ready.get_game_status() == "In progress"
        game_ready.set_game_status("Waiting")
        assert game_ready.get_game_status() == "Waiting"
