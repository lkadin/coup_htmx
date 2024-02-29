class Content:
    def __init__(self, game, user_id: str) -> None:
        self.game = game
        self.players = self.game.players
        self.user_id = user_id

    def show_hand(self, player):
        self.add_to_table = ""
        for card in player.hand:
            if player.name == self.players[self.user_id].name:
                self.add_to_table += f"""
                <img src='/static/jpg/{card}.jpg' {card} style=opacity:1.0;>
                """
            else:
                self.add_to_table += f"""
                <img src='/static/jpg/down.png' {card} style=opacity:1.0;>
                """
        return self.add_to_table

    def show_table(self):
        self.table = """
            <div hx-swap-oob="innerHTML:#photo">
            """
        for player in self.players.values():
            self.table += f"""
            <p style=text-align:top;><strong>{player.name}</strong> coins -  {player.coins}</p>
            """
            self.table += self.show_hand(player)
        self.table += self.show_actions()
        self.table += """    
            </div>
            """
        return self.table

    def show_turn(self):
        self.turn = f"""
        <div hx-swap-oob="innerHTML:#turn">
        <p style=text-align:top;><strong>{self.game.whose_turn_name()}'s turn</strong> </p>
        """
        return self.turn

    def show_actions(self):
        self.actions = """ <form hx-ws="send" hx-target="#notifications">"""
        for action in self.game.actions:
            self.actions += f"""
                    <br>
                    <input type="hidden" name="user_name" value={self.user_id}>
                    <input type="hidden" name="message_txt" value={action}>
                    <input type="submit" value={action}>
                    """

        self.actions += """
         </form>
                </div>
                """
        return self.actions

    def show_notification(self, message):
        self.show_notification = f"""
        <div hx-swap-oob="beforeend:#notifications">
        <p>{message}</p>
        </div>
        """
        return self.show_notification
