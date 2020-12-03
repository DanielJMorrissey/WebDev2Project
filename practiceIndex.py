#!/usr/local/bin/python3

from cgitb import enable
enable()
from html import escape
import pymysql as db
from cgi import FieldStorage
print("Content-Type: text/html")
print()
formData=FieldStorage()


playerScores=""

result=""
try:
    connection=db.connect('localhost', 'dgjm1', 'ahgha', 'cs1021_cs5021_dgjm1')
    cursor=connection.cursor(db.cursors.DictCursor)

    if len(formData) > 0:
        username=escape(formData.getfirst("username", "").strip())
        firstname=escape(formData.getfirst("firstname", "").strip())
        surname=escape(formData.getfirst("surname", "").strip())
        teamname=escape(formData.getfirst("team", "").strip())
        if len(username)>0 and len(firstname)>0 and len(surname)>0 and len(teamname)>0:
            cursor.execute("SELECT * FROM FANTASYPLAYERS WHERE username=%s", (username))
            if cursor.rowcount > 0:
                result = "<p>Username taken! Try again!</p>"

            else:
                cursor.execute("SELECT * FROM FANTASYPLAYERS WHERE teamName=%s", (teamname))
                if cursor.rowcount>0:
                    result = "<p>Team name taken! Try again!</p>"
                else:
                    cursor.execute("INSERT INTO FANTASYPLAYERS (teamName, budget, points, playerFirstName, playerSurnameName, username) VALUES (%s, 100000000, 0, %s, %s, %s)", (teamname, firstname, surname, username))
                    connection.commit()
                    result="<p>Your details have been added!</p>"
        else:
            result = "<p>Please enter all details!</p>"


    cursor.execute("SELECT username, teamName, points FROM FANTASYPLAYERS ORDER BY points DESC")
    if cursor.fetchall == 0:
        playerScores="<p>There are currently no fantasy football players at the moment</p>"
    else:
        playerScores="<table id='leagueTable'><tr><th>Manager</th><th>Team</th><th>Points</th></tr>"
        for row1 in cursor.fetchall():
            playerScores+="<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (row1["username"], row1["teamName"], row1["points"])
        playerScores+="</table>"
    cursor.close()
    connection.close()
except db.Error:

    result, playerScores="<p>Sorry, we're having issues at the moment. Please come back later!</p>"




print("""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8" />
                <title>Fantasy Football</title>
                <link rel="stylesheet" href="index.css" />
            </head>
            <body>
                <header>
                    <h1>
                        Welcome to Dan's Fantasy Football League!
                    </h1>
                    <p>
                        Play against your friends or just kill time by becoming a virtual manager..
                    </p>
                </header>
                <main>
                    <section class="links">
                        <ul>

                            <li><a href="practicePlayerForm.py">Player List</a></li>
                            <li><a href="practicePlayerTeam.py">Your Team</a></li>
                            <li><a href="practicePlayerTransfer.py">Request a Transfer</a></li>
                            <li><a href="practicePlayerRelease.py">Release a Player</a></li>
                            <li><a href="practicePlayerScore.py">Enter Your Players Performance Stats</a></li>
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
                                    <li>Once a player has been chosen no other fantasy football player can choose that player without asking for a transfer</li>
                                    <li>Check the rules on each page as there are rules relevant to that page</li>
                                    <li>Each point will get you &pound;100,000</li>
                                    <li>Remember, check the bottom of the form to see if you have successfully updated your score or team</li>
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
                            Scoring
                        </h1>
                        <section id="scoring">
                            <table class="scoring1">
                                <tr>
                                    <th>Action</th><th>Point(s)</th>
                                </tr>
                                <tr>
                                    <td>Not playing</td><td>0</td>
                                </tr>
                                <tr>
                                    <td>Playing for 60 minutes or less</td><td>1</td>
                                </tr>
                                <tr>
                                    <td>Playing for 61 minutes or more</td><td>2</td>
                                </tr>
                                <tr>
                                    <td>Goal scored by a goalkeeper</td><td>7</td>
                                </tr>
                                <tr>
                                    <td>Goal scored by a defender</td><td>6</td>
                                </tr>
                                <tr>
                                    <td>Goal scored by a midfielder</td><td>5</td>
                                </tr>
                                <tr>
                                    <td>Goal scored by a forward</td><td>4</td>
                                </tr>
                                <tr>
                                   <td>Goal assist by a defender or goalkeeper</td><td>6</td>
                                </tr>
                                <tr>
                                    <td>Goal assist by a midfielder or forward</td><td>5</td>
                                </tr>
                                <tr>
                                    <td>Clean sheet by a goalkeeper or defender</td><td>4</td>
                                </tr>
                                <tr>
                                    <td>Clean sheet by a midfielder</td><td>5</td>
                                </tr>
                            </table>
                            <table  class="scoring1">
                                <tr>
                                    <th>Action</th><th>Point(s)</th>
                                </tr>
                                <tr>
                                    <td>Every 4 shots saved by a goalkeeper</td><td>1</td>
                                </tr>
                                <tr>
                                    <td>For every penalty save</td><td>5</td>
                                </tr>
                                <tr>
                                    <td>For every penalty miss</td><td>-5</td>
                                </tr>
                                <tr>
                                    <td>For conceding a free kick</td><td>-1</td>
                                </tr>
                                <tr>
                                    <td>For conceding a penalty</td><td>-3</td>
                                </tr>
                                <tr>
                                    <td>Player being Man of the Match</td><td>2</td>
                                </tr>
                                <tr>
                                    <td>For every goal conceded</td><td>-1</td>
                                </tr>
                                <tr>
                                    <td>For each yellow card</td><td>-1</td>
                                </tr>
                                <tr>
                                    <td>For each red card</td><td>-3</td>
                                </tr>
                                <tr>
                                    <td>For each own goal</td><td>-3</td>
                                </tr>
                            </table>
                        </section>
                    </section>

                    <section id="login">
                        <h1>
                            Your Details
                        </h1>
                        <form action="practiceIndex.py" method="post">

                            <input type="text" name="username" placeholder="Username"/>
                            <input type="text" name="firstname" placeholder="First Name" />
                            <input type="text" name="surname" placeholder="Surname" />
                            <input type="text" name="team" placeholder="Team Name" />
                            <input type="submit" />
                        </form>
                        %s
                    </section>


                    <section>
                        <h1 id="leagueHeading">
                            League Table
                        </h1>
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
    """ % (result, playerScores))
