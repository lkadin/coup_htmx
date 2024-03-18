import random


class Card:
    def __init__(self, value) -> None:
        self.value = value


class Deck:
    def __init__(self) -> None:
        self.cards = []
        for value in ["duke", "assassin", "ambassador", "captain", "contessa"]:
            for _ in range(3):
                self.cards.append(value)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self) -> Card:
        return self.cards.pop()

    def __repr__(self) -> str:
        return " ".join([self.card for self.card in self.cards])


class Player:
    def __init__(self, id: str, name: str = None) -> None:
        self.id = id
        self.name = name
        self.hand = []
        self.coins = 2

    def draw(self, deck: Deck):
        self.hand.append(deck.draw())

    def play_card(self) -> list[str]:
        return self.hand.pop()

    def add_remove_coins(self, num_of_coins: int):
        self.coins += num_of_coins

    def __repr__(self) -> str:
        return self.id + " - " + " ".join(self.hand) + " " + f"{self.coins=}"


class Action:
    def __init__(
        self, name, coins_required: int, status: str, second_player_required: bool
    ) -> None:
        self.name = name
        self.coins_required = coins_required
        self.status = status
        self.second_player_required = second_player_required

    def __repr__(self) -> str:
        return self.name


class Game:
    def __init__(self) -> None:
        self.players = {}
        self.NUM_OF_CARDS = 2
        self.status = "Not started"
        self.actions = []
        self.current_action: Action = None
        self.second_player = None

    def initial_deal(self):
        for _ in range(self.NUM_OF_CARDS):
            for player in self.players.values():
                player.draw(self.deck)

    def add_all_players(self, player_ids: list[str]):
        self.player_ids = player_ids
        for player_id, player_name in self.player_ids:
            self.players[player_id] = Player(player_id, player_name)
        random.shuffle(self.player_ids)
        self.current_player_index = 0

    def next_turn(self):
        self.current_player_index += 1
        if self.current_player_index >= len(self.players):
            self.current_player_index = 0
        self.second_player = None
        self.current_action = None

    def whose_turn(self):
        return self.current_player_index

    def whose_turn_name(self):
        return self.player_ids[self.current_player_index][1]

    def add_all_actions(self):
        self.actions = []
        for name, number_of_coins, status, second_player_required in [
            ("Assassinate", 3, "disabled", True),
            ("Coup", 7, "disabled", True),
            ("Steal", 0, "disabled", True),
            ("Take_3_coins", 0, "disabled", False),
            ("Foreign_aid", 0, "disabled", False),
            ("Income", 0, "disabled", False),
            ("Exchange", 0, "disabled", False),
            ("Block", 0, "disabled", False),
            ("Challenge", 0, "disabled", False),
        ]:
            self.actions.append(
                Action(name, number_of_coins, status, second_player_required)
            )

        if self.status == "Waiting":
            self.actions.append(Action("Start", 0, "enabled", False))
        if self.status == "In Progress":
            del self.actions["Start"]

    def wait(self):
        self.status = "Waiting"
        self.add_all_actions()

    def enable_all_actions(self):
        for self.action in self.actions:
            self.action.status = "enabled"

    def start(self):
        self.status = "In progress"
        self.deck = Deck()
        self.deck.shuffle()
        self.add_all_actions()
        self.enable_all_actions()
        self.initial_deal()

    def your_turn(self, user_id: str) -> bool:
        return self.whose_turn_name() == self.players[user_id].name

    def process_action(self, action: Action, user_id: str):
        assert isinstance(action, Action)
        if not self.your_turn(user_id):
            return

        if action.name == "Start" and self.status == "Waiting":
            self.start()
            return

        if self.status == "Waiting":
            return

        if action.name == "Take_3_coins":
            self.player(user_id).add_remove_coins(3)
            self.next_turn()

        if action.name == "Income":
            self.player(user_id).add_remove_coins(1)
            self.next_turn()

        if action.name == "Foreign_aid":
            self.player(user_id).add_remove_coins(2)
            self.next_turn()

        if action.second_player_required:
            self.current_action = action

        if action == "Steal" and self.second_player:
            self.steal(give_to=user_id, steal_from=self.second_player)

    def player(self, user_id) -> Player:
        return self.players[user_id]

    def player_id(self, name) -> str:
        for player_id in self.player_ids:
            if player_id[1] == name:
                return player_id[0]

    def steal(self, give_to, steal_from):
        self.player(give_to).add_remove_coins(2)
        self.player(steal_from).add_remove_coins(-2)
        self.next_turn()

    def action_from_action_name(self, action_name: str) -> Action:
        for action in self.actions:
            if action.name == action_name:
                return action


def main():
    ids = [("1", "Lee"), ("2", "Adina"), ("3", "Joey"), ("9", "Jamie")]
    game = Game()
    game.add_all_players(ids)
    game.wait()
    print(game.actions)
    game.start()
    print(game.actions)
    game.steal("2", "1")
    print(game.players)
    print(type(game.whose_turn()))
    print(game.player_id("Lee"))


if __name__ == "__main__":
    main()
