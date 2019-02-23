from flask import Flask, render_template, json, request, redirect, url_for
from forms import RerecForm
import mysql.connector

app = Flask("Sprint2")

mydb = mysql.connector.connect(
  host="cs358.cis.valpo.edu",
  user="senate",
  password='358senate',
  database="senate"
)

clubs = {"101":"Alliance", 
		"102": "Federation of Authors", 
		"103": "The Insult Rosasco League",
		"104": "The Grand Unified Hairline Project",
		"0": "I have neither given or received, nor have I tolerated others' use of unauthorized aid."
		}

@app.route("/")
def hello():
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
	#If the user tries to access this page by means other than the submit button, they are redirected to 		the form
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
# The Club Pages
############################
@app.route("/clubs")
@app.route("/clubs/")
@app.route("/clubs/<club>")
def club_info(club=None):
	#if no club is selected:
	if(club == None):
		return "<h1>Join a club!</h1>"
		
	
	#Check if the club is in the list:
	if club in clubs.keys():
		return "<h2>This is where we'll have page info for " + clubs[club] + ".</h2>"
	else:
		return "<h2>Cannot find Club with ID: \"" + club + "\".</h2>"
