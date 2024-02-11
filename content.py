class Content:
    def __init__(self, player) -> None:
        self.player = player

    def html(self):
        print(self.player)
        content = """
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
        return content
