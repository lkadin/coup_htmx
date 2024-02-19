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

    def draw(self, deck):
        self.hand.append(deck.draw())

    def play_card(self) -> list[str]:
        return self.hand.pop()

    def add_remove_coins(self, num_of_coins: int):
        self.coins += num_of_coins

    def __repr__(self) -> str:
        return self.id + "-" + " ".join(self.hand) + f"{self.coins=}"


class Action:
    def __init__(self, name, coins_required: int) -> None:
        self.name = name
        self.coins_required = coins_required


class Game:
    def __init__(self, player_ids: list[tuple]) -> None:
        self.player_ids = player_ids
        self.players = {}
        self.NUM_OF_CARDS = 2
        self.status = "Not started"
        self.deck = Deck()
        self.deck.shuffle()
        self.add_all_players()
        self.initial_deal()
        self.actions = []
        self.add_all_actions()

    def initial_deal(self):
        for _ in range(self.NUM_OF_CARDS):
            for player in self.players.values():
                player.draw(self.deck)

    def add_all_players(self):
        for player_id, player_name in self.player_ids:
            self.players[player_id] = Player(player_id, player_name)
        random.shuffle(self.player_ids)
        self.current_player_index = 0

    def next_turn(self):
        self.current_player_index += 1
        if self.current_player_index > 3:
            self.current_player_index

    def whose_turn(self):
        return self.current_player_index

    def whose_turn_name(self):
        return self.player_ids[self.current_player_index][1]

    def add_all_actions(self):
        for name, number_of_coins in [
            ("Assassinate", 3),
            ("Coup", 7),
            ("Steal", 0),
            ("Take 3 coins", 0),
            ("Foreign aid", 0),
            ("Income", 0),
        ]:
            self.actions.append(Action(name, number_of_coins))

    def play(self):
        self.staus = "In progress"


def main():
    ids = [("1", "Lee"), ("2", "Adina"), ("3", "Joey"), ("9", "Jamie")]
    game = Game(ids)
    game.play()


if __name__ == "__main__":
    main()
