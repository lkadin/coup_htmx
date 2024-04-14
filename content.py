class Content:
    def __init__(self, game, user_id: str) -> None:
        self.game = game
        self.players = self.game.players
        self.user_id = user_id
        self.history: str = ""
        self.actions: str = ""

    def show_hand(self, player):
        def non_exchange(card):
            if (
                player.name == self.players[self.user_id].name
                and card.card_status == "down"
            ):
                self.display_hand += f"""
                <img src='/static/jpg/{card.value}.jpg' {card.value} style=opacity:1.0;>
                """
            else:
                if card.card_status == "down":
                    self.display_hand += f"""
                    <img src='/static/jpg/down.png' {card.value} style=opacity:1.0;>
                    """
                else:
                    self.display_hand += f"""
                    <img src='/static/jpg/{card.value}.jpg' {card.value} style=opacity:.5;>
                    """

        def coup(card):
            if (
                self.user_id == self.game.player_to_coup
                and player.name == self.players[self.user_id].name
            ):
                self.display_hand += f"""
                <input type="checkbox" name="cardnames" value="{card.value}" <td><img src="/static/jpg/{card.value}.jpg" height="350">
                """
            else:
                self.display_hand += f"""
                <img src='/static/jpg/down.png' {card.value} style=opacity:1.0;>
                """

        def exchange(card):
            if player.name == self.players[self.user_id].name:
                self.display_hand += f"""
                <input type="checkbox" name="cardnames" value="{card.value}" <td><img src="/static/jpg/{card.value}.jpg" height="350">
                """
            else:
                self.display_hand += f"""
                <img src='/static/jpg/down.png' {card.value} style=opacity:1.0;>
                """

        if (
            self.game.exchange_in_progress
            and player.name == self.players[self.user_id].name
        ):
            self.display_hand = '<form hx-ws="send" hx-target="cards">'
        elif self.game.coup_in_progress and self.user_id == self.game.player_to_coup:
            self.display_hand = '<form hx-ws="send" hx-target="cards">'
        else:
            self.display_hand = ""
        for card in player.hand:
            if (self.game.exchange_in_progress) and self.game.your_turn(self.user_id):
                exchange(card)
            elif (
                self.game.coup_in_progress and self.user_id == self.game.player_to_coup
            ):
                coup(card)
            else:
                non_exchange(card)
        if (
            self.game.exchange_in_progress
            and player.name == self.players[self.user_id].name
            and self.game.your_turn(self.user_id)
        ):
            self.display_hand += """
                <p> Which card(s) do you want to discard?</p>
                <input type="submit" id="test" value="Submit">
                </form>
                """
        elif (
            self.game.coup_in_progress
            and self.user_id == self.game.player_to_coup
            and player.name == self.players[self.user_id].name
        ):
            self.display_hand += """
                <p> Which card do you want to discard?</p>
                <input type="submit" id="test" value="Submit">
                </form>
                """
        self.display_hand += "</a>"
        return self.display_hand

    def show_table(self):
        self.table = """
            <div hx-swap-oob="innerHTML:#cards">
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

    def show_game_status(self):
        self.game_status = f"""
            <div hx-swap-oob="innerHTML:#game_status">
            <h4>{self.game.players[self.user_id].name} - {self.game.game_status}</h4>
            </div>
            """
        return self.game_status

    def show_history(self, message: str) -> str:
        self.history = f"""
        <br>
        <div hx-swap-oob="innerHTML:#history">
        {self.game.action_history}
        <br>
        </div>

        """
        return self.history

    def delete_start_action(self):
        self.actions += f"""
                <div id="Start">
                <form hx-ws="send" hx-target="#actions">
                <input type="hidden" name="user_name" value={self.user_id}>
                <input type="hidden" name="message_txt" value=Start>
                <input type="submit" value="Start" hidden>
                </form>
                </div>
                """
        return self.actions

    def show_actions(self):
        start = False
        self.actions = ""
        for action in self.game.actions:
            if action.name == "Start":
                start = True
            visible = ""
            if action.action_status == "disabled":
                visible = "hidden"
            self.actions += f"""
                <div id="{action}">
                <form hx-ws="send" hx-target="#actions">
                <input type="hidden" name="user_name" value={self.user_id}>
                <input type="hidden" name="message_txt" value={action}>
                <input type="submit" value={action} {action.action_status} {visible}>
                </form>
                </div>
            """
        self.actions += "<br>"
        if not start:
            self.actions += self.delete_start_action()
        return self.actions

    def pick_second_player(self):
        self.show_other_players = """
            <div id="second_player" >
            <br>
                <form hx-ws="send" hx-target="#second_player" >
                <label for="player">Pick a player</label>
                <select name="player" id="player">
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

    def hide_second_player(self):
        self.hide_other_players = """
            <div id="second_player" hidden >
            """
        return self.hide_other_players
