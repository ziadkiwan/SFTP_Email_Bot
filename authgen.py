import uuid
import REQUESTSERVER
import dbconnector
import sendemail
def random_password(string_length=10):
	"""Returns a random string of length string_length."""
	random = str(uuid.uuid4()) # Convert UUID format to a Python string.
	random = random.upper() # Make all characters uppercase.
	random = random.replace("-","") # Remove the UUID '-'.
	return random[0:string_length] # Return the random string.


def startauth(id,name):
	print("Generating Credentials")

	#with open("authenitcation", "a") as myfile:
	#	myfile.write(name.split(" ")[0]+","+random_password(10)+"\n")
	ranpass = random_password(10);
	lastauthid = dbconnector.generateauth(id,name.split(" ")[0],ranpass)
	if(lastauthid!= 9999999):
		sendemail.sendAuthmail(name, name.split(" ")[0], ranpass)
		REQUESTSERVER.startserver(name.split(" ")[0],ranpass)