class Content:
    def __init__(self, game) -> None:
        self.players = game.players

    def content_generic(self):
        self.table = """
            <div hx-swap-oob="innerHTML:#photo">
            <table style='border-collapse: collapse;'>
            <col width="40%">
            <col width="40%">
            <tr>
            """
        for id, player in self.players.items():
            print(player, id)
            self.table += f"""
            <td>
            <p style=text-align:top;><strong>{player.id}</strong> has 2 coins</p>
            """
            for card in range(2):
                self.table += """
                <img src='/static/jpg/down.png' {card} style=opacity:0.4;>
                """
            self.table += """
            </td>
            </tr>
            """
        self.table += """    
            <tr>
            <td><br><br></td>
            </tr>
            <tr>
            </tr>
            </table>
            </div>
            """
        return self.table

    def html(self):
        return self.content_generic()
