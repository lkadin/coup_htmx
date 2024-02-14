import random


class Card:
    def __init__(self, value) -> None:
        self, value = value


class Deck:
    def __init__(self) -> None:
        self.cards = []
        for value in ["Duke", "Assassin", "Ambassador", "Captain", "Contessa"]:
            for _ in range(3):
                self.cards.append(value)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def __repr__(self) -> str:
        return " ".join([self.card for self.card in self.cards])


class Player:
    def __init__(self, id) -> None:
        self.id = id
        self.hand = []
        self.coins = 2

    def draw(self, deck):
        self.hand.append(deck.draw())

    def play_card(self):
        return self.hand.pop()

    def __repr__(self) -> str:
        return self.id + "-" + " ".join(self.hand)


class Game:
    def __init__(self, player_ids) -> None:
        self.player_ids = player_ids
        self.players = {}
        self.NUM_OF_CARDS = 2
        self.deck = Deck()
        self.deck.shuffle()
        for player_id in self.player_ids:
            self.players[player_id] = Player(player_id)

        for _ in range(self.NUM_OF_CARDS):
            for player_id, player in self.players.items():
                player.draw(self.deck)

    def play(self):
        pass


def main():
    game = Game(["1", "2", "3", "4"])
    game.play()


if __name__ == "__main__":
    main()
