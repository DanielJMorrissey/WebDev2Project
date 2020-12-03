#!/usr/local/bin/python3

from cgitb import enable
enable()
from html import escape
import pymysql as db
from cgi import FieldStorage


print("Content-Type: text/html")
print()
formData=FieldStorage()

checkboxPlayers = ""
goalkeeper = ""
defender = ""
midfielder = ""
forward = ""
username = ""
resultGK = ""
resultDef = ""
resultMF = ""
resultFor = ""

def add_To_Team(username, playerList, limit):
    if len(playerList)<=limit and len(playerList)>0:
        for player in playerList:
            cursor.execute("SELECT * FROM PLAYERSWD2 WHERE name=%s", (player))
            if cursor.rowcount>0:
                cursor.execute("SELECT * FROM PLAYERSWD2 WHERE name=%s", (player))
                playerPosition = cursor.fetchone()
                cursor.execute("SELECT * FROM PLAYERSWD2 WHERE playerteam=%s and playingPosition=%s", (username, playerPosition["playingPosition"]))
                if not cursor.rowcount>=limit:
                    cursor.execute("SELECT * FROM PLAYERSWD2 WHERE name=%s", (player))
                    playerClub = cursor.fetchone()
                    cursor.execute("SELECT * FROM PLAYERSWD2 WHERE club=%s and playerteam=%s", (playerClub["club"], username))
                    if cursor.rowcount < 6:
                        #checking if player can be added to the team (when playerteam=="None")
                        cursor.execute("SELECT * FROM PLAYERSWD2 WHERE name=%s", (player))
                        check=cursor.fetchone()
                        if check["playerteam"]=="None":
                            #adding the player to the users team and updating the users budget
                            cursor.execute("UPDATE PLAYERSWD2 SET playerteam=%s WHERE name=%s", (username, player))
                            connection.commit()
                            cursor.execute("SELECT value FROM PLAYERSWD2 WHERE name=%s", (player))
                            playerValue=cursor.fetchone()
                            cursor.execute("SELECT budget FROM FANTASYPLAYERS WHERE username=%s", (username))
                            userBudget=cursor.fetchone()
                            newUserBudget=int(userBudget["budget"])-int(playerValue["value"])
                            cursor.execute("UPDATE FANTASYPLAYERS SET budget=%s WHERE username=%s", (newUserBudget, username))
                            connection.commit()

                        else:
                            cursor.execute("SELECT playerteam FROM PLAYERSWD2 WHERE name=%s", (player))
                            name1=cursor.fetchone()
                            return "<p>Player taken by %s</p>" % name1["playerteam"]
                    else:
                        return "<p>You have reached the limit of players from the same club! Check your team!</p>"
                else:
                    return "<p>You already have the limit! Check your team!</p>"
    else:
        return "<p>You can only pick up to the limit! Check your team!</p>"

    return "<p>Update success! Check your team!</p>"


connection=db.connect('localhost', 'dgjm1', 'ahgha', 'cs1021_cs5021_dgjm1')
cursor=connection.cursor(db.cursors.DictCursor)

if len(formData)!=0:
    try:
        username = escape(formData.getfirst("username", "").strip())
        if username:
            cursor.execute("SELECT * FROM FANTASYPLAYERS WHERE username=%s", (username))
            if cursor.rowcount > 0:
                cursor.execute("SELECT * FROM PLAYERSWD2 WHERE playerteam=%s", (username))
                if cursor.rowcount<15:
                    goalkeepers=formData.getlist("goalkeeper")
                    defenders=formData.getlist("defender")
                    midfielders=formData.getlist("midfielder")
                    forwards=formData.getlist("forward")
                    if len(goalkeepers)>0:
                        resultGK = add_To_Team(username, goalkeepers, 2)
                    if len(defenders)>0:
                        resultDef = add_To_Team(username, defenders, 5)
                    if len(midfielders)>0:
                        resultMF = add_To_Team(username, midfielders, 5)
                    if len(forwards)>0:
                        resultFor = add_To_Team(username, forwards, 3)

                else:
                    checkboxPlayers = "<p>You can't have more than fifteen players!</p>"
            else:
                checkboxPlayers = "<p>That username is not in our database!</p>"

        else:
            checkboxPlayers = "<p>Please enter your username!</p>"
    except db.Error:
        checkboxPlayers="<p>Sorry, we're having issues at the moment. Please come back later!</p>"






try:
    cursor.execute("SELECT name, club, playingPosition FROM PLAYERSWD2 ORDER BY playingPosition")
    if cursor.rowcount == 0:
        checkboxPlayers="<p>Sorry. There are no players at present.</p>"
    else:
        cursor.execute("SELECT name, club, playingPosition, value, playerteam FROM PLAYERSWD2 WHERE playingPosition='goalkeeper' AND playerteam = 'None' ORDER BY name")
        for row in cursor.fetchall():
            slicing=row["name"][:3]
            goalkeeper+="<label for='%s'>%s, Team: %s, Position: %s, Value: %s</label><input type='checkbox' name='goalkeeper' value='%s' id='%s' />" % (slicing, row["name"], row["club"], row["playingPosition"], row["value"], row["name"], slicing)

        cursor.execute("SELECT name, club, playingPosition, value, playerteam FROM PLAYERSWD2 WHERE playingPosition='defender' AND playerteam = 'None' ORDER BY name")
        for row in cursor.fetchall():
            if row["name"]=="David Luiz" or row["name"]=="Antonio Rudiger" or row["name"]=="Marcos Alonso"  or row["name"]=="Nicolas Otamendi":
                slicing1=row["name"][:3]+"1"
            else:
                slicing1=row["name"][:3]
            defender+="<label for='%s'>%s, Team: %s, Position: %s, value: %s</label><input type='checkbox' name='defender' value='%s' id='%s' />" % (slicing1, row["name"], row["club"], row["playingPosition"], row["value"], row["name"], slicing1)

        cursor.execute("SELECT name, club, playingPosition, value, playerteam FROM PLAYERSWD2 WHERE playingPosition='midfielder' AND playerteam = 'None' ORDER BY name")
        for row in cursor.fetchall():
            if row["name"]=="Dani Ceballos" or row["name"]=="Bernardo Silva" or row["name"]=="Mason Mount":
                slicing2=row["name"][:3]+"1"
            elif row["name"]=="David Silva":
                slicing2=row["name"][:3]+"2"
            else:
                slicing2=row["name"][:3]
            midfielder+="<label for='%s'>%s, Team: %s, Position: %s, value: %s</label><input type='checkbox' name='midfielder' value='%s' id='%s' />" % (slicing2, row["name"], row["club"], row["playingPosition"], row["value"], row["name"], slicing2)

        cursor.execute("SELECT name, club, playingPosition, value, playerteam FROM PLAYERSWD2 WHERE playingPosition='forward' AND playerteam = 'None' ORDER BY name")
        for row in cursor.fetchall():
            if row["name"]=="Sergio Aguero" or row["name"]=="Willian":
                slicing3=row["name"][:3]+"1"
            else:
                slicing3=row["name"][:3]
            forward+="<label for='%s'>%s, Team: %s, Position: %s, value: %s</label><input type='checkbox' name='forward' value='%s' id='%s' />" % (slicing3, row["name"], row["club"], row["playingPosition"], row["value"], row["name"], slicing3)



    cursor.close()
    connection.close()

except db.Error:
    checkboxPlayers="<p>Sorry, we're having issues at the moment. Please come back later!</p>"



print("""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8" />
                <title>Players List</title>
                <link rel="stylesheet" href="index.css" />
                <!--put favicon, javascript here-->
            </head>
            <body>
                <header>
                    <h1>
                        Players
                    </h1>
                </header>
                <main>
                    <section class="links">
                        <ul>
                            <li><a href="practiceIndex.py">Home Page</a></li>
                            <li><a href="practicePlayerTeam.py">Your Team</a></li>
                            <li><a href="practicePlayerScore.py">Enter Your Players Performance Stats</a></li>
                            <li><a href="practicePlayerTransfer.py">Request a Transfer</a></li>
                            <li><a href="practicePlayerRelease.py">Release a Player</a></li>
                        </ul>
                    </section>
                    <section>
                        <h1>
                            Rules
                        </h1>
                        <section id="rules">
                            <section class="rules1">
                                <ul>
                                    <li>In order to play, you must first register and login (don't worry, it's free!).</li>
                                    <li>After creating your team, you'll be given &pound;100 million to spend on players!</li>
                                    <li>You can only choose up to 15 players for your team.</li>
                                    <li>Once a player has been chosen no other fantasy football player can choose that player without asking for a transfer (request page is on a different page, link above)</li>
                                    <li>Check the bottom of the page to check if you successfully made updates to your team and check your full team at the link above as well</li>
                                    <li>You can't have more than 6 players from the same club</li>
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
                    </section><section>
                        <h1>
                            Football Players
                        </h1>

                            <section id="footballers">
                                <form action="practicePlayerForm.py" method="post">
                                    <fieldset class="footballers">


                                        %s


                                        %s


                                        %s


                                        %s
                                        <label for="username">Please enter your username</label>
                                        <input type="text" name="username" id="username" />
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
            </html>"""%(goalkeeper, defender, midfielder, forward, checkboxPlayers, resultGK, resultDef, resultMF, resultFor))
