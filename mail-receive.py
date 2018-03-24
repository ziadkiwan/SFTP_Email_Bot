import imaplib
import email
import sched,time
import REQUESTSERVER
import authgen
import dbconnector
import sendemail
import threading
fromuser = "";
headermail = "";
dateofmail = "";
increment = 0;
#istryingagain=False;
#isnew = False;
idtoupdate = 0;

youremail = "EMAILHERE"
yourpassword = "PASSWORDHERE"
keyword = "DATA"

def saveuser(idtoupdate,headermail,fromuser,increment,dateofmail, isnew):
	if(isnew):
		# with open("/home/serv/Desktop/isold", "a") as myfile:
		# 			   myfile.write(headermail+","+fromuser+",0,"+dateofmail+"\n")
		result = dbconnector.saveuser(idtoupdate,headermail,fromuser, increment,dateofmail,isnew)
	else:
		result = dbconnector.saveuser(idtoupdate,headermail,fromuser, increment,dateofmail,isnew)
	return result
		# print(headermail+","+fromuser+","+str(int(increment)+1)+","+dateofmail+"\n")
		# for line in fileinput.input('isold', inplace=True):
		# 		print line.rstrip().replace(headermail+","+fromuser+","+increment+","+dateofmail+"\n", headermail+","+fromuser+","+str(int(increment)+1)+","+dateofmail+"\n"),

def readmailbox():
	print "Checking Mailbox...."
	isareaquestmail = False;
	try:
		url = "imap.gmail.com"
		mail = imaplib.IMAP4_SSL(url, 993)
		user, password = (youremail, yourpassword)
		mail.login(user, password)
	except Exception as e:
		print e
	#print(mail.list())
	mail.select("INBOX") # connect to inbox.
	result, data = mail.search(None, "ALL")
	ids = data[0] # data is a list.
	id_list = ids.split() # ids is a space separated string
	latest_email_id = id_list[-1] # get the latest
	#with open('isold') as f:
	#	content = f.readlines()
	result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
	#date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
	   # print(date)
	#result, data = mail.uid('search',"(RFC822)", '(HEADER Subject "test")')
		#print(data)
	isnew = False;
	istryingagain = False;
	for response_part in data:
		 if isinstance(response_part, tuple):
				msg = email.message_from_string(response_part[1])
				for header in [ 'subject', 'to', 'from','date' ]:
#		            print '%-8s: %s' % (header.upper(), msg[header])
					if 'SUBJECT' in header.upper():
						print("SUBJECT:"+msg[header])
						if keyword in msg[header]:
							 headermail = msg[header]
							 isareaquestmail = True
					if 'FROM' in header.upper():
					   print("FROM:"+msg[header])
					   fromuser = msg[header];
					if 'DATE' in header.upper():
					   print("DATE:"+msg[header])
					   dateofmail = msg[header].split(",")[1];
	if(isareaquestmail):
		content = dbconnector.checkuser(headermail,fromuser);
		if len(content)==0:
			isnew = True
			# lastid = saveuser(0,headermail,fromuser,0,dateofmail,True)
			# if(lastid!= 9999999):
			# 	if not REQUESTSERVER.running():
			# 		authgen.startauth(lastid,fromuser)
		else:
			for i in range(len(content)):
				if (content[i][4] not in dateofmail and content[i][3] <=2):
					print(1)
					istryingagain=True;
					idtoupdate = content[i][0]
					increment = content[i][3]
				#elif (content[i][1] in headermail) and (content[i][2] in fromuser) and (content[i][3] <=2) and (content[i][4] not in dateofmail):
				#		print(2)
				#		istryingagain=True
				#		idtoupdate = content[i][0]
				#		increment = content[i][3]
	if(isnew):
		if not REQUESTSERVER.running():
			print(fromuser+"is new!")
			isnew=False
			lastid = saveuser(0 ,headermail ,fromuser ,0 ,dateofmail, True)
			if(lastid!= 9999999):
				thread = threading.Thread(target=authgen.startauth,args=(lastid,fromuser))
				thread.daemon = True
				thread.start()
				#authgen.startauth(lastid,fromuser)
		else:
			print("BUSY - New")
			if (len(dbconnector.checkuserwaiting(headermail,fromuser,dateofmail))==0):
				lastid = saveuser(0, headermail, fromuser, 0, dateofmail, True)
				if(lastid!= 9999999):
					if(len(dbconnector.checkwaitinglist(lastid))==0):
						dbconnector.markaswaitingnew(lastid)
						sendemail.sendruningmail(fromuser)
	elif(istryingagain):
		if not REQUESTSERVER.running():
			istryingagain=False
			print(fromuser+"is trying again!")
			lastid = saveuser( idtoupdate, headermail, fromuser, increment,dateofmail, False)
			if(lastid!= 9999999):
				print("LASTID")
				print lastid
				thread = threading.Thread(target=authgen.startauth, args=(lastid, fromuser))
				thread.daemon = True
				thread.start()
				dbconnector.removewaiting(lastid)
		else:
			print("BUSY - Trying Again")
			waiting = dbconnector.checkuser(headermail,fromuser)
			if(len(waiting)!=0):
				if(len(dbconnector.checkwaitinglist(int(waiting[0][0])))==0):
					dbconnector.markaswaitingnew(waiting[0][0])
					sendemail.sendruningmail(fromuser)
	print "Checking Waiting List...."
	if not REQUESTSERVER.running():
		waitinglist = dbconnector.getallwaiting();
		if (len(waitinglist) != 0):
				result = dbconnector.updatewaiting(waitinglist[0][0])
				if (result):
					thread = threading.Thread(target=authgen.startauth, args=(waitinglist[0][3], waitinglist[0][5]))
					thread.daemon = True
					thread.start()
	time.sleep(60)
while(True):
	readmailbox()

#raw_email = data[0][1] # here's the body, which is raw text of the whole email
#print(raw_email)
# including headers and alternate payloads
