import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sys


#Next, log in to the server
serverip="SERVERIP"
youremail = "YourEmailHere"
yourpassword = "YourPasswordHere"

def getemailfromname(name):
	startcut = 0
	endcut = 0
	index = 0
	for c in name:
		if '<' in c:
			startcut = index
		if '>' in c:
			endcut = index
		index = index + 1
	return name[startcut+1:endcut]

fromaddr = youremail
# if "reminder" in sys.argv[1]:
# 	with open('/home/serv/Desktop/REQUEST-DIR/listofmails') as f:
# 		content = f.readlines()
		# you may also want to remove whitespace characters like `\n` at the end of each line
# 		content = [x.strip() for x in content]
# 	for line in content:
# 		toaddr = line;
# 		msg = MIMEMultipart()
# 		msg['From'] = fromaddr
# 		msg['To'] = toaddr
# 		msg['Subject'] = "Resellers Reminders"
# 		body = "Dear, \n\nThis is a reminder, Please don't forget to send the monthly resellers list, Thank you \n\nBest Regards "
# 		msg.attach(MIMEText(body, 'plain'))
# 		server = smtplib.SMTP('smtp.general-security.gov.lb', 25)
# 		#server.ehlo()
# 		#server.starttls()
# 		#server.ehlo()
# 		server.login("mahmoud.younes@general-security.gov.lb", "M@#moud12345")
# 		text = msg.as_string()
# 		server.sendmail(fromaddr, toaddr, text)
		#Send the mail
		#msg = " Hello!" # The /n separates the message from the headers
		#server.sendmail("mahmoud.younes@general-security.gov.lb", "ziad_kiwan_1992@hotmail.com", msg)
def sendAuthmail(to,user,password):
		toaddr = getemailfromname(to);
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Subject'] = "Server is Ready"
		body = "Dear , \n\nThe SFTP server is ready to recieve data, please use the IP "+serverip+", port 2200 and the following credentials to login:\n\nUsername:"+user+" \nPassword:"+password+"\n\nAfter one hour the server will shutdown, you can request a new username and password by sending a new email again.\n\nBest Regards "
		msg.attach(MIMEText(body, 'plain'))
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		#server.ehlo()
		#server.starttls()
		#server.ehlo()
		server.login(youremail, yourpassword)
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		#Send the mail
		#msg = " Hello!" # The /n separates the message from the headers
def sendruningmail(to):
	toaddr = getemailfromname(to);
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Server is Busy"
	body = "Dear , \n\nThe SFTP server is already running, Please check your inbox or the junk folder, \nif it's the first time you send a request the server will email back your credential when its ready.\n\nBest Regards "
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	# server.ehlo()
	# server.starttls()
	# server.ehlo()
	server.login(youremail, yourpassword)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)