#!/usr/local/bin/python3

from cgitb import enable
enable()
from html import escape
from cgi import FieldStorage
import pymysql as db



print("Content-Type: text/html")
print()

checkBox=""
goalkeeper=""
defender=""
midfielder=""
forward=""
formData=FieldStorage()
defe=""
goalK=""
midF=""
forW=""

def transfer_Function(username, playerList, limit):
    if len(playerList)>0 and len(playerList)<=limit:
        for player in playerList:
            #making sure user does not get more than the max amount of players in that position
            cursor.execute("SELECT * FROM PLAYERSWD2 WHERE playingPosition='goalkeeper' and playerteam=%s", (username))
            if not cursor.rowcount>=limit:
                cursor.execute("SELECT * FROM PLAYERSWD2 WHERE name=%s", (player))
                if cursor.rowcount>0:
                    cursor.execute("SELECT * FROM PLAYERSWD2 WHERE name=%s", (player))
                    playerClub = cursor.fetchone()
                    cursor.execute("SELECT * FROM PLAYERSWD2 WHERE club=%s and playerteam=%s", (playerClub["club"], username))
                    if cursor.rowcount < 6:
                        #checking if player is not in users team
                        cursor.execute("SELECT * FROM PLAYERSWD2 WHERE name=%s", (player))
                        check=cursor.fetchone()
                        if check["playerteam"]!="None" and check["playerteam"]!=username:
                            #updating data to make player part of users team and budget is updated
                            cursor.execute("SELECT * FROM PLAYERSWD2 WHERE name=%s", (player))
                            check1=cursor.fetchone()
                            cursor.execute("SELECT * FROM FANTASYPLAYERS WHERE username=%s", (username))
                            check2=cursor.fetchone()
                            balanceCheck=int(check2["budget"])-int(check1["value"])
                            if balanceCheck>0:
                                cursor.execute("UPDATE PLAYERSWD2 SET playerteam=%s WHERE name=%s", (username, player))
                                connection.commit()
                                cursor.execute("SELECT * FROM PLAYERSWD2 WHERE name=%s", (player))
                                goalkeeperValue=cursor.fetchone()
                                cursor.execute("UPDATE FANTASYPLAYERS SET budget=budget-%s WHERE username=%s", (goalkeeperValue["value"], username))
                                connection.commit()

                            else:
                                return "<p>You do not have enough money in your budget, check if your team</p>"
                        else:
                            return "<p>A player you selected either belongs to your team or has not been selected for a team</p>"
                    else:
                        return "<p>You have reached the limit of players from the same club! Check your team!</p>"
                else:
                    return "<p>That player is not in our database!</p>"
            else:
                return "<p>You can't have more than the limit of players in that position! Check youir team!</p>"
    else:
        return "<p>You have selected more than the limit!</p>"

    return "<p>Transfer(s) Complete! Check your team!</p>"

try:
    connection=db.connect('localhost', 'dgjm1', 'ahgha', 'cs1021_cs5021_dgjm1')
    cursor=connection.cursor(db.cursors.DictCursor)

    if len(formData)!=0:
        username=escape(formData.getfirst("user", "").strip())
        if username:
            #checking if username is in database
            cursor.execute("SELECT * FROM FANTASYPLAYERS WHERE username=%s", (username))
            if cursor.rowcount>0:
                #check if username matches the one logged in

                            cursor.execute("SELECT * FROM PLAYERSWD2 WHERE playerteam=%s", (username))
                            if cursor.rowcount<15:
                                goalkeepers=formData.getlist("goalkeeper")
                                defenders=formData.getlist("defender")
                                midfielders=formData.getlist("midfielder")
                                forwards=formData.getlist("forward")
                                if len(goalkeepers)>0:
                                    goalK = transfer_Function(username, goalkeepers, 2)
                                if len(defenders)>0:
                                    defe = transfer_Function(username, defenders, 5)
                                if len(midfielders)>0:
                                    midF = transfer_Function(username, midfielders, 5)
                                if len(forwards)>0:
                                    forW = transfer_Function(username, forwards, 3)
                            else:
                                checkBox="<p>You Have 15 players, let one go first!</p>"

        else:
            checkBox="<p>Please enter a username!</p>"

    #putting out list of players
    cursor.execute("SELECT name, club, playingPosition FROM PLAYERSWD2 ORDER BY playingPosition")
    if cursor.rowcount == 0:
        checkBox="<p>Sorry. There are no players at present.</p>"
    else:
        cursor.execute("SELECT name, club, playingPosition, value, playerteam FROM PLAYERSWD2 WHERE playingPosition='goalkeeper' ORDER BY name")
        for row in cursor.fetchall():
            slicing=row["name"][:3]
            goalkeeper+="<label for='%s'>%s, Team: %s, Position: %s, Value: %s, User: %s</label><input type='checkbox' name='goalkeeper' value='%s' id='%s' />" % (slicing, row["name"], row["club"], row["playingPosition"], row["value"], row["playerteam"], row["name"], slicing)

        cursor.execute("SELECT name, club, playingPosition, value, playerteam FROM PLAYERSWD2 WHERE playingPosition='defender' ORDER BY name")
        for row in cursor.fetchall():
            if row["name"]=="David Luiz" or row["name"]=="Antonio Rudiger" or row["name"]=="Marcos Alonso"  or row["name"]=="Nicolas Otamendi":
                slicing1=row["name"][:3]+"1"
            else:
                slicing1=row["name"][:3]
            defender+="<label for='%s'>%s, Team: %s, Position: %s, value: %s, User: %s</label><input type='checkbox' name='defender' value='%s' id='%s' />" % (slicing1, row["name"], row["club"], row["playingPosition"], row["value"], row["playerteam"], row["name"], slicing1)

        cursor.execute("SELECT name, club, playingPosition, value, playerteam FROM PLAYERSWD2 WHERE playingPosition='midfielder' ORDER BY name")
        for row in cursor.fetchall():
            if row["name"]=="Dani Ceballos" or row["name"]=="Bernardo Silva" or row["name"]=="Mason Mount":
                slicing2=row["name"][:3]+"1"
            elif row["name"]=="David Silva":
                slicing2=row["name"][:3]+"2"
            else:
                slicing2=row["name"][:3]
            midfielder+="<label for='%s'>%s, Team: %s, Position: %s, value: %s, User: %s</label><input type='checkbox' name='midfielder' value='%s' id='%s' />" % (slicing2, row["name"], row["club"], row["playingPosition"], row["value"], row["playerteam"], row["name"], slicing2)

        cursor.execute("SELECT name, club, playingPosition, value, playerteam FROM PLAYERSWD2 WHERE playingPosition='forward' ORDER BY name")
        for row in cursor.fetchall():
            if row["name"]=="Sergio Aguero" or row["name"]=="Willian":
                slicing3=row["name"][:3]+"1"
            else:
                slicing3=row["name"][:3]
            forward+="<label for='%s'>%s, Team: %s, Position: %s, value: %s, User: %s</label><input type='checkbox' name='forward' value='%s' id='%s' />" % (slicing3, row["name"], row["club"], row["playingPosition"], row["value"], row["playerteam"], row["name"], slicing3)

    cursor.close()
    connection.close()


except db.Error:
    checkBox="<p>Sorry, we're experiencing problems at the moment. Please try again another time!</p>"





print("""
      <!DOCTYPE html>
      <html lang="en">
        <head>
          <title>Transfer Request</title>
          <meta charset="utf-8" />
          <link rel="stylesheet" href="index.css" />
        </head>
        <body>
          <header>
            <h1>
                Transfer Request
            </h1>
          </header>
          <main>
            <section class="links">
                <ul>
                    <li><a href="index.py">Home Page</a></li>
                    <li><a href="playerForm.py">Player List</a></li>
                    <li><a href="playerTeam.py">Your Team</a></li>
                    <li><a href="playerScore.py">Enter Your Players Performance Stats</a></li>
                    <li><a href="playerRelease.py">Release a Player</a></li>
                </ul>
            </section>

            <section>
                <h1>
                    Rules
                </h1>
                <section id="rules">
                    <section class="rules1">
                        <ul>
                            <li>In order to play, you must first register(don't worry, it's free!).</li>
                            <li>After creating your team, you'll be given &pound;100 million to spend on players!</li>
                            <li>You can only choose up to 15 players for your team.</li>
                            <li>You can't have more than 6 players from the same club</li>
                            <li>Once a player has been chosen no other fantasy football player can choose that player without asking for a transfer</li>
                            <li>To request a transfer, you must have less than 15 players in your team</li>
                            <li>If you have 15 players, you must first let go of at least one player</li>
                            <li>You will only be able to get players within your budget</li>
                            <li>Remember, letting players go does not mean you'll get your virtual money back</li>
                            <li>Check the bottom of the form to see if you have successfully made a transfer</li>
                        </ul>
                    </section>
                    <section class="rules1">
                        <h1>
                            Choosing Players
                        </h1>
                        <p>
                            Your 15 man squad must contain up to:
                        </p>
                        <ul>
                            <li>2 Goalkeepers</li>
                            <li>5 Defenders</li>
                            <li>5 Midfielders</li>
                            <li>3 Forwards</li>
                        </ul>
                    </section>
                </section>
            </section>
            <section>
                        <h1>
                            Football Players
                        </h1>

                            <section id="footballers">
                                <form action="practicePlayerTransfer.py" method="post">
                                    <fieldset class="footballers">


                                        %s


                                        %s


                                        %s


                                        %s
                                        <label for="user">Please enter your username</label>
                                        <input type="text" name="user" id="user" />
                                        <input type='reset' class='submit' />
                                        <input type='submit' class='submit' />

                                    </fieldset>



                                </form>
                            </section>
                            %s
                            %s
                            %s
                            %s
                            %s
                    </section>
          </main>
          <footer>
              <small>
                  Player names and clubs belong to their rightful owners and have only been used for educational purposes
              </small>
          </footer>
        </body>
      </html>

""" % (goalkeeper, defender, midfielder, forward, checkBox, goalK, defe, midF, forW))
