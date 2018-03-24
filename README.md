# SFTP_Email_Bot
A bot that opens an SFTP request and generate a unique username and password for each email.

To trigger the bot you need to send an email to the email you specify in the script containing a keyword by default its "DATA" the bot will generate a unique username and password and email back them to you, the server will give a one hour session and closes the connection back, if another request is sent while the server have an opened session, the server will notify the sender that it's busy and then automatically opens a sftp session for him after its done.

Required Libraries:
smtplib
paramico

the server uses mysqldb to store the opened sessions, requested sessions.
Python 2.7 is used.

Configuration Steps:
in the mail-recieve.py:
  you need to add the email that the bot should listen too at the top of the script you change the variables below:
  youremail = "EMAILHERE"
  yourpassword = "PASSWORDHERE"
  if you want to change the keyword change the variable below:
  keyword = "DATA"
in the sendemail.py:
  you need to add the email that the bot should send notifications from at the top of the script you change the variables below:
  youremail = "EMAILHERE"
  yourpassword = "PASSWORDHERE"
in dbconnector.py:
  you should edit the connection strings specify your server address and the username and password.
     return MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="password",  # your password
                         db="sftp") 
use the createdatabase.db script to create the server db.
to launch the bot:
  python mail-receive.py
