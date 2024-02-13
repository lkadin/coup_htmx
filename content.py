class Content:
    def __init__(self, player_ids, user_id) -> None:
        self.player_ids = player_ids
        self.user_id = user_id

    def content1(self):
        pass

    def content2(self):
        self.table = """
                <div hx-swap-oob="innerHTML:#photo">
                <table style='border-collapse: collapse;'>
                <col width="40%">
                <col width="40%">
                <tr>
                    <td>
                        <img src="/static/jpg/down.png">
                    </td>
                    <td>
                        <img src="/static/jpg/down.png">
                    </td>
                </tr>
                <tr>
                    <td><br><br></td>
                </tr>
                <tr>
                    
                </tr>
                </table>
                </div>
            """
        return self.table

    def content3(self):
        return """
            <div hx-swap-oob="innerHTML:#photo">
            <img src="/static/jpg/duke.JPG" alt="duke">
            </div>
            """

    def content9(self):
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
        print(self.table)
        return self.table

    def html(self):
        # print(f"{self.player_ids=}")
        # print(f"Content for - {self.user_id}")
        if self.user_id == "1":
            return self.content1()
        if self.user_id == "2":
            return self.content2()
        if self.user_id == "3":
            return self.content3()
        if self.user_id == "9":
            return self.content9()
