import random
from datetime import datetime

COUP_REQUIRED = 10  # # of coins when you MUST Coup


class Card:
    def __init__(self, value) -> None:
        self.value = value
        self.card_status = "down"


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

    def return_to_deck(self, cardname):
        self.cards.append(cardname)

    def __repr__(self) -> str:
        return " ".join([self.card for self.card in self.cards])


class Player:
    def __init__(self, id: str, name: str | None) -> None:
        self.id = id
        self.name = name
        self.hand = []
        self.coins = 2
        self.player_alert = ""

    def get_index(self, cardname: str):
        for index, card in enumerate(self.hand):
            if card.value == cardname and card.card_status == "down":
                return index
        raise Exception("Card to discard not found in hand")

    def draw(self, deck: Deck):
        self.hand.append(Card(deck.draw()))

    def discard(self, cardnames: list, deck: Deck):
        for cardname in cardnames:
            index = self.get_index(cardname)
            self.hand.pop(index)
            deck.return_to_deck(cardname)

    def play_card(self) -> list[str]:
        return self.hand.pop()

    def add_remove_coins(self, num_of_coins: int):
        self.coins += num_of_coins

    def lose_influence(self, cardname):
        self.cardname = cardname
        index = self.get_index(cardname)
        self.hand[index].card_status = "up"

    def influence(self) -> int:
        cards = 0
        for card in self.hand:
            if card.card_status == "down":
                cards += 1
        return cards

    def set_player_alert(self, message):
        self.player_alert = message

    def clear_player_alert(self):
        self.player_alert = ""

    def __repr__(self) -> str:
        return f"{self.id}-{self.hand} {self.coins=}"


class Action:
    def __init__(
        self,
        name,
        coins_required: int,
        action_status: str,
        second_player_required: bool,
        your_turn_only: bool = True,
    ) -> None:
        self.name = name
        self.coins_required = coins_required
        self.action_status = action_status
        self.second_player_required = second_player_required
        self.your_turn_only = your_turn_only

    def __repr__(self) -> str:
        return self.name


class Game:
    def __init__(self) -> None:
        self.players = {}
        self.NUM_OF_CARDS = 2
        self.game_status = "Not started"
        self.actions = []
        self.current_action = Action("No_action", 0, "disabled", False)
        self.second_player = None
        self.cards_to_exchange: list = []
        self.exchange_in_progress = False
        self.assassinate_in_progress = False
        self.coup_in_progress = False
        self.assassinate_in_progress = False
        self.current_player_index = 0
        self.required_discard_qty = 0
        self.action_history = []
        self.card_to_lose = None
        self.player_to_coup = None
        self.player_to_assassinate = None
        self.game_alert = ""
        self.couping_player = ""
        self.assassinating_player = ""
        self.players_remaining = []
        self.user_id = None
        self.must_coup = False
        self.player_ids = []
        self.ids = []

    def initial_deal(self):
        for _ in range(self.NUM_OF_CARDS):
            for player in self.players.values():
                player.draw(self.deck)

    def add_player(self, player_id: str, player_name: str):
        if player_name in [player.name for player in self.players.values()]:
            return False
        self.players[player_id] = Player(player_id, player_name)
        self.ids.append((player_id, player_name))
        self.add_all_players(self.ids)
        return True

    def add_all_players(self, player_ids: list[str]):
        self.player_ids = player_ids
        for player_id, player_name in self.player_ids:
            self.players[player_id] = Player(player_id, player_name)

    def next_turn(self, user_id):
        self.user_id = user_id
        self.add_history(self.user_id)
        self.current_player_index += 1
        if self.current_player_index >= len(self.players):
            self.current_player_index = 0
        if not self.players[str(self.current_player_index + 1)].influence():
            self.current_player_index += 1
        if self.current_player_index >= len(self.players):
            self.current_player_index = 0
        self.clear_all_player_alerts()
        self.second_player = None
        self.current_action = Action("No_action", 0, "disabled", False)
        if self.game_over():
            self.game_alert = f"Game Over - Winner - {self.players_remaining[0].name} "
            self.set_game_status("Game Over")
            self.add_all_actions()

    def whose_turn(self):
        return self.current_player_index

    def whose_turn_name(self):
        if self.game_status == "In progress":
            return self.player_ids[self.current_player_index][1]
        else:
            return None

    def add_all_actions(self):
        self.actions = []
        for (
            name,
            number_of_coins,
            self.action_status,
            second_player_required,
            your_turn_only,
        ) in [
            ("Assassinate", 3, "disabled", True, True),
            ("Coup", 7, "disabled", True, True),
            ("Steal", 0, "disabled", True, True),
            ("Take_3_coins", 0, "disabled", False, True),
            ("Foreign_aid", 0, "disabled", False, True),
            ("Income", 0, "disabled", False, True),
            ("Exchange", 0, "disabled", False, True),
            ("Block", 0, "disabled", False, False),
            ("Challenge", 0, "disabled", False, False),
        ]:
            self.actions.append(
                Action(
                    name,
                    number_of_coins,
                    self.action_status,
                    second_player_required,
                    your_turn_only,
                )
            )

        if self.game_status == "Waiting":
            self.actions.append(Action("Start", 0, "enabled", False))

        if self.game_status == "In Progress" and self.actions[-1:] == "Start":
            self.actions.pop()

    def wait(self):
        self.game_status = "Waiting"
        self.add_all_actions()

    def enable_all_actions(self):
        for self.action in self.actions:
            self.action.action_status = "enabled"

    def start(self):
        self.game_status = "In progress"
        self.deck = Deck()
        self.deck.shuffle()
        self.add_all_actions()
        self.enable_all_actions()
        self.initial_deal()
        self.clear_history()
        self.current_player_index = random.randint(0, len(self.players) - 1)

    def your_turn(self, user_id: str) -> bool:
        self.user_id = user_id
        whose_turn = self.whose_turn_name()
        name = self.players[self.user_id].name
        return whose_turn == name

    def process_action(self, action: Action, user_id: str):
        self.user_id = user_id
        if not isinstance(action, Action):
            action = self.action_from_action_name(action)

        if action.name == "Start" and self.game_status == "Waiting":
            self.start()
            return

        if (
            not self.your_turn(self.user_id)
            and not self.coup_in_progress
            and not self.assassinate_in_progress
        ):
            return

        if self.must_coup and action.name != "Coup":
            return

        if self.game_status == "Waiting":
            return

        if action.name == "Take_3_coins":
            self.player(self.user_id).add_remove_coins(3)
            self.next_turn(self.user_id)

        if action.name == "Income":
            self.player(self.user_id).add_remove_coins(1)
            self.next_turn(self.user_id)

        if action.name == "Foreign_aid":
            self.player(self.user_id).add_remove_coins(2)
            self.next_turn(self.user_id)

        if action.name == "Exchange":
            self.exchange(self.user_id)

        if action.second_player_required:
            self.current_action = action

        if action.name == "Steal" and self.second_player:
            self.steal(give_to=self.user_id, steal_from=self.second_player)

        if action.name == "Coup":
            self.coup(self.user_id)

        if action.name == "Assassinate":
            self.assassinate(self.user_id)

    def player(self, user_id) -> Player:
        self.user_id = user_id
        try:
            return self.players[self.user_id]
        except KeyError:
            return None

    def player_id(self, name) -> str:
        for player_id in self.player_ids:
            if player_id[1] == name:
                return player_id[0]
        return ""

    def steal(self, give_to, steal_from):
        self.player(give_to).add_remove_coins(2)
        self.player(steal_from).add_remove_coins(-2)
        self.next_turn(self.user_id)

    def exchange(self, user_id):
        self.user_id = user_id
        # if not self.cards_to_exchange:
        self.required_discard_qty = self.player(self.user_id).influence() - 2

        if not self.cards_to_exchange and self.exchange_in_progress:
            self.player(self.user_id).set_player_alert("You didn't pick any cards")
            return

        if self.required_discard_qty <= 2 and not self.cards_to_exchange:
            for _ in range(4 - self.player(self.user_id).influence()):
                self.player(self.user_id).draw(self.deck)
                self.exchange_in_progress = True

        if self.cards_to_exchange:
            if self.required_discard_qty != len(self.cards_to_exchange):
                self.player(self.user_id).set_player_alert(
                    "You didn't pick the correct amount of cards"
                )
                return
            self.player(self.user_id).discard(self.cards_to_exchange, self.deck)
            self.cards_to_exchange = []
            self.exchange_in_progress = False
            self.next_turn(self.user_id)

    def action_from_action_name(self, action_name: str) -> Action:
        default_action = Action("No_action", 0, "disabled", False)
        for action in self.actions:
            if action.name == action_name:
                return action
        return default_action

    def set_current_action(self, action_name: str, user_id: str):
        self.user_id = user_id
        self.current_action = self.action_from_action_name(action_name)
        self.must_coup = False
        if (
            self.check_coins(self.user_id) == -1 and self.current_action.name != "Coup"
        ):  # must coup
            self.must_coup = True
            self.current_action = Action("No_action", 0, "disabled", False)
            return
        if self.check_coins(self.user_id) == 1:
            return
        self.current_action = self.action_from_action_name(action_name)
        if self.current_action.your_turn_only and not self.your_turn(self.user_id):
            return

    def get_current_action(self):
        return self.current_action

    def set_second_player(self, player_name: str):
        self.second_player = None
        if player_name != "":
            self.second_player = player_name

    def set_cards_to_exchange(self, cardnames: list[str]):
        self.cards_to_exchange = cardnames

    def set_game_status(self, game_status: str):
        self.game_status = game_status

    def get_game_status(self):
        return self.game_status

    def coup(self, user_id):
        self.user_id = user_id
        if (
            not self.second_player and not self.coup_in_progress
        ):  # Need to pick second player
            return
        if (
            not self.card_to_lose
            and not self.coup_in_progress
            and self.player(self.user_id).influence()
        ):
            self.coup_in_progress = True
            self.player_to_coup = self.second_player
            self.couping_player = self.player(self.user_id).id
            self.second_player = None

        if self.card_to_lose and isinstance(self.card_to_lose, str):
            self.player(self.player_to_coup).lose_influence(self.card_to_lose)
            self.player(self.couping_player).add_remove_coins(-7)
            self.card_to_lose = None
            self.coup_in_progress = False
            self.couping_player = ""
            self.must_coup = False
            self.next_turn(self.user_id)
        else:
            if (
                not self.card_to_lose
                and self.coup_in_progress
                and self.player_to_coup == self.user_id
            ):
                self.player(self.user_id).set_player_alert("You must pick one card")

    def assassinate(self, user_id):
        self.user_id = user_id
        if (
            not self.second_player and not self.assassinate_in_progress
        ):  # need to pick second player
            return
        if (
            not self.card_to_lose
            and self.player(self.user_id).influence()
            and not self.assassinate_in_progress
        ):
            self.assassinate_in_progress = True
            self.player_to_assassinate = self.second_player
            self.assassinating_player = self.player(self.user_id).id
            self.second_player = None

        if self.card_to_lose and isinstance(self.card_to_lose, str):
            self.player(self.player_to_assassinate).lose_influence(self.card_to_lose)
            self.player(self.assassinating_player).add_remove_coins(-3)
            self.card_to_lose = None
            self.assassinate_in_progress = False
            self.assassinating_player = ""
            self.next_turn(self.user_id)
        else:
            if (
                not self.card_to_lose
                and self.assassinate_in_progress
                and self.player_to_assassinate == self.user_id
            ):
                self.player(self.user_id).set_player_alert("You must pick one card")

    def clear_history(self):
        self.action_history = []

    def add_history(self, user_id):
        self.user_id = user_id
        if not self.current_action:
            return
        if self.current_action.name == "Coup":
            self.player2 = self.player_to_coup
        elif self.current_action.name == "Assassinate":
            self.player2 = self.player_to_assassinate
        else:
            self.player2 = self.second_player
        h1 = History_action(
            self.player_ids[self.current_player_index][0],
            self.player2,
            self.current_action,
        )
        self.action_history.append(h1)

    def game_over(self):
        self.players_remaining = []
        self.over = False
        self.players_with_influence = 0
        for self.one_player in self.players.values():
            if self.one_player.influence():
                self.players_with_influence += 1
                self.players_remaining.append(self.one_player)
        if self.players_with_influence == 1:
            self.over = True
        return self.over

    def check_coins(self, user_id: str):
        if not self.current_action:  # Game has not started yet
            return 0
        self.user_id = user_id
        if self.player(self.user_id).coins >= COUP_REQUIRED:
            self.player(self.user_id).set_player_alert("You must coup")
            return -1
        if self.player(self.user_id).coins >= self.current_action.coins_required:
            return 0
        if self.player(self.user_id).coins < self.current_action.coins_required:
            return 1

    def clear_all_player_alerts(self):
        for player in self.players.values():
            player.clear_player_alert()


class History_action:
    def __init__(self, player1, player2, action):
        self.player1 = player1
        self.player2 = player2
        self.action = action
        self.time_added = datetime.now()
        if not self.player2:
            self.player2 = ""


def main():
    ids = [("1", "Lee"), ("2", "Adina")]
    game = Game()
    game.add_all_players(ids)
    game.wait()
    print(game.actions)
    game.start()
    print(game.actions)
    print(game.players)
    print(type(game.whose_turn()))
    print(game.player_id("Lee"))
    print(game.your_turn("1"))
    print(game.whose_turn_name())
    game.process_action(Action("Exchange", 0, "enabled", False), "1")
    print(game.players["1"])
    cards = ["contessa", "ambassador"]
    game.set_cards_to_exchange(cards)
    game.process_action(Action("Exchange", 0, "enabled", False), "1")
    print(game.players["1"])


if __name__ == "__main__":
    main()
