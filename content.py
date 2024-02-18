class Content:
    def __init__(self, game, user_id) -> None:
        self.game = game
        self.players = game.players
        self.user_id = user_id

    def show_table(self):
        self.table = """
            """
        for player in self.players.values():
            self.table += f"""
            <div hx-swap-oob="innerHTML:#photo">
            <p style=text-align:top;><strong>{player.name}</strong> coins -  {player.coins}</p>
            """
            for card in player.hand:
                self.table += f"""
                <img src='/static/jpg/{card}.jpg' {card} style=opacity:1.0;>
                """
        self.table += """    
            </div>
            """
        return self.table

    def whose_turn(self):
        self.table = f"""
        <div hx-swap-oob="innerHTML:#user{self.user_id}">
        <p style=text-align:top;><strong>{self.game.whose_turn_name()} it's your turn</strong> </p>
        """
        return self.table
