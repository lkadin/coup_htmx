from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)
history_template = env.get_template("history.html")
turn_template = env.get_template("turn.html")
actions_template = env.get_template("actions.html")
player_alert_template = env.get_template("player_alerts.html")
game_alert_template = env.get_template("game_alerts.html")
second_player_template = env.get_template("second_player.html")
card_template = env.get_template("cards.html")


class Content:

    def __init__(self, game, user_id: str) -> None:
        self.game = game
        self.players = self.game.players
        self.user_id = user_id
        self.history: str = ""
        self.actions: str = ""

    def show_hand(self, player):
        self.checkbox_required = False
        self.discard_prompt = False

        def non_exchange(card):
            card.opacity = 1.0
            card.display = card.value
            if (
                player.name != self.players[self.user_id].name
                and card.card_status == "down"
            ):
                card.display = "down"
            elif card.card_status == "up":
                card.opacity = 0.5
                card.card_number = "X"

        def lose_influence(card):
            card.display = card.value
            if (
                self.user_id == self.game.player_id_to_lose_influence
                and player.name == self.players[self.user_id].name
                and card.card_status == "down"
            ):
                card.display = card.value
                self.checkbox_required = True
            else:
                if card.card_status == "down":
                    card.display = "down"

        def exchange(card):
            card.display = card.value
            if (
                player.name == self.players[self.user_id].name
                and card.card_status == "down"
            ):
                card.display = card.value
                self.checkbox_required = True
            else:
                if card.card_status == "down":
                    card.display = "down"

        # exchange
        if self.game.exchange_in_progress and self.game.your_turn():
            self.display_cards = []
            for card_number, card in enumerate(player.hand):
                if card.card_status == "down":
                    card.card_number = card_number
                exchange(card)
                self.display_cards.append(card)
            if player.name == self.players[self.user_id].name:
                self.discard_prompt = True
                self.checkbox_required = True

        # lose influence - select card to lose
        elif (
            self.game.coup_assassinate_in_progress
            or self.game.lose_influence_in_progress
        ) and self.user_id == self.game.player_id_to_lose_influence:
            self.display_cards = []
            for card_number, card in enumerate(player.hand):
                if card.card_status == "down":
                    card.card_number = card_number
                lose_influence(card)
                self.display_cards.append(card)
            if player.name == self.players[self.user_id].name:
                self.discard_prompt = True
        else:  # non-exchange
            self.display_cards = []
            try:
                for card in player.hand:
                    non_exchange(card)
                    self.display_cards.append(card)
            except AttributeError:
                pass

        keep_discard = "Keep" if self.game.keep_cards else "discard"
        output = card_template.render(
            cards=self.display_cards,
            checkbox_required=self.checkbox_required,
            discard_prompt=self.discard_prompt,
            player=player,
            keep_discard=keep_discard,
        )
        return output

    def show_table(self):
        self.table = """
            <div hx-swap-oob="innerHTML:#table">
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
        self.table += self.show_hand(player)

    def show_turn(self):
        suffix = self.game.get_suffix()
        output = turn_template.render(turn=self.game.whose_turn_name(), suffix=suffix)
        return output

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
        output = second_player_template.render(
            player_names=available_players, second_player_visible="visible"
        )
        return output

    def hide_second_player(self):
        output = second_player_template.render(
            player_names=[], second_player_visible="hidden"
        )
        return output

    def show_game_alert(self):
        output = game_alert_template.render(game_alert=self.game.game_alert)
        return output

    def show_player_alert(self, user_id):
        try:
            output = player_alert_template.render(
                player_alert=self.game.player(user_id).player_alert
            )
        except AttributeError:
            output = player_alert_template.render(player_alert="")
        return output
