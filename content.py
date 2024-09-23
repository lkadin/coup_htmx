from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)
history_template = env.get_template("history.html")
turn_template = env.get_template("turn.html")
actions_template = env.get_template("actions.html")
player_alert_template = env.get_template("player_alerts.html")
game_alert_template = env.get_template("game_alerts.html")
second_player_template = env.get_template("second_player.html")


class Content:

    def __init__(self, game, user_id: str) -> None:
        self.game = game
        self.players = self.game.players
        self.user_id = user_id
        self.history: str = ""
        self.actions: str = ""

    def show_hand(self, player):
        card_width = 200

        def checkbox(card, card_number):
            return f"""
                <input type="checkbox" name="cardnames" value="{card.value}" id="{card_number}">
                <label for = "{card_number}">
                <img src="/static/jpg/{card.value}.jpg">
                </label>
                """

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
                self.display_hand += checkbox(card, card_number)
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
                self.display_hand += checkbox(card, card_number)
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
        return self.table

    def show_player(self, player):
        self.table += f"""
        <p style=text-align:top;><strong>{player.name}</strong> coins -  {player.coins}</p>
        """
        self.table += self.show_hand(player)

    def show_turn(self):
        suffix = self.game.get_suffix()
        output = turn_template.render(turn=self.game.whose_turn_name(), suffix=suffix)
        return output

    # def show_game_status(self):
    #     try:
    #         self.game_status = f"""
    #             <div hx-swap-oob="innerHTML:#game_status">
    #             <h4>{self.game.players[self.user_id].name} - {self.game.game_status}</h4>
    #             </div>
    #             """
    #         return self.game_status
    #     except KeyError:
    #         return ""

    def show_history(self) -> str:
        self.game.prep_history_list()
        output = history_template.render(history_list=self.game.history_list)
        return output

    def show_actions(self):
        output = actions_template.render(
            actions=self.game.actions, user_id=self.game.user_id
        )
        return output

    def pick_second_player(self):
        available_players = []
        if self.game.check_coins(self.user_id) == 1:
            return
        if (
            self.game.player_index_to_id(self.game.whose_turn())
            != self.players[self.user_id].id
        ):
            return
        for player in self.players.values():
            if player.id == self.user_id:
                continue
            if not player.influence():
                continue
            available_players.append(player.name)
        output = second_player_template.render(player_names=available_players)
        return output

    def hide_second_player(self):
        self.hide_other_players = """
            <div id="second_player" hidden >
            """
        return self.hide_other_players

    def show_game_alert(self):
        output = game_alert_template.render(game_alert=self.game.game_alert)
        return output

    def show_player_alert(self, user_id):
        output = player_alert_template.render(
            player_alert=self.game.player(user_id).player_alert
        )
        return output
