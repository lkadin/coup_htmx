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
    def __init__(self, id: str) -> None:
        self.id = id
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
    def __init__(self, player_ids: list) -> None:
        self.player_ids = player_ids
        self.players = {}
        self.NUM_OF_CARDS = 2
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
        for player_id in self.player_ids:
            self.players[player_id] = Player(player_id)
        random.shuffle(self.player_ids)
        self.current_player_index = 0

    def next_turn(self):
        self.current_player_index += 1
        if self.current_player_index > 3:
            self.current_player_index

    def whose_turn(self):
        return self.current_player_index

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
        pass


def main():
    game = Game(["1", "2", "3", "4"])
    game.play()


if __name__ == "__main__":
    main()
