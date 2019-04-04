from flask import Flask, render_template, json, request, redirect, url_for, abort
from forms import RerecForm, RecForm, OfficerForm
import mysql.connector
import datetime

app = Flask("Sprint2")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #Maybe prevents an issue with static files being cached in the browser, remove in final product

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
		
	
	else:
		# read the posted values from the form
		form = RecForm(request)
		errors = form.validate()
		if (errors):
			return(errors)
		else:
			
			mycursor = mydb.cursor()
			#Insert org info to the database
			sql = """INSERT INTO organizations (ORG_NAME, ORG_ACR, ORG_EMAIL, ORG_DESCRIPTION, CONSTITUTION, ORG_MEMBERS, 			 
					 ORG_ATTENDING_MEMBERS) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
			val = (form.org_name, form.org_acronym, form.org_email, form.description, None, form.num_members, form.attendance)
			mycursor.execute(sql, val)
			mydb.commit()
			
			ID = mycursor.lastrowid #The ID for the last insert done by this cursor object
			
			sql_insert_query = """INSERT INTO officers (OFFICER_NAME, OFFICER_PHONE, OFFICER_EMAIL, TITLE, ORG_ID, YEAR) VALUES (%s, %s, %s, %s, %s, %s)"""
			for i in range(form.num_officers):
				val = (form.off_names[i], form.off_phones[i], form.off_emails[i], form.off_pos[i], ID, datetime.datetime.now().year)
				mycursor.execute(sql_insert_query, val)
			mydb.commit()
			
			sql_insert_query = """INSERT INTO advisors (ADVISOR_NAME, ADVISOR_PHONE, ADVISOR_EMAIL, ORG_ID) VALUES (%s, %s, %s, %s)"""
			for i in range(form.num_advisors):
				val = (form.adv_names[i], form.adv_phones[i], form.adv_emails[i], ID)
				mycursor.execute(sql_insert_query, val)
			mydb.commit()
			

			return redirect('orgs/'+ str(ID))

##########################################
# The Rerec Form
##########################################
@app.route("/new-rerec", methods=['POST', 'GET'])
def who_rerec():	
			
	if request.method == "GET":
		mycursor = mydb.cursor()
		mycursor.execute("SELECT ORG_NAME, ORG_ID FROM organizations")
		org_name_list = mycursor.fetchall()
		
		#TODO: The below code is a VERY roundabout way of formatting this list properly. The original fetchall  using just the org_name returns a list of 
		#tuples that looks like [('name1,'), ('name2,')... etc with the commas stuck there. This should be fixed.
		names, IDs = [], []
		for row in org_name_list:
			name, ID = row
			names.append(name)
			IDs.append(ID)
		
		return render_template("org_selection_form.html", ORGS = names, IDS = IDs) 
		
	else:
		mycursor = mydb.cursor()
		sql = """SELECT ORG_NAME, ORG_ACR, ORG_EMAIL, ORG_ID, ORG_DESCRIPTION, CONSTITUTION, ORG_MEMBERS, ORG_ATTENDING_MEMBERS FROM organizations WHERE 
		ORG_ID = '""" + str(request.form['org']) + "'" 
		mycursor.execute(sql)
		fetch = mycursor.fetchall()
		
		#TODO: Add officer/advisor info here, and make this cleaner.
		return render_template("rerecognition_form.html", NAME=fetch[0][0], ACR=fetch[0][1], EMAIL=fetch[0][2], ID=fetch[0][3], DESC=fetch[0][4], CONSTITUTION=fetch[0][5], MEMBERS=fetch[0][6], ATTENDANCE=fetch[0][7])
			

##########################################
# The Submit Button For the Re-Rec Form
##########################################
@app.route("/new-rerec-submission/<ID>", methods=['POST', 'GET'])
def new_submission_rerec(ID):
	#If the user tries to access this page by means other than the submit button, they are redirected to the form
	if request.method == "GET":
		return render_template("rerecognition_form.html", ID=ID) 
		
	
	else:
		# read the user input into the RerecForm class
		form = RerecForm(request)
		errors = form.validate()
		if (errors):
			return(errors)
		else:
			
			mycursor = mydb.cursor()	
			sql_update_query = """UPDATE organizations ORG_NAME= %s, ORG_ACR= %s, ORG_EMAIL= %s, TIER_REQUEST= %s, ORG_DESCRIPTION= %s, CONSTITUTION= %s, ORG_MEMBERS= %s, ORG_ATTENDING_MEMBERS= %s WHERE ORG_ID = %s"""
			val = (form.org_name, form.org_acronym, form.org_email, form.tier_dest, form.description, None, form.num_members, form.attendance, ID)
			mycursor.execute(sql_update_query, val)
			mydb.commit()
			
			ID = mycursor.lastrowid #The ID for the last insert done by this cursor object
			
			sql_insert_query = """INSERT INTO officers (OFFICER_NAME, OFFICER_PHONE, OFFICER_EMAIL, TITLE, ORG_ID, YEAR) VALUES (%s, %s, %s, %s, %s, %s)"""
			for i in range(form.num_officers):
				val = (form.off_names[i], form.off_phones[i], form.off_emails[i], form.off_pos[i], ID, datetime.datetime.now().year)
				mycursor.execute(sql_insert_query, val)
			mydb.commit()
			
			sql_insert_query = """INSERT INTO advisors (ADVISOR_NAME, ADVISOR_PHONE, ADVISOR_EMAIL, ORG_ID) VALUES (%s, %s, %s, %s)"""
			for i in range(form.num_advisors):
				val = (form.adv_names[i], form.adv_phones[i], form.adv_emails[i], ID)
				mycursor.execute(sql_insert_query, val)
			mydb.commit()
			
			return redirect('orgs/'+ str(ID))
			
####################################################
# Org Select For The Advisor/Officer Change Prompt
####################################################
@app.route("/off-adv-change-prompt/", methods=['GET', 'POST'])
@app.route("/off-adv-change-prompt/<ID>", methods=['GET', 'POST'])

def off_adv_change_prompt(ID=None):	
			
	if request.method == "GET":
		mycursor = mydb.cursor()
		mycursor.execute("SELECT ORG_NAME, ORG_ID FROM organizations")
		org_name_list = mycursor.fetchall()
		
		#TODO: The below code is a VERY roundabout way of formatting this list properly. The original fetchall  using just the org_name returns a list of 
		#tuples that looks like [('name1,'), ('name2,')... etc with the commas stuck there. This should be fixed.
		names, IDs = [], []
		for row in org_name_list:
			name, ID = row
			names.append(name)
			IDs.append(ID)
		
		return render_template("org_select_adv_off.html", ORGS = names, IDS = IDs) 
		
	else:
		mode = request.form['radAnswer'] #Either <officer> or <advisor>
		ID = request.form['org'] #Gets the ID of the selected org
		if mode == 'officer':
			mycursor = mydb.cursor()
			sql = 'SELECT OFFICER_NAME, OFFICER_PHONE, OFFICER_EMAIL, TITLE FROM officers WHERE ORG_ID = ' + ID
			mycursor.execute(sql)
			officer_list = mycursor.fetchall()
			
			#return str(fetch)
			return render_template("officer_change_form.html", OFF_LIST=officer_list, ID=ID)
		
		elif mode == 'advisor':
			mycursor = mydb.cursor()
			sql = sql = 'SELECT ADVISOR_NAME, ADVISOR_PHONE, ADVISOR_EMAIL FROM advisors WHERE ORG_ID = ' + ID
			mycursor.execute(sql)
			fetch = mycursor.fetchall()
			
			
			return render_template("advisor_change_form.html")


##########################################
# The Officer Change Form
##########################################
@app.route("/new-officers-submission/<ID>", methods=['POST'])
def officer_change(ID):

	# read the user input into the RerecForm class
	form = OfficerForm(request)
	errors = form.validate()
	if (errors):
		return(errors)
	else:
		
		mycursor = mydb.cursor()	
		
		sql_delete_query = "DELETE FROM officers WHERE ORG_ID = " + ID
		mycursor.execute(sql_delete_query)
		sql_insert_query = """INSERT INTO officers (OFFICER_NAME, OFFICER_PHONE, OFFICER_EMAIL, TITLE, ORG_ID, YEAR) VALUES (%s, %s, %s, %s, %s, %s)"""
		for i in range(form.num_officers):
			val = (form.off_names[i], form.off_phones[i], form.off_emails[i], form.off_pos[i], ID, datetime.datetime.now().year)
			mycursor.execute(sql_insert_query, val)
		mydb.commit()

	return redirect('orgs/'+ str(ID))


##########################################
# The Advisor Change Form
##########################################
@app.route("/advisor-officer-change", methods=['POST', 'GET'])
def advisor_change():

	return render_template("advisor_change_form.html") 
	

##########################################
# The Org List
##########################################
@app.route("/orgs")
@app.route("/orgs/")
def org_list():
	cursor = mydb.cursor()
	cursor.execute("SELECT ORG_NAME, ORG_ACR, ORG_EMAIL, ORG_ID FROM organizations")
	rows = cursor.fetchall()
	names = []
	ACRs = []
	emails = []
	IDS = []
	
	for row in rows:
		name, ACR, email, ID = row
		names.append(name)
		ACRs.append(ACR)
		emails.append(email)
		IDS.append(ID)
	
	#return str(names) + "<br>" + str(emails) + "<br>" + str(ACRs)

	#Sawyer

	return render_template("org_list.html", NAMES=names, ACRS=ACRs, EMAILS=emails, IDS=IDS)

		
##########################################
# Individual Org Page
##########################################

@app.route("/orgs/<ID>")
def org_page(ID):
	
	
	#Check the database for this org
	cursor = mydb.cursor()
	cursor.execute("SELECT ORG_ID, ORG_NAME, ORG_ACR, ORG_DESCRIPTION, ORG_EMAIL FROM organizations WHERE ORG_ID = " + str(ID))
	rows = cursor.fetchall()
	
	
	
	#Aborts (teapot) if someone tries to query an org that doesn't exist
	if rows == []:
		abort(418)
	
	ID, name, ACR, desc, email = rows[0]
	
	"""
	ID = 315
	name = "Testy McTestClub"
	ACR = "McTestClub"
	desc = "I'm a testing platform for Sawyer's template. If you see me in production, something's gone horribly wrong."
	email = "test@testymctestclub.valpo.edu"
	"""
	
	return render_template("org_ind.html", ID=ID, NAME=name, ACR=ACR, DESC=desc, EMAIL=email)
	
	
	

