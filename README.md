# SFTP_Email_Bot
A bot that manage an SFTP server connections by email commands.

To trigger the bot you need to send an email to the email you specify in the script containing a keyword by default its "DATA" the bot will generate a unique username and password and email back them to you, the server default session time is 1 hour after it expires it will close the connection,if another request is sent while the server have an opened session, the server will notify the sender that it's busy when the server is done from the first session it will automatically opens up a session for the second one.

<h4>Required Libraries:</h4>
smtplib<br />
paramico<br />

the server uses mysqldb to store the opened sessions, requested sessions.<br />
Python 2.7 is used.<br />

<h4>Configuration Steps:</h4>
<h5>mail-recieve.py:</h5>
  add the lisetning email, at the top of the script you change the variables below:<br />
    <code> youremail = "EMAILHERE"</code> <br />
    <code>yourpassword = "PASSWORDHERE" </code><br />
  if you want to change the keyword change the variable below:<br />
    <code> keyword = "DATA"</code><br />
<h5>sendemail.py:</h5>
   add the email that the bot should use to send notifications, at the top of the script you change the variables below:<br />
   <code> youremail = "EMAILHERE"</code> <br />
    <code>yourpassword = "PASSWORDHERE" </code>
  
<h5>dbconnector.py:</h5>
  you should edit the connection strings specify your server address and the username and password.
  
     return MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="password",  # your password
                         db="sftp") 
<h5>Mysql DB Configuration</h5>               
use <b>createdatabase.sql</b> to create the DB.
<h4>launch the bot:</h4>
  <code>python mail-receive.py</code>
