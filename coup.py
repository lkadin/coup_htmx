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
    def __init__(self, name) -> None:
        self.name = name
        self.hand = []

    def draw(self, deck):
        self.hand.append(deck.draw())

    def play_card(self):
        return self.hand.pop()

    def __repr__(self) -> str:
        return self.name


class Game:
    def __init__(self, players) -> None:
        self.players = []
        self.NUM_OF_CARDS = 2
        self.deck = Deck()
        self.deck.shuffle()
        self.player_ids = players
        for player in self.player_ids:
            self.add_player(Player(player))

        for _ in range(self.NUM_OF_CARDS):
            for player in self.players:
                player.draw(self.deck)

    def add_player(self, player):
        self.players.append(player)

    def play(self):
        pass

def main():
    game = Game(["1", "2", "3", "4"])
    game.play()


if __name__ == "__main__":
    main()
