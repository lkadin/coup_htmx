import random
from datetime import datetime

COUP_REQUIRED = 10  # of coins when you MUST Coup
REQUIRED_CARD = {
    "Assassinate": ["assassin"],
    "Steal": ["captain"],
    "Exchange": ["ambassador"],
    "Take_3_coins": ["duke"],
    # block the following:
    "Block_Foreign_aid": ["duke"],
    "Block_Steal": ["ambassador", "captain"],
    "Block_Assassinate": ["contessa"],
}


class No_Card(Exception):
    pass


class Card:
    def __init__(self, value) -> None:
        self.value = value
        self.card_status = "down"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.value == other.value and self.card_status == other.card_status


class Deck:
    def __init__(self) -> None:
        self.cards = []
        for value in ["duke", "assassin", "ambassador", "captain", "contessa"]:
            for _ in range(3):
                self.cards.append(value)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self) -> Card:
        return self.cards.pop(0)

    def return_to_deck(self, cardname):
        self.cards.append(cardname)

    def __repr__(self) -> str:
        return " ".join([self.card for self.card in self.cards])


class Player:
    def __init__(self, id: str, name: str | None) -> None:
        self.id = id
        self.name = name
        self.hand: list[Card] = []
        self.coins = 2
        self.player_alert = ""
        self.cards_prior_to_exchange: list[Card] = []

    def reset(self):
        self.hand: list[Card] = []
        self.coins = 2
        self.player_alert = ""
        self.cards_prior_to_exchange: list[Card] = []

    def get_index(self, cardname: str) -> int:
        for index, card in enumerate(self.hand):
            if card.value == cardname and card.card_status == "down":
                return index
        raise No_Card("Card to discard not found in hand")

    def draw(self, deck: Deck) -> None:
        self.hand.append(Card(deck.draw()))

    def discard(self, cardnames: list, deck: Deck) -> None:
        for cardname in cardnames:
            index = self.get_index(cardname)
            self.hand.pop(index)
            deck.return_to_deck(cardname)

    def add_remove_coins(self, num_of_coins: int) -> None:
        self.coins += num_of_coins

    def lose_influence(self, cardname) -> None:
        self.cardname = cardname
        index = self.get_index(cardname)
        self.hand[index].card_status = "up"

    def lose_all_influence(self):
        for card in self.hand:
            card.card_status = "up"

    def influence(self) -> int:
        cards = 0
        for card in self.hand:
            if card.card_status == "down":
                cards += 1
        return cards

    def set_player_alert(self, message) -> None:
        self.player_alert = message

    def clear_player_alert(self) -> None:
        self.player_alert = ""

    def check_card_in_hand(self, cards_to_check: list[str], check_prior: bool):
        if check_prior:
            hand = self.cards_prior_to_exchange.copy()
        else:
            hand = self.hand.copy()
        for card in hand:
            if card.value in cards_to_check and card.card_status == "down":
                return card.value
        return None

    def save_cards(self):
        self.cards_prior_to_exchange = self.hand.copy()
        pass

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
        can_be_blocked: bool = False,
        can_be_challenged: bool = False,
    ) -> None:
        self.name = name
        self.coins_required = coins_required
        self.action_status = action_status
        self.second_player_required = second_player_required
        self.your_turn_only = your_turn_only
        self.can_be_blocked = can_be_blocked
        self.can_be_challenged = can_be_challenged

    def __repr__(self) -> str:
        return self.name


class Game:
    def __init__(self) -> None:
        self.players: dict[str, Player] = {}
        self.NUM_OF_CARDS: int = 2
        self.game_status: str = "Not started"
        self.actions: list[Action] = []
        self.current_action: Action = Action("No_action", 0, "disabled", False)
        self.current_action_player_id: str = ""
        self.second_player_id: str = ""
        self.cards_to_exchange: list[str] = []
        self.exchange_in_progress: bool = False
        self.coup_assassinate_in_progress: bool = False
        self.current_player_index: int = 0
        self.action_history: list[History_action] = []
        self.card_name_to_lose: str = ""
        self.player_id_to_lose_influence: str = ""
        self.game_alert: str = ""
        self.couping_assassinating_player: Player | None = None
        self.players_remaining = []
        self.user_id: str = ""
        self.must_coup_assassinate: bool = False
        self.block_in_progress: bool = False
        self.blocking_player: Player | None = None
        self.challenge_in_progress: bool = False
        self.last_challenge_successful = False
        self.lose_influence_in_progress = False
        self.last_user_id_assigned = 0

    def initial_deal(self) -> None:
        for _ in range(self.NUM_OF_CARDS):
            for player in self.players.values():
                player.draw(self.deck)

    def add_player(self, player_id: str, player_name: str) -> bool:
        if player_name in [player.name for player in self.players.values()]:
            return False
        self.players[player_id] = Player(player_id, player_name)
        return True

    def next_turn(self) -> None:
        self.add_history()
        self.next_player()
        self.clear_all_player_alerts()
        self.clear_game_alerts()
        self.second_player_id = ""
        self.current_action = Action("No_action", 0, "disabled", False)
        self.lose_influence_in_progress = False
        self.coup_assassinate_in_progress = False

    def next_player(self):
        self.current_player_index += 1
        if self.current_player_index >= len(self.players):
            self.current_player_index = 0
        self.current_player_id = str(
            self.player_id_from_index(self.current_player_index)
        )

        while not self.player(self.current_player_id).influence():
            self.current_player_index += 1
            if self.current_player_index >= len(self.players):
                self.current_player_index = 0
            self.current_player_id = str(
                self.player_id_from_index(self.current_player_index)
            )

        self.current_player_id = str(
            self.player_id_from_index(self.current_player_index)
        )

    def whose_turn(self) -> int:
        return self.current_player_index

    def whose_turn_name(self) -> str | None:
        if self.game_status == "In progress":
            for i, player in enumerate(self.players):
                if i == self.current_player_index:
                    return self.players[player].name
        else:
            return None

    def player_index_to_id(self, index: int) -> str:
        for i, player in enumerate(self.players):
            if i == self.current_player_index:
                return self.players[player].id
        else:
            return ""

    def add_all_actions(self):
        self.actions = []
        for (
            name,
            number_of_coins,
            self.action_status,
            second_player_required,
            your_turn_only,
            can_be_blocked,
            can_be_challenged,
        ) in [
            ("Assassinate", 3, "disabled", True, True, True, True),
            ("Coup", 7, "disabled", True, True, False, False),
            ("Steal", 0, "disabled", True, True, True, True),
            ("Take_3_coins", 0, "disabled", False, True, False, True),
            ("Foreign_aid", 0, "disabled", False, True, True, False),
            ("Income", 0, "disabled", False, True, False, False),
            ("Exchange", 0, "disabled", False, True, False, True),
            ("Block", 0, "disabled", False, False, False, True),
            ("Challenge", 0, "disabled", False, False, False, False),
            ("Accept_Block", 0, "disabled", False, False, False, False),
            ("Restart", 0, "disabled", False, False, False, False),
        ]:
            self.actions.append(
                Action(
                    name,
                    number_of_coins,
                    self.action_status,
                    second_player_required,
                    your_turn_only,
                    can_be_blocked,
                    can_be_challenged,
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
            if self.action.name != "Restart":
                self.action.action_status = "enabled"

    def enable_one_action(self, action_name):
        for self.action in self.actions:
            if self.action.name == action_name:
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

    def restart(self):
        for player in self.players.values():
            player.reset()
            self.clear_all_player_alerts
            self.clear_game_alerts()
            self.challenge_in_progress = False
            self.coup_assassinate_in_progress = False
            self.couping_assassinating_player = None
            self.over = False
            self.exchange_in_progress = False
            self.lose_influence_in_progress = False
            self.actions.pop()  # remove restart action
        self.start()

    def your_turn(self) -> bool:
        whose_turn = self.whose_turn_name()
        name = self.players[self.user_id].name
        return whose_turn == name

    def process_action(self, action: Action, user_id: str):
        print(f"processing {action=} {user_id=}")
        if self.game_over():
            self.game_alert = f"Game Over - Winner - {self.players_remaining[0].name} "
            self.set_game_status("Game Over")
            self.add_all_actions()
            self.enable_one_action("Restart")
        self.user_id = user_id
        if not isinstance(action, Action):
            action = self.action_from_action_name(action)
        if action.name == "Restart":
            self.restart()
        if self.block_in_progress and self.current_action.name not in (
            "Accept_Block",
            "Challenge",
        ):
            return  # Can't do anything if block in progress

        if self.lose_influence_in_progress and self.card_name_to_lose:
            self.process_lose_influence()

        if action.name == "Block":
            if not self.action_history:
                return
            try:
                if self.user_id == self.action_history[-1].player1.id:
                    return  # can't block yourself
            except AttributeError as e:
                print(e)
                print(self.action_history)

            if self.action_history[-1].action.can_be_blocked:
                self.block_in_progress = True
                self.blocking_player = self.player(self.user_id)
                self.game_alert = f"{self.player(self.user_id).name} is blocking"
                self.add_history()  ################################################### Why

        if action.name == "Accept_Block":
            if not self.block_in_progress:
                action = None  # type: ignore
                return  # can't accept your own block
            try:
                if self.user_id == self.action_history[-1].player1.id:
                    return  # can't block yourself
            except AttributeError as e:
                print(e)
                print(self.action_history)

            self.reverse_last_action()
            if self.coup_assassinate_in_progress:
                self.next_turn()
            else:
                self.add_history()  ################################## Why
            self.block_in_progress = False
            self.coup_assassinate_in_progress = False
            self.blocking_player = None
            self.clear_game_alerts()

        if action.name == "Challenge":
            self.challenge()

        if (
            action.name == "Start"
            and self.game_status == "Waiting"
            and len(self.players) > 1
        ):
            self.start()
            return

        if (
            not self.your_turn()
            and not self.coup_assassinate_in_progress
            and not self.block_in_progress
            and not self.challenge_in_progress
        ):
            return

        if self.must_coup_assassinate and action.name != "Coup":
            return

        if self.game_status == "Waiting":
            return

        if action.name == "Take_3_coins":
            self.player(self.user_id).add_remove_coins(3)
            self.next_turn()

        if action.name == "Income":
            self.player(self.user_id).add_remove_coins(1)
            self.next_turn()

        if action.name == "Foreign_aid":
            self.player(self.user_id).add_remove_coins(2)
            self.next_turn()

        if action.name == "Exchange":
            self.exchange(self.user_id)

        if action.second_player_required:
            self.current_action = action

        if action.name == "Steal" and self.second_player_id:
            self.steal(give_to=self.user_id, steal_from=self.second_player_id)

        if action.name in ("Assassinate", "Coup"):
            if self.block_in_progress:
                return  # must finish block
            self.coup_assassinate(self.user_id)

    def player(self, user_id) -> Player:
        try:
            return self.players[user_id]
        except KeyError:
            return None  # type: ignore

    def player_id(self, name) -> str:
        for i, player in enumerate(self.players):
            if self.players[player].name == name:
                return self.players[player].id
        return ""

    def steal(self, give_to, steal_from):
        self.player(give_to).add_remove_coins(2)
        self.player(steal_from).add_remove_coins(-2)
        self.next_turn()

    def exchange(self, user_id):
        self.user_id = user_id

        if not self.cards_to_exchange and self.exchange_in_progress:
            self.player(self.user_id).set_player_alert("You didn't pick any cards")
            return

        if not self.cards_to_exchange:
            self.player(self.user_id).save_cards()
            for _ in range(2):
                self.player(self.user_id).draw(self.deck)
                self.exchange_in_progress = True

        if self.cards_to_exchange:
            number_of_cards_to_discard = 2
            if number_of_cards_to_discard != len(self.cards_to_exchange):
                self.player(self.user_id).set_player_alert(
                    "You didn't pick the correct amount of cards"
                )
                return
            self.player(self.user_id).discard(self.cards_to_exchange, self.deck)
            self.cards_to_exchange = []
            self.exchange_in_progress = False
            self.next_turn()

    def challenge_can_continue(self):
        if not self.action_history:
            return
        if self.action_history[-1].action.name == "Challenge":
            return  # Can't challenge a challenge
        if (
            self.user_id == self.action_history[-1].player1.id
            and not self.lose_influence_in_progress
        ):
            return  # can't challenge yourself
        if self.exchange_in_progress:
            return  # can't challenge in the middle of exchange
        if not self.player(self.user_id).influence():
            return  # can't challenge if no influence
        return True

    def challenge(self):
        if not self.challenge_can_continue():
            return

        self.block_in_progress = False
        self.lose_influence_in_progress = True
        self.challenge_in_progress = True

        if self.challenge_successful():
            self.game_alert = f"{self.player(self.user_id).name} challenge is successful"  #### attacker doesn't have the correct card
            self.last_challenge_successful = True
            self.reverse_last_action_challenge()
            self.player_id_to_lose_influence = self.action_history[-1].player1.id  # type: ignore
            self.add_history()
        else:
            self.game_alert = f"{self.player(self.user_id).name} challenge is unsuccessful"  #### attacker has the correct card
            self.last_challenge_successful = False
            self.swap_winning_card()
            self.player_id_to_lose_influence = self.user_id
            if self.action_history[-1].action.name == "Assassinate":
                self.players[self.user_id].lose_all_influence()
                self.next_turn()

    def swap_winning_card(self):
        #####if exchange only swap card if it's still in the hand ##################
        try:
            self.player(self.action_history[-1].player1.id).discard(
                [self.required_card], self.deck
            )
            self.player(self.action_history[-1].player1.id).draw(self.deck)
        except No_Card:

            pass

    def action_from_action_name(self, action_name: str) -> Action:
        default_action = Action("No_action", 0, "disabled", False)
        for action in self.actions:
            if action.name == action_name:
                return action
        return default_action

    def set_current_action(self, action_name: str, user_id: str):
        self.user_id = user_id
        self.current_action = self.action_from_action_name(action_name)
        self.current_action_player_id = user_id
        self.must_coup_assassinate = False
        if (
            self.check_coins(self.user_id) == -1 and self.current_action.name != "Coup"
        ):  # must coup
            self.must_coup_assassinate = True
            # self.current_action = Action("No_action", 0, "disabled", False)
            return
        if self.check_coins(self.user_id) == 1:
            return
        if self.current_action.your_turn_only and not self.your_turn():
            return

    def get_current_action(self):
        return self.current_action

    def set_second_player_id(self, player_id: str):
        self.second_player_id = ""
        if player_id != "":
            self.second_player_id = player_id

    def set_cards_to_exchange(self, cardnames: list[str]):
        self.cards_to_exchange = cardnames

    def set_game_status(self, game_status: str):
        self.game_status = game_status

    def get_game_status(self):
        return self.game_status

    def coup_assassinate(self, user_id):
        self.user_id = user_id
        if (
            not self.second_player_id and not self.coup_assassinate_in_progress
        ):  # Need to pick second player
            return
        if (  ###no card was picked
            not self.card_name_to_lose
            and not self.coup_assassinate_in_progress
            and self.player(self.user_id).influence()
        ):
            self.coup_assassinate_in_progress = True
            self.lose_influence_in_progress = True
            self.player_id_to_lose_influence = self.second_player_id
            self.couping_assassinating_player = self.player(self.user_id)
            # self.add_history()
            self.second_player_id = ""
            self.couping_assassinating_player.add_remove_coins(  # type: ignore
                (self.current_action.coins_required * -1)
            )
            self.next_turn()

        self.process_lose_influence()

    def process_lose_influence(self):
        if self.card_name_to_lose and isinstance(
            self.card_name_to_lose, str
        ):  # card was picked need to lose influence
            self.player(self.player_id_to_lose_influence).lose_influence(
                self.card_name_to_lose
            )
            self.coup_assassinate_in_progress = False
            self.couping_assassinating_player = None
            self.must_coup_assassinate = False
            self.lose_influence_in_progress = False
            self.card_name_to_lose = ""
        else:
            if (
                not self.card_name_to_lose
                and self.coup_assassinate_in_progress
                and self.player_id_to_lose_influence == self.user_id
            ):
                self.player(self.user_id).set_player_alert("You must pick one card")
        self.lose_influence_in_progress = False

    def clear_history(self):
        self.action_history = []

    def add_history(self):
        if not self.current_action:
            return
        self.player2 = self.player(self.second_player_id)
        if self.current_action.name in ("Challenge", "Block"):
            self.player2 = self.action_history[-1].player1

        if self.current_action.name in ("Coup", "Assassinate"):
            if self.card_name_to_lose:
                return
            else:
                self.player2 = self.player(self.player_id_to_lose_influence)

        if self.current_action.name == "Accept_block":
            h1 = History_action(
                self.player(self.blocking_player),
                self.player2,
                self.current_action,
            )
        else:
            h1 = History_action(
                self.player(self.current_action_player_id),
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
        if (
            self.player(self.user_id).coins >= COUP_REQUIRED
            and "Block" not in self.current_action.name
        ):
            self.player(self.user_id).set_player_alert("You must coup")
            return -1
        if self.player(self.user_id).coins >= self.current_action.coins_required:
            return 0  # not enough coins
        if self.player(self.user_id).coins < self.current_action.coins_required:
            return 1  # enough coins

        return 0

    def clear_all_player_alerts(self):
        for player in self.players.values():
            player.clear_player_alert()

    def clear_game_alerts(self):
        self.game_alert = ""

    def player_id_from_index(self, index: int) -> str:
        for i, player in enumerate(self.players):
            if i == index:
                return self.players[player].id
        return ""

    def reverse_last_action(self):
        if not self.action_history:
            return
        prior_action = self.action_history[-2].action.name

        if prior_action == "Foreign_aid":
            player1 = self.action_history[-2].player1
            player1.add_remove_coins(-2)

        if prior_action == "Steal":
            player1 = self.action_history[-2].player1
            player2 = self.action_history[-2].player2
            player1.add_remove_coins(-2)
            player2.add_remove_coins(2)  # type: ignore

        if prior_action == "Assassinate":
            self.assassinate_in_progress = False

    def reverse_last_action_challenge(self):
        if not self.action_history:
            return
        prior_action = self.action_history[-1].action.name

        if prior_action == "Foreign_aid":
            player1 = self.action_history[-1].player1
            player1.add_remove_coins(-1)

        if prior_action == "Assassinate":
            self.assassinate_in_progress = False
            player1 = self.action_history[-1].player1
            player1.add_remove_coins(3)

        if prior_action == "Take_3_coins":
            player1 = self.action_history[-1].player1
            player1.add_remove_coins(-3)

        if prior_action == "Steal":
            self.player1 = self.action_history[-1].player1
            self.player2 = self.action_history[-1].player2
            self.player1.add_remove_coins(-2)
            self.player2.add_remove_coins(2)  # type: ignore

        if prior_action == "Exchange":
            player1 = self.action_history[-1].player1
            cards_to_discard = player1.hand.copy()
            for card in cards_to_discard:
                if card.card_status == "down":
                    player1.discard([card.value], self.deck)
            player1.hand = player1.cards_prior_to_exchange
            self.exchange_in_progress = False

    def challenge_successful(self) -> bool:
        if not self.action_history:
            return True
        prior_action = self.action_history[-1].action
        prior_action_player1 = self.action_history[-1].player1
        if prior_action.name == "Block":  # Challenging a block
            action_name_to_check = "Block_" + self.action_history[-2].action.name
        else:
            action_name_to_check = prior_action.name
        if prior_action.name in ("Exchange"):
            check_prior = True
        else:
            check_prior = False

        self.required_card = prior_action_player1.check_card_in_hand(
            REQUIRED_CARD[action_name_to_check], check_prior
        )
        if self.required_card:
            return False
        else:
            return True
        if prior_action_player1.check_card_in_hand(
            REQUIRED_CARD[prior_action.name], check_prior
        ):
            self.required_card = REQUIRED_CARD[prior_action.name]
            return False
        return True

    def next_user_id(self):
        self.last_user_id_assigned += 1
        return self.last_user_id_assigned


class History_action:
    def __init__(self, player1, player2, action):
        self.player1: Player = player1
        self.player2: Player | None = player2
        self.action = action
        self.time_added = datetime.now()
        if not self.player2:
            self.player2 = None


def main():
    ids = [("1", "Lee"), ("2", "Adina")]
    game = Game()
    for player_id, player_name in ids:
        game.players[player_id] = Player(player_id, player_name)
    game.wait()
    print(game.actions)
    game.start()
    print(game.actions)
    game.user_id = "1"
    print(game.whose_turn())
    print(game.player_id("1"))
    game.current_player_index = 1
    print(game.your_turn())
    print(game.whose_turn_name())
    game.process_action(Action("Exchange", 0, "enabled", False), "1")
    cards = ["contessa", "ambassador"]
    game.set_cards_to_exchange(cards)
    game.process_action(Action("Exchange", 0, "enabled", False), "1")
    print(game.action_history)


if __name__ == "__main__":
    main()
