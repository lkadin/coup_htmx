class Content:
    def __init__(self, player_ids, user_id) -> None:
        self.player_ids = player_ids
        self.user_id = user_id

    def content_generic(self, user_id):
        self.table = """
            <div hx-swap-oob="innerHTML:#photo">
            <table style='border-collapse: collapse;'>
            <col width="40%">
            <col width="40%">
            <tr>
            """
        for player_id in self.player_ids:
            self.table += f"""
            <td>
            <p style=text-align:top;><strong>{player_id}</strong> has 2 coins</p>
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
        return self.content_generic(self)
