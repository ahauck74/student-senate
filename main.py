from flask import Flask, render_template, json, request, redirect, url_for, abort
from forms import RerecForm
import mysql.connector

app = Flask("Sprint2")

mydb = mysql.connector.connect(
  host="cs358.cis.valpo.edu",
  user="senate",
  password='358senate',
  database="senate"
)

@app.route("/")
def homepage():
	return render_template("homepage.html")

############################
# The Form
############################
@app.route("/new", methods=['POST', 'GET'])
def new():
	return render_template("new_submission.html")

############################
# The Submit Button
############################
@app.route("/new-submission", methods=['POST', 'GET'])
def new_submission():
	#If the user tries to access this page by means other than the submit button, they are redirected to the form
	if request.method == "GET":
		return render_template("new_submission.html") 
		
	# read the posted values from the UI
	else:
		form = RerecForm(request)
		errors = form.validate()
		if (errors):
			return(errors)
		else:
			
			mycursor = mydb.cursor()
			sql = "INSERT INTO organizations (ORG_NAME, ORG_ACR, ORG_DESCRIPTION, ORG_EMAIL) VALUES (%s, %s, %s, %s)"
			
			val = (form.org_name, form.org_acronym, form.description, form.org_email)
			mycursor.execute(sql, val)
			mydb.commit()
			'''
			sql = "INSERT INTO org_record (ORG_NAME, ORG_ACR, ORG_DESCRIPTION, ORG_EMAIL) VALUES (%s, %s, %s, %s)"
			
			val = (form.org_name, self.org_acronym, self.description, self.org_email)
			mycursor.execute(sql, val)
			mydb.commit()
			'''

			print(mycursor.rowcount, "record inserted.")
			
			return("ready to commit to database")
		


############################
# The Org List
############################
@app.route("/orgs")
@app.route("/orgs/")
def org_list():
	cursor = mydb.cursor()
	cursor.execute("SELECT ORG_NAME, ORG_ACR, ORG_EMAIL FROM organizations")
	rows = cursor.fetchall()
	
	names = []
	ACRs = []
	emails = []
	
	for row in rows:
		name, ACR, email = row
		names.append(name)
		ACRs.append(ACR)
		emails.append(email)
	
	#return str(names) + "<br>" + str(emails) + "<br>" + str(ACRs)

	#Sawyer
	try:
		return render_template("club_short.html", NAMES=names, ACRS=ACRs, EMAILS=emails)
	except:
		abort(404)	
		
############################
# Individual Org Page
############################

@app.route("/orgs/<ID>")
def org_page(ID):
	
	"""
	#Check the database for this org
	cursor = mydb.cursor()
	cursor.execute("SELECT ORG_NAME, ORG_ACR, ORG_EMAIL FROM organizations WHERE ID = " + str(ID))
	rows = cursor.fetchall()
	
	#
	#	Account for what happens if two ID's get returned <might not be necessary>
	#
	
	#
	#	Here is where I'll need to account for what will happen if the club ID isn't real.
	#
	
	ID, name, acr, desc, email = row[0]
	"""
	
	ID = 315
	name = "Testy McTestClub"
	ACR = "McTestClub"
	desc = "I'm a testing platform for Sawyer's template. If you see me in production, something's gone horribly wrong."
	email = "test@testymctestclub.valpo.edu"
	
	return render_template("club_full.html", ID=ID, NAME=name, ACR=ACR, DESC=desc, EMAIL=email)
	
	
	

