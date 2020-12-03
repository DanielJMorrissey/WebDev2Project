#!/usr/local/bin/python3

from cgitb import enable
enable()
from html import escape
from cgi import FieldStorage
import pymysql as db



print("Content-Type: text/html")
print()

def player_Release(username, playerList, limit):
    if len(playerList)>0 and len(playerList)<=limit:
        for player in playerList:
            #checking if player is in database
            cursor.execute("SELECT * FROM PLAYERSWD2 WHERE name=%s", (player))
            if cursor.rowcount>0:
                #checking if player is part of users team
                cursor.execute("SELECT * FROM PLAYERSWD2 WHERE name=%s", (player))
                check=cursor.fetchone()
                if check["playerteam"]==username:
                    #releasing player from the users team
                    cursor.execute("UPDATE PLAYERSWD2 SET playerteam='None' WHERE name=%s", (player))
                    connection.commit()

                else:
                    return "<p>The player is either not on your team or has not been selected for a team! Check your team!</p>"
            else:
                return "<p>Player is not in our database! Check your team!</p>"

        return "<p>The player(s) has been released</p>"
    else:
        return "<p>You can not have more than the limit of players in that position in your team!</p>"


formData=FieldStorage()
checkBoxP=""
goalkeeper=""
goalKee=""
defender=""
midfielder=""
forward=""
checkU=""
defe=""
midf=""
forwa=""



try:
    connection=db.connect('localhost', 'dgjm1', 'ahgha', 'cs1021_cs5021_dgjm1')
    cursor=connection.cursor(db.cursors.DictCursor)

    if len(formData)!=0:
        username=escape(formData.getfirst("user", "").strip())
        if username:
            cursor.execute("SELECT * FROM FANTASYPLAYERS WHERE username=%s", (username))
            if cursor.rowcount>0:

                    goalkeepers=formData.getlist("goalkeeper")
                    defenders=formData.getlist("defender")
                    midfielders=formData.getlist("midfielder")
                    forwards=formData.getlist("forward")
                    
                    if len(goalkeepers)>0:
                        goalKee = player_Release(username, goalkeepers, 2)

                    if len(defenders)>0:
                        defe = player_Release(username, defenders, 5)
                    if len(midfielders)>0:
                        midf = player_Release(username, midfielders, 5)

                    if len(forwards)>0:
                        forwa = player_Release(username, forwards, 3)

            else:
                checkU="<p>Username is not in our database</p>"
        else:
            checkU="<p>Please enter a username!</p>"

    #putting out list of players
    cursor.execute("SELECT name, club, playingPosition FROM PLAYERSWD2 ORDER BY playingPosition")
    if cursor.rowcount == 0:
        checkBoxP="<p>Sorry. There are no players at present.</p>"
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
    checkBoxP="<p>Sorry, we're experiencing problems at the moment. Please try again another time!</p>"




print("""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <title>Player Release</title>
                <meta charset="utf-8" />
                <link rel="stylesheet" href="index.css" />
            </head>
            <body>
                <header>
                    <h1>
                        Player Release
                    </h1>
                </header>
                <main>
                    <section class="links">
                        <ul>
                            <li><a href="practiceIndex.py">Home Page</a></li>
                            <li><a href="practicePlayerForm.py">Player List</a></li>
                            <li><a href="playerTeam.py">Your Team</a></li>
                            <li><a href="playerScore.py">Enter Your Players Performance Stats</a></li>
                            <li><a href="playerTransfer.py">Request a Transfer</a></li>
                           
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
                                    <li>Then you must create a team where you'll be the manager.</li>
                                    <li>After creating your team, you'll be given &pound;100 million to spend on players!</li>
                                    <li>You can only choose up to 15 players for your team.</li>
                                    <li>Once a player has been chosen no other fantasy football player can choose that player without asking for a transfer</li>
                                    <li>Only remove players from your own team</li>
                                    <li>Releasing a player will not cost you anything but your budget will not increase</li>
                                    <li>Check the bottom of the form to see if you have successfully released the player</li>
                                </ul>
                            </section>
                            <section class="rules1">
                                <h1>
                                    Choosing Players
                                </h1>
                                <p>
                                    Your 15 man squad must contain:
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
                                        <form action="practicePlayerRelease.py" method="post">
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
""" % (goalkeeper, defender, midfielder, forward, checkBoxP, checkU, goalKee, defe, midf, forwa))
