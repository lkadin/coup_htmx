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
        self.table += """    
            </div>
            """
        return self.table

    def show_turn(self):
        self.turn = f"""
            <div hx-swap-oob="innerHTML:#turn">
            <h4>{self.game.whose_turn_name()}'s Turn</h4>
            </div>
            """
        return self.turn

    def show_notification(self, message):
        self.show_notification = f"""
        <br>
        <div hx-swap-oob="beforeend:#history">
        {message}
        <br>
        </div>

        """
        return self.show_notification

    def delete_start_action(self):
        self.show_actions += f"""
                <div id="Start">
                <form hx-ws="send" hx-target="#actions">
                <input type="hidden" name="user_name" value={self.user_id}>
                <input type="hidden" name="message_txt" value=Start>
                <input type="submit" value="Start" hidden>
                </form>
                </div>
                """
        return self.show_actions

    def show_actions(self):
        start = False
        self.show_actions = ""
        for action in self.game.actions:
            if action.name == "Start":
                start = True
            visible = ""
            if action.status == "disabled":
                visible = "hidden"
            self.show_actions += f"""
                <div id="{action}">
                <form hx-ws="send" hx-target="#actions">
                <input type="hidden" name="user_name" value={self.user_id}>
                <input type="hidden" name="message_txt" value={action}>
                <input type="submit" value={action} {action.status} {visible}>
                </form>
                </div>
            """
        self.show_actions += "<br>"
        if not start:
            self.show_actions += self.delete_start_action()
        return self.show_actions

    def pick_second_player(self):
        self.show_other_players = """
            <div id="second_player" >
            <br>
                <form hx-ws="send" hx-target="#second_player" >
                <label for="players">Pick a player</label>
                <select name="players id="player">
             """
        for player in self.players.values():
            if player.id == self.user_id:
                continue
            self.show_other_players += f"""
                <option value="{player.name}">{player.name}</option>
                """
        self.show_other_players += """
            </select>
            <input type="submit" value="Submit">
            <br>
            </div>
            """
        return self.show_other_players
