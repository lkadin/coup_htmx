actions_text = {
    "Assassinate": "Pay 3 coins, choose player to lose card. (Can be blocked by Contessa.)",
    "Coup": "Pay 7 Coins, choose player to lose card. (Cannot be blocked or challenged.)",
    "Steal": "Take 2 coins from another player. (Can be blocked by Captain or Ambassador.) ",
    "Take_3_coins": "Take 3 Coins. (Cannot be blocked)",
    "Foreign_aid": "Take 2 coins. (Cannot be challenged. Can be blocked by player claiming duke)",
    "Income": "Take 1 coin. (Cannot be blocked or challenged.)",
    "Exchange": "Take 2 cards, return 2 back to deck. (Cannot be blocked.)",
    "Block": "Block foreign aid, stealing, or assasination (Check card to see which you can do.)",
    "Challenge": "Challenge at any turn that allows challenges.",
    "Accept_Block": "Accept a block without a challange.",
    "Restart": "RESTART: New game.",
}


# <p><b>ASSASSINATE</b>: Pay 3 coins, choose player to lose card. <br><i>Can be blocked by Contessa.</i></p>
# <p><b>COUP</b>: Pay 7 Coins, choose player to lose card. <br><i>Can be blocked or challenged.</i><p>
# <p><b>STEAL</b>: Take 2 coins from another player. <br><i>Can be blocked by Captain or Ambassador.</i><p>
# <p><b>TAX</b>: Take 3 Coins. <br><i>Cannot be blocked</i><p>
# <p><b>FOREIGN AID</b>: Take 2 coins. <br><i>Cannot be challenged. Can be blocked by player claiming duke</i><p>
# <p><b>INCOME</b>: Take 1 coin. <br><i>Cannot be blocked or challenged.</i><p>
# <p><b>EXCHANGE</b>: Take 2 cards, return 2 back to deck. <br><i>Cannot be blocked.</i><p>
# <p><b>BLOCK</b>: Block foreign aid, stealing, or assasination <br><i>Check card to see which you can do.</i><p>
# <p><b>CHALLENGE</b>: Challenge at any turn that allows challenges.<p>
# <p><b>ACCEPT BLOCK</b>: Accept a block without a challange.<p>
# <p><b>RESTART</b>: New game.</p>


# <div id="notifications" class="col-4">
#     <!-- <div id="game_status">
#         <h4>Lee - In progress</h4>
#     </div> -->
#     <div id="turn">
#         <h4>Jamie</h4>
#     </div>
#     <br><br>
#     <p id="user1"></p>


#     <div class="mb-2" id="Assassinate">
#         <form hx-ws="send" hx-target="#actions">
#             <input type="hidden" name="user_name" value="1">
#             <input type="hidden" name="message_txt" value="Assassinate">
#             <input type="submit" value="ASSASSINATE" enabled="">
#         </form>
#     <div></div></div>
#     <p>Pay 3 coins, choose player to lose card. (Can be blocked by Contessa.)</p>

#     <div class="mb-2" id="Coup">
#         <form hx-ws="send" hx-target="#actions">
#             <input type="hidden" name="user_name" value="1">
#             <input type="hidden" name="message_txt" value="Coup">
#             <input type="submit" value="COUP" enabled="">
#         </form>
#     </div>
#     <p>Pay 7 Coins, choose player to lose card. (Cannot be blocked or challenged.)</p>

#     <div class="mb-2" id="Steal">
#         <form hx-ws="send" hx-target="#actions">
#             <input type="hidden" name="user_name" value="1">
#             <input type="hidden" name="message_txt" value="Steal">
#             <input type="submit" value="STEAL" enabled="">
#         </form>
#     </div>
#     <p>Take 2 coins from another player. (Can be blocked by Captain or Ambassador.)</p>

#     <div class="mb-2" id="Take_3_coins">
#         <form hx-ws="send" hx-target="#actions">
#             <input type="hidden" name="user_name" value="1">
#             <input type="hidden" name="message_txt" value="Take_3_coins">
#             <input type="submit" value="TAX" enabled="">
#         </form>
#     </div>
#     <p>Take 3 Coins. (Cannot be blocked)</p>

#     <div class="mb-2" id="Foreign_aid">
#         <form hx-ws="send" hx-target="#actions">
#             <input type="hidden" name="user_name" value="1">
#             <input type="hidden" name="message_txt" value="Foreign_aid">
#             <input type="submit" value="FOREIGN AID" enabled="">
#         </form>
#     </div>
#     <p>Take 2 coins. (Cannot be challenged. Can be blocked by player claiming duke)</p>

#     <div class="mb-2" id="Income">
#         <form hx-ws="send" hx-target="#actions">
#             <input type="hidden" name="user_name" value="1">
#             <input type="hidden" name="message_txt" value="Income">
#             <input type="submit" value="INCOME" enabled="">
#         </form>
#     </div>

#     <p>Take 1 coin. (Cannot be blocked or challenged.)</p>
#     <div class="mb-2" id="Exchange">
#         <form hx-ws="send" hx-target="#actions">
#             <input type="hidden" name="user_name" value="1">
#             <input type="hidden" name="message_txt" value="Exchange">
#             <input type="submit" value="EXCHANGE" enabled="">
#         </form>
#     </div>
#     <p>Take 2 cards, return 2 back to deck. (Cannot be blocked.)</p>

#     <div class="mb-2" id="Block">
#         <form hx-ws="send" hx-target="#actions">
#             <input type="hidden" name="user_name" value="1">
#             <input type="hidden" name="message_txt" value="Block">
#             <input type="submit" value="BLOCK" enabled="">
#         </form>
#     </div>

#     <p>Block foreign aid, stealing, or assasination (Check card to see which you can do.)</p>
#     <div class="mb-2" id="Challenge">
#         <form hx-ws="send" hx-target="#actions">
#             <input type="hidden" name="user_name" value="1">
#             <input type="hidden" name="message_txt" value="Challenge">
#             <input type="submit" value="CHALLENGE" enabled="">
#         </form>
#     </div>

#     <p>Challenge at any turn that allows challenges.</p>
#     <div class="mb-2" id="Accept_Block">
#         <form hx-ws="send" hx-target="#actions">
#             <input type="hidden" name="user_name" value="1">
#             <input type="hidden" name="message_txt" value="Accept_Block">
#             <input type="submit" value="ACCEPT BLOCK" enabled="">
#         </form>
#     </div>

#     <p> Accept a block without a challange.</p>


#     <div class="mb-2" id="Restart">
#         <form hx-ws="send" hx-target="#actions">
#             <input type="hidden" name="user_name" value="1">
#             <input type="hidden" name="message_txt" value="Restart">
#             <input type="submit" value="RESTART" disabled="" hidden="">
#         </form>
#     </div>
#     <p>New game.</p>
#     <br>
#                 <div id="history" class="overflow-auto ">

# </div>
# <br>
#                 <div id="second_player">
#     <br>
#     <form hx-ws="send" hx-target="#second_player" hidden="">
#         <label for="player">Pick a player</label>
#         <select name="player" id="player">
#             <option value="Lee">Lee</option>
#             <option value="Adina">Adina</option>
#         </select>
#         <input type="submit" value="Submit">
#     </form>
#     <br>
# </div>
# </div>

# Duke: Take three coins from the treasury. Block someone from taking foreign aid.
# Assassin: Pay three coins and try to assassinate another player's character.
# Contessa: Block an assassination attempt against yourself.
# Captain: Take two coins from another player, or block someone from stealing coins from you.
# Ambassador: Draw two character cards from the Court (the deck), choose which (if any) to exchange with your
# face-down
# characters, then return two. Block someone from stealing coins from you.
