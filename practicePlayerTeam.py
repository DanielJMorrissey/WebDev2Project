#!/usr/local/bin/python3

from cgitb import enable
enable()
from html import escape
from cgi import FieldStorage
import pymysql as db



print("Content-Type: text/html")
print()

formData=FieldStorage()
result=""
budget=""


if len(formData)!=0:
    try:
        connection=db.connect('localhost', 'dgjm1', 'ahgha', 'cs1021_cs5021_dgjm1')
        cursor=connection.cursor(db.cursors.DictCursor)
        username=escape(formData.getfirst("user", "").strip())
        if username:
            #checking if username is in database
            cursor.execute("SELECT * FROM FANTASYPLAYERS WHERE username=%s", (username))
            if cursor.rowcount>0:
                #pulling data from the database to show to user
                cursor.execute("SELECT * FROM FANTASYPLAYERS WHERE username=%s", (username))
                budgetCheck=cursor.fetchone()
                budget="<h1>%s's Current Budget</h1><p>&pound;%i</p>" % (username, budgetCheck["budget"])
                cursor.execute("SELECT * FROM PLAYERSWD2 WHERE playerteam=%s", (username))
                if cursor.rowcount>0:
                    result="<h1>%s's Team</h1><table><tr><th>Player</th><th>Club</th><th>Position</th><th>Value</th></tr>" % (username)
                    cursor.execute("SELECT * FROM PLAYERSWD2 WHERE playerteam=%s ORDER BY playingPosition", (username))
                    for player in cursor.fetchall():
                        result+="<tr><td>%s</td><td>%s</td><td>%s</td><td>&pound;%s</td></tr>" % (player["name"], player["club"], player["playingPosition"], player["value"])
                    result+="</table>"
                else:
                    result="<h1>%s's Team</h1><p>There are currently no players in your team!</p>" % (username)
            else:
                result="<p>Username is not in our database!</p>"
        else:
            result="<p>Please enter a username!</p>"

        cursor.close()
        connection.close()
    except db.Error:
        result="<p>Sorry, we're experiencing problems at the moment. Please try again another time!</p>"



print("""
      <!DOCTYPE html>
      <html lang="en">
        <head>
          <title>Your Team</title>
          <meta charset="utf-8" />
          <link rel="stylesheet" href="index.css" />
        </head>
        <body>
          <header>
            <h1>
              Your Team
            </h1>
          </header>
          <main>
            <section class="links">
                <ul>
                    <li><a href="practiceIndex.py">Home Page</a></li>
                    <li><a href="practicePlayerForm.py">Player List</a></li>
                    <li><a href="practicePlayerScore.py">Enter Your Players Performance Stats</a></li>
                    <li><a href="practicePlayerTransfer.py">Request a Transfer</a></li>
                    <li><a href="practicePlayerRelease.py">Release a Player</a></li>
                </ul>
            </section>

            <section id="instructions">
                <h1>
                    Instructions
                </h1>
                <p>
                    All you have to do is enter a username and press submit. This is where you'll see your budget and your players (or other users budget and players).
                </p>
            </section>
            <section>


                            <section id="footballers">
                                <form action="practicePlayerTeam.py" method="post">
                                    <fieldset class="footballers">

                                        <label for="user">Please enter your username</label>
                                        <input type="text" name="user" id="user" />

                                        <input type='submit' class='submit' />

                                    </fieldset>



                                </form>
                            </section>

                    </section>
                    <section id="budget">

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
""" % (budget, result))
