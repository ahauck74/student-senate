from flask import Flask, render_template, json, request, redirect, url_for, abort
from forms import RerecForm, RecForm
import mysql.connector

app = Flask("Sprint2")

mydb = mysql.connector.connect(
  host="cs358.cis.valpo.edu",
  user="senate",
  password='358senate',
  database="senate"
)

##########################################
# The Homepage
##########################################
@app.route("/")
@app.route("/home")

def homepage():
	return render_template("homepage.html")

##########################################
# The Recognition Form
##########################################
@app.route("/new-rec", methods=['POST', 'GET'])
def new_rec():
	
	
	return render_template("recognition_form.html")
	
##########################################
# The Submit Button For the Rec Form
##########################################
@app.route("/new-rec-submission", methods=['POST', 'GET'])
def new_rec_submission():
	#If the user tries to access this page by means other than the submit button, they are redirected to the form
	if request.method == "GET":
		return render_template("recognition_form.html") 
		
	# read the posted values from the UI
	else:
		form = RecForm(request)
		errors = form.validate()
		if (errors):
			return(errors)
		else:
			
			
			mycursor = mydb.cursor()
			sql = "INSERT INTO organizations (ORG_LINK_NAME, ORG_NAME, ORG_ACR, ORG_EMAIL, ORG_DESCRIPTION, CONSTITUTION, ORG_MEMBERS, ORG_ATTENDING_MEMBERS) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
			
			
			val = (form.get_org_link(), form.org_name, form.org_acronym, form.org_email, form.description, None, form.num_members, form.attendance, form.ORG_ID)
			mycursor.execute(sql, val)
			mydb.commit()

			print(mycursor.rowcount, "record inserted.")
			return ("Updated database") #TODO: Render org template for the org that was updated, maybe...

##########################################
# Wait... Who are you?
##########################################
@app.route("/new-rerec", methods=['POST', 'GET'])
def who_rerec():	
			
	if request.method == "GET":
		mycursor = mydb.cursor()
		mycursor.execute("SELECT ORG_NAME, ORG_ID FROM organizations")
		org_name_list = mycursor.fetchall()
		
		#TODO: The below code is a VERY roundabout way of formatting this list properly. The original fetchall  using just the org_name returns a list of tuples that looks like [('name1,'), ('name2,')... etc with the commas stuck there. This should be fixed.
		names, IDs = [], []
		for row in org_name_list:
			name, ID = row
			names.append(name)
			IDs.append(ID)
		
		return render_template("org_selection_form.html", ORGS = names, ) 
		
	else:
		mycursor = mydb.cursor()
		mycursor.execute("SELECT ORG_NAME, ORG_ACR, ORG_EMAIL, ORG_ID FROM organizations WHERE ORG_NAME = '" + str(request.form['org']) + "'" )
		fetch = mycursor.fetchall()
		#return(str(fetch[0]))
		return render_template("rerecognition_form.html", NAME=fetch[0][0], ACR=fetch[0][1], EMAIL=fetch[0][2], ID=fetch[0][3])
			
		
##########################################
# The Re-Recognition Form
##########################################
'''
@app.route("/new-rerec/", methods=['POST', 'GET'])
def new_rerec():
	
	return render_template("rerecognition_form.html") 
	'''

##########################################
# The Submit Button For the Re-Rec Form
##########################################
@app.route("/new-rerec-submission/<ID>", methods=['POST', 'GET'])
def new_submission_rerec(ID):
	#If the user tries to access this page by means other than the submit button, they are redirected to the form
	if request.method == "GET":
		return render_template("rerecognition_form.html", ID=ID) 
		
	# read the posted values from the UI
	else:
		form = RerecForm(request)
		errors = form.validate()
		if (errors):
			return(errors)
		else:
			
			mycursor = mydb.cursor()
			#TODO: Update the database
			sql_update_query = """UPDATE organizations SET ORG_LINK_NAME = %s, ORG_NAME= %s, ORG_ACR= %s, ORG_EMAIL= %s, TIER_REQUEST= %s, ORG_DESCRIPTION= %s, CONSTITUTION= %s, ORG_MEMBERS= %s, ORG_ATTENDING_MEMBERS= %s WHERE ORG_ID = %s"""
			
			val = (form.get_org_link(), form.org_name, form.org_acronym, form.org_email, form.tier_dest, form.description, None, form.num_members, form.attendance, ID)
			mycursor.execute(sql_update_query, val)
			mydb.commit()

			print(mycursor.rowcount, "record inserted.")
			return ("Insderted into the database") #TODO: Render the template for the org that just submitted, maybe...

##########################################
# The Advisor/Officer Change Form
##########################################
@app.route("/advisor-officer-change", methods=['POST', 'GET'])
def new():
	return render_template("advisor_officer_change_form.html") 


		
##########################################
# The Org List
##########################################
@app.route("/orgs")
@app.route("/orgs/")
def org_list():
	cursor = mydb.cursor()
	cursor.execute("SELECT ORG_NAME, ORG_ACR, ORG_EMAIL FROM organizations")
	rows = cursor.fetchall()
	#return str(rows)
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

	return render_template("org_list.html", NAMES=names, ACRS=ACRs, EMAILS=emails)

		
##########################################
# Individual Org Page
##########################################

@app.route("/orgs/<ID>")
def org_page(ID):
	
	
	#Check the database for this org
	cursor = mydb.cursor()
	cursor.execute("SELECT ORG_NAME, ORG_ACR, ORG_EMAIL FROM organizations WHERE ORG_ID = " + str(ID))
	rows = cursor.fetchall()
	
	return str(rows)
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
	"""
	
	return render_template("org_ind.html", ID=ID, NAME=name, ACR=ACR, DESC=desc, EMAIL=email)
	
	
	

