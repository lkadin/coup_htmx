class Content:
    def __init__(self, game, user_id) -> None:
        self.game = game
        self.players = game.players
        self.user_id = user_id

    def show_table(self):
        self.table = """
            <div hx-swap-oob="innerHTML:#photo">
            """
        for player in self.players.values():
            self.table += f"""
            <p style=text-align:top;><strong>{player.name}</strong> coins -  {player.coins}</p>
            """
            for card in player.hand:
                if player.name == self.players[self.user_id].name:
                    self.table += f"""
                    <img src='/static/jpg/{card}.jpg' {card} style=opacity:1.0;>
                    """
                else:
                    self.table += f"""
                    <img src='/static/jpg/down.png' {card} style=opacity:1.0;>
                    """
        self.table += """    
            </div>
            """
        return self.table

    def whose_turn(self):
        self.turn = f"""
        <div hx-swap-oob="innerHTML:#user{self.user_id}">
        <p style=text-align:top;><strong>{self.game.whose_turn_name()}'s turn</strong> </p>
        """
        return self.turn

    def not_your_turn(self, on_off):
        if on_off:
            self.turn = """
            <div hx-swap-oob="innerHTML:#turn">
           <p style=text-align:top;><strong>It's not your turn</strong> </p>
            """
        else:
            self.turn = """
            <div hx-swap-oob="innerHTML:#turn">
           <p style=text-align:top;><strong></strong> </p>
            """
        print(self.turn)
        return self.turn
