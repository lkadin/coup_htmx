class Content:
    def __init__(self, game, user_id) -> None:
        self.game = game
        self.players = game.players
        self.user_id = user_id

    def content_generic(self):
        self.table = """
            """
        for player in self.players.values():
            self.table += f"""
            <div hx-swap-oob="innerHTML:#photo">
            <p style=text-align:top;><strong>Player {player.id}</strong> coins -  {player.coins}</p>
            """
            for card in player.hand:
                self.table += f"""
                <img src='/static/jpg/{card}.jpg' {card} style=opacity:0.4;>
                """
        self.table += """    
            </div>
            """
        return self.table

    def whose_turn(self):
        self.table = f"""
        <div hx-swap-oob="innerHTML:#user{self.user_id}">
        <p style=text-align:top;><strong>Player {self.game.whose_turn()} it's your turn</strong> </p>
        """
        return self.table

    def html(self):
        return self.content_generic()
