class Content:
    def __init__(self, game, user_id: str) -> None:
        self.game = game
        self.players = self.game.players
        self.user_id = user_id
        self.history: str = ""
        self.actions: str = ""

    def show_hand(self, player):
        card_width = 200

        def non_exchange(card):
            if (
                player.name == self.players[self.user_id].name
                and card.card_status == "down"
            ):
                self.display_hand += f"""
                <img src='/static/jpg/{card.value}.jpg' {card.value} style="opacity:1.0; width:{card_width}px;">
                """
            else:
                if card.card_status == "down":
                    self.display_hand += f"""
                    <img src='/static/jpg/down.png' {card.value} style="opacity:1.0; width:{card_width}px;">
                    """
                else:
                    self.display_hand += f"""
                    <img src='/static/jpg/{card.value}.jpg' {card.value} style="opacity:.5; width: {card_width}px;">
                    """

        def lose_influence(card, card_number):
            if (
                self.user_id == self.game.player_id_to_lose_influence
                and player.name == self.players[self.user_id].name
                and card.card_status == "down"
            ):
                self.display_hand += f"""
                <input type="checkbox" name="cardnames" value="{card.value}" id="{card_number}">
                <label for = "{card_number}">
                <img src="/static/jpg/{card.value}.jpg">
                </label>
                """
            else:
                if card.card_status == "down":
                    self.display_hand += f"""
                    <img src='/static/jpg/down.png' {card.value} style="opacity:1.0; width:{card_width}px;">
                    """
                else:
                    self.display_hand += f"""
                    <img src='/static/jpg/{card.value}.jpg' {card.value} style="opacity:0.5; width:{card_width}px;">
                    """

        def exchange(card, card_number):
            if (
                player.name == self.players[self.user_id].name
                and card.card_status == "down"
            ):
                self.display_hand += f"""
                <input type="checkbox" name="cardnames" value="{card.value}" id="{card_number}">
                <label for = "{card_number}">
                <img src="/static/jpg/{card.value}.jpg">
                </label>
                """
            else:
                if card.card_status == "down":
                    self.display_hand += f"""
                    <img src='/static/jpg/down.png' {card.value} ;">
                    """
                else:
                    self.display_hand += f"""
                    <img src='/static/jpg/{card.value}.jpg' {card.value} style="opacity:0.5; width:{card_width}px;">
                    """

        # exchange
        if self.game.exchange_in_progress and self.game.your_turn():
            self.display_hand = '<form hx-ws="send" hx-target="cards">'
            self.display_hand += '<div class="card-container">'
            for card_number, card in enumerate(player.hand):
                exchange(card, card_number)
            if player.name == self.players[self.user_id].name:
                self.display_hand += """
                </div>
                <p> Which cards do you want to discard?</p>
                <input type="submit" id="test" value="Submit">
                </form>
                """

        # lose influence - select card to lose
        elif (
            self.game.coup_assassinate_in_progress
            or self.game.lose_influence_in_progress
        ) and self.user_id == self.game.player_id_to_lose_influence:
            self.display_hand = '<div class="card-container">'
            self.display_hand += '<form hx-ws="send" hx-target="cards">'
            for card_number, card in enumerate(player.hand):
                lose_influence(card, card_number)
            if player.name == self.players[self.user_id].name:
                self.display_hand += """
                <p> Which card do you want to discard?</p>
                <input type="submit" id="test" value="Submit">
                </form>
                """
        else:
            self.display_hand = ""
            for card in player.hand:
                non_exchange(card)

        return self.display_hand

    def show_table(self):
        self.table = """
            <div hx-swap-oob="innerHTML:#cards">
            """
        # first show player = user_id
        player = self.game.player(self.user_id)
        self.show_player(player)
        for player in self.players.values():
            if player.id == self.user_id:
                continue
            self.show_player(player)
        self.table += """    
            </div>
            """
        return self.table

    def show_player(self, player):
        self.table += f"""
        <p style=text-align:top;><strong>{player.name}</strong> coins -  {player.coins}</p>
        """
        self.table += self.show_hand(player)

    def show_turn(self):
        if not self.game.whose_turn_name():
            return ""
        self.turn = f"""
            <div hx-swap-oob="innerHTML:#turn">
            <h4>{self.game.whose_turn_name()}'s Turn</h4>
            </div>
            """
        return self.turn

    def show_game_status(self):
        try:
            self.game_status = f"""
                <div hx-swap-oob="innerHTML:#game_status">
                <h4>{self.game.players[self.user_id].name} - {self.game.game_status}</h4>
                </div>
                """
            return self.game_status
        except KeyError:
            return ""

    def show_history(self, message: str) -> str:
        self.history = """
        <br>
        <div hx-swap-oob="innerHTML:#history">
        """
        for history_action in self.game.action_history[::-1]:
            player1_name = history_action.player1.name
            if not history_action.player2:
                player2_name = ""
            else:
                player2_name = history_action.player2.name
            self.history += f"""
            {player1_name} {history_action.action} {player2_name}
            <br>
            """
        self.history += """
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
        if self.game.check_coins(self.user_id) == 1:
            return ""
        if (
            self.game.player_index_to_id(self.game.whose_turn())
            != self.players[self.user_id].id
        ):
            return ""
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
            if not player.influence():
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

    def show_game_alert(self):
        self.game_alert = f"""
        <div hx-swap-oob="innerHTML:#game_alerts" visible>
        <h1 style="color: red;">{self.game.game_alert}</h1>
        </div>
        """
        return self.game_alert

    def show_player_alert(self, user_id):
        try:
            self.player_alert = f"""
            <div hx-swap-oob="innerHTML:#player_alerts" visible>
            <h1 style="color: red;">{self.game.player(user_id).player_alert}</h1>
            </div>
            """
            return self.player_alert
        except AttributeError:
            return ""
