#Jackson Heise

import smtplib
from os import urandom

def sendVerificationCode(dest_email):
	
	#Email verification code information
	username = "weregoingupton"
	password = "Upton2016"
	source_email = "weregoingupton@gmail.com"
	
	#Generate the code
	x = urandom(5)
	code = x.hex()
	
	#Generate the email text
	msg = "Hello! Your Student Senate login code is:\n" + code
	
	#Create and log in to the server
	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()			#Send an echo message to the system
	except:
		return "CONNECTERROR"
		
	try:
		server.starttls()		#Enable Secure Connection
	except:
		return "SECURERROR"
		
	try:
		server.login(username, password)
	except:
		return "LOGINERROR"
	
	#Send the email itself
	try:
		server.sendmail(source_email, dest_email, msg)
	except:
		return "SENDMAILERROR"

	#return the email code
	return code

if __name__ == "__main__":
	code = sendVerificationCode("alec.hauck@valpo.edu")
	print(code)
	
