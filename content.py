class Content:
    def __init__(self, game, user_id) -> None:
        self.players = game.players
        self.user_id = user_id

    def content_generic(self):
        self.table = """
            <div hx-swap-oob="innerHTML:#photo">
            """
        for player in self.players.values():
            self.table += f"""
            <p style=text-align:top;><strong>{player.id}</strong> has 2 coins</p>
            """
            for card in player.hand:
                self.table += f"""
                <img src='/static/jpg/{card}.jpg' {card} style=opacity:0.4;>
                """
        self.table += """    
            </div>
            """
        return self.table

    def html(self):
        return self.content_generic()
