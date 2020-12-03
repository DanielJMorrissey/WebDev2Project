#!/usr/local/bin/python3

from cgitb import enable
enable()
from html import escape
from cgi import FieldStorage
import pymysql as db



print("Content-Type: text/html")
print()

formData=FieldStorage()
score=0
result=""
playerScores=""



try:

    connection=db.connect('localhost', 'dgjm1', 'ahgha', 'cs1021_cs5021_dgjm1')
    cursor=connection.cursor(db.cursors.DictCursor)

    if len(formData)!=0:
        username=escape(formData.getfirst("username", "").strip())
        player=escape(formData.getfirst("playername", "").strip())
        position=escape(formData.getfirst("position", "").strip())
        minutes=escape(formData.getfirst("time", "").strip())
        goalsScored=escape(formData.getfirst("scored", "").strip())
        goalsAssisted=escape(formData.getfirst("assists", "").strip())
        cleanSheet=escape(formData.getfirst("cleanSheet", "").strip())
        saves=escape(formData.getfirst("saves", "").strip())
        penaltySave=escape(formData.getfirst("penaltySave", "").strip())
        penaltyMiss=escape(formData.getfirst("penaltyMiss", "").strip())
        concededFreeKick=escape(formData.getfirst("concededFree", "").strip())
        concededPenKick=escape(formData.getfirst("concededPen", "").strip())
        manMatch=escape(formData.getfirst("manMatch", "").strip())
        goalsConceded=escape(formData.getfirst("conceded", "").strip())
        yellowCards=escape(formData.getfirst("yellow", "").strip())
        redCards=escape(formData.getfirst("redCard", "").strip())
        ownGoal=escape(formData.getfirst("owngoal", "").strip())
        #checking if all relevant data was sent
        if player and position and minutes and goalsScored and goalsAssisted and cleanSheet and yellowCards and redCards and ownGoal:
            if saves and penaltySave and penaltyMiss and concededFreeKick and concededPenKick and manMatch and goalsConceded and username:
                #checking if player is in database
                cursor.execute("SELECT * FROM PLAYERSWD2 WHERE name=%s", (player))
                if cursor.rowcount>0:



                        cursor.execute("SELECT * FROM FANTASYPLAYERS WHERE username=%s", (username))
                        if cursor.rowcount>0:
                            #checking if player is part of users team
                            cursor.execute("SELECT * FROM PLAYERSWD2 WHERE playerteam=%s and name=%s", (username, player))
                            if cursor.rowcount>0:
                                #updating the users score
                                cursor.execute("SELECT * FROM PLAYERSWD2 WHERE playerteam=%s and name=%s", (username, player))
                                check=cursor.fetchone()
                                playingPosition=check["playingPosition"]
                                playingTime=minutes
                                if int(playingTime) or int(playingTime)==0:
                                    playingTime=int(playingTime)

                                    if playingTime==0:
                                        score=0
                                    elif playingTime>0 and playingTime<=60:
                                        score+=1
                                    elif playingTime>60:
                                        score+=2


                                else:
                                    result="<p>You have sent wrong data! 1</p>"
                                if int(playingTime)>0:
                                    goalsScored1=goalsScored
                                    if int(goalsScored1) or int(goalsScored1)==0:
                                        goalsScored1=int(goalsScored1)
                                        if playingPosition=="goalkeeper":
                                            score+=(7*goalsScored1)
                                        elif playingPosition=="defender":
                                            score+=(6*goalsScored1)
                                        elif playingPosition=="midfielder":
                                            score+=(5*goalsScored1)
                                        elif playingPosition=="forward":
                                            score+=(4*goalsScored1)

                                    else:
                                        result="<p>You have sent wrong data! 2</p>"
                                    goalsAssisted1=goalsAssisted
                                    if int(goalsAssisted1) or int(goalsAssisted1)==0:
                                        goalsAssisted1=int(goalsAssisted1)
                                        if playingPosition=="goalkeeper" or playingPosition=="defender":
                                            score+=(6*goalsAssisted1)
                                        elif playingPosition=="midfielder" or playingPosition=="forward":
                                            score+=(5*goalsAssisted1)

                                    else:
                                        result="<p>You have sent wrong data! 3</p>"
                                    cleanSheet=cleanSheet.lower()
                                    if cleanSheet=="yes":
                                        if playingPosition=="goalkeeper" or playingPosition=="defender":
                                            score+=4
                                        elif playingPosition=="midfielder":
                                            score+=5
                                    elif cleanSheet=="no":
                                        if playingPosition=="goalkeeper" or playingPosition=="defender":
                                            score+=0
                                        elif playingPosition=="midfielder":
                                            score+=0
                                    elif cleanSheet!="no" or cleanSheet!="yes":
                                        result="<p>You have sent wrong data! 4</p>"
                                    saves1=saves
                                    if int(saves1) or int(saves1)==0:
                                        saves1=int(saves1)
                                        score+=(1*(saves1//4))

                                    else:
                                        result="<p>You have sent wrong data! 5</p>"
                                    penaltySave1=penaltySave
                                    if int(penaltySave1) or int(penaltySave1)==0:
                                        penaltySave1=int(penaltySave1)
                                        score+=(5*penaltySave1)

                                    else:
                                        result="<p>You have sent wrong data! 6</p>"
                                    penaltyMiss1=penaltyMiss
                                    if int(penaltyMiss1) and cleanSheet=="no":
                                        penaltyMiss1=int(penaltyMiss1)
                                        score-=(5*penaltyMiss1)
                                    elif int(penaltyMiss1)==0:
                                        penaltyMiss1=int(penaltyMiss1)
                                        score-=(5*penaltyMiss1)
                                    elif cleanSheet=="yes" and int(penaltyMiss1)>0:
                                        result="<p>You can't have a clean sheet and miss a penalty!</p>"
                                    else:
                                        result="<p>You have sent wrong data! 7</p>"
                                    concededFreeKick1=concededFreeKick
                                    if int(concededFreeKick1) or int(concededFreeKick1)==0:
                                        concededFreeKick1=int(concededFreeKick1)
                                        score-=(1*concededFreeKick1)
                                    else:
                                        result="<p>You have sent wrong data! 8</p>"
                                    concededPenKick1=concededPenKick
                                    if int(concededPenKick1) or int(concededPenKick1)==0:
                                        concededPenKick1=int(concededPenKick1)
                                        score-=(3*concededPenKick1)
                                    else:
                                        result="<p>You have sent wrong data! 9</p>"
                                    manMatch=manMatch.lower()
                                    if manMatch=="yes":
                                        score+=2
                                    elif manMatch=="no":
                                        score+=0
                                    else:
                                        result="<p>You have sent wrong data! 10</p>"

                                    goalsConceded1=goalsConceded
                                    if int(goalsConceded1) and cleanSheet=="no":
                                        goalsConceded1=int(goalsConceded1)
                                        score-=(1*goalsConceded1)
                                    elif int(goalsConceded1)==0:
                                        goalsConceded1=int(goalsConceded1)
                                        score-=(1*goalsConceded1)
                                    elif cleanSheet=="yes" and int(goalsConceded1)>0:
                                        result="<p>You can't have a clean sheet and concede a goal</p>"
                                    else:
                                        result="<p>You have sent wrong data! 11</p>"
                                    yellowCards1=yellowCards
                                    if int(yellowCards1) and int(yellowCards1)>0:
                                        yellowCards1=int(yellowCards1)
                                        if yellowCards1<=2:
                                            score-=(1*yellowCards1)
                                        else:
                                            result="<p>You have sent wrong data! 12</p>"
                                    elif int(yellowCards1)==0:
                                        yellowCards1=int(yellowCards1)
                                        if yellowCards1<=2:
                                            score-=(1*yellowCards1)
                                    else:
                                        result="<p>You have sent wrong data! 13</p>"
                                    redCards=redCards.lower()
                                    if redCards=="yes":
                                        score-=3
                                    elif redCards=="no":
                                        score+=0
                                    else:
                                        result="<p>You have sent wrong data!</p>"

                                    ownGoal1=ownGoal
                                    if int(ownGoal1) and cleanSheet=="no":
                                        ownGoal1=int(ownGoal1)
                                        score-=(3*ownGoal1)
                                    elif int(ownGoal1)==0:
                                        ownGoal1=int(ownGoal1)
                                        score-=(3*ownGoal1)
                                    elif cleanSheet=="yes" and int(ownGoal1)>0:
                                        result="<p>You can't have a clean sheet and concede a goal</p>"
                                    else:
                                        result="<p>You have sent wrong data(15)!</p>"
                                    if result=="":
                                        cursor.execute("UPDATE FANTASYPLAYERS SET points=points+%s WHERE username=%s", (score, username))
                                        connection.commit()
                                        reward=score*100000
                                        cursor.execute("UPDATE FANTASYPLAYERS SET budget=budget+%s WHERE username=%s", (reward, username))
                                        connection.commit()
                                        result="<p>League table updated</p>"
                                else:
                                    result="<p>The player can't get points if he didn\'t play!</p>"
                            else:
                                result="<p>The player is not part of your team!</p>"

                        else:
                            result="<p>Username is not in our database!</p>"

                else:
                    result="<p>Player is not in our database!</p>"
            else:
                result="<p>Please fill all fields!</p>"
        else:
            result="<p>Please fill all fields!</p>"

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
    result="<p>Sorry, we're experiencing problems at the moment. Please try again another time!</p>"


print("""
      <!DOCTYPE html>
      <html lang="en">
        <head>
          <title>Player Stats Submission</title>
          <meta charset="utf-8" />
          <link rel="stylesheet" href="index.css" />
        </head>
        <body>
          <header>
            <h1>
              Player Stats Submission
            </h1>
          </header>
          <main>
            <section class="links">
                <ul>
                    <li><a href="practiceIndex.py">Home Page</a></li>
                    <li><a href="practicePlayerForm.py">Player List</a></li>
                    <li><a href="practicePlayerTeam.py">Your Team</a></li>
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
                            <li>Once a player has been chosen no other fantasy football player can choose that player without asking for a transfer</li>
                            <li>Check the league table below.</li>
                            <li>Each point will get you &pound;100,000</li>
                            <li>Please fill all fields</li>
                            <li>Check the bottom of the form to see if you have successfully entered the stats</li>
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
            <section>
                <form action="practicePlayerScore.py" method="post">
                    <fieldset>
                        <legend>Player's Performance</legend>
                        <label for="username">Please enter your username</label>
                        <input type="text" name="username" id="username" class="textfield1" />

                        <label for="playername" class="textfield">Player's Name</label>
                        <input type="text" name="playername" id="playername" class="textfield1" />

                        <label for="position" class="textfield">Player's Position</label>
                        <input type="text" name="position" id="position" class="textfield1" />

                        <label for="time" class="textfield">Minutes Played</label>
                        <input type="text" name="time" id="time" class="textfield1" />

                        <label for="scored" class="textfield">Goals Scored</label>
                        <input type="text" name="scored" id="scored" class="textfield1" />

                        <label for="assist" class="textfield">Goals Assisted</label>
                        <input type="text" name="assists" id="assist" class="textfield1" />

                        <label id="clean">Clean Sheet</label>
                        <label for="YES" class="radio" id="yes">Yes:</label>
                        <input type="radio" name="cleanSheet"  value="yes" id="YES" class="radio1"/>
                        <label for="NO" class="radio" id="no">No:</label>
                        <input type="radio" name="cleanSheet" value="no" id="NO" class="radio1" checked />

                        <label for="saves" class="textfield">Number of Saves Made</label>
                        <input type="text" name="saves" id="saves" class="textfield1" />

                        <label for="penaltySave" class="textfield">Number of Saved Penalties</label>
                        <input type="text" name="penaltySave" id="penaltySave" class="textfield1" />

                        <label for="penaltyMiss" class="textfield">Number of Penalties Missed</label>
                        <input type="text" name="penaltyMiss" id="penaltyMiss" class="textfield1" />

                        <label for="concededFree" class="textfield">Number of Free Kicks Conceded</label>
                        <input type="text" name="concededFree" id="concededFree" class="textfield1" />

                        <label for="concededPen" class="textfield">Number of Penalties Conceded</label>
                        <input type="text" name="concededPen" id="concededPen" class="textfield1" />

                        <label>Man of the Match</label>
                        <label for="YES1" class="radio" id="yes1">Yes:</label>
                        <input type="radio" name="manMatch" value="yes" id="YES1" class="radio1" />
                        <label for="NO1" class="radio" id="no1">No:</label>
                        <input type="radio" name="manMatch" value="no" id="NO1" class="radio1" checked />

                        <label for="conceded" class="textfield">Number of Goals Conceded</label>
                        <input type="text" name="conceded" id="conceded" class="textfield1" />

                        <label for="yellow" class="textfield">Number of Yellow Cards</label>
                        <input type="text" name="yellow" id="yellow" class="textfield1" />

                        <label>Red Card</label>
                        <label for="YES2" class="radio" id="yes2">Yes:</label>
                        <input type="radio" name="redCard" value="yes" id="YES2" class="radio1" />
                        <label for="NO2" class="radio" id="no2">No:</label>
                        <input type="radio" name="redCard" value="no" id=NO2 class="radio1" checked />

                        <label for="owngoal" class="textfield">Number of Own Goals</label>
                        <input type="text" name="owngoal" id="owngoal" class="textfield1" />

                        <input type="reset" class="submit"/>
                        <input type="submit" class="submit" />
                        %s
                    </fieldset>
                </form>

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
