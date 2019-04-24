from flask import Flask, render_template, json, request, redirect, url_for, abort, flash, make_response
from forms import RerecForm, RecForm, OfficerForm, AdvisorForm, SenateLoginForm
import email_test
import mysql.connector
import datetime
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message, Mail
import os

app = Flask("Sprint2")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #Maybe prevents an issue with static files being cached in the browser, remove in final product
app.config['SECRET_KEY'] = 'endgame'
app.config['SECURITY_PASSWORD_SALT'] = 'luxury'
app.config['MAIL_DEFAULT_SENDER'] = "weregoingupton@gmail.com"

# mail settings
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# gmail authentication
app.config['MAIL_USERNAME'] = 'weregoingupton'
app.config['MAIL_PASSWORD'] = 'Upton2016'


#app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


mail = Mail(app)
mydb = mysql.connector.connect(
  host="cs358.cis.valpo.edu",
  user="senate",
  password='358senate',
  database="senate"
)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
           
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email
    
def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

##########################################
# The Homepage
##########################################
@app.route("/")
@app.route("/home")

def homepage():
	isSenate = request.cookies.get('userID') == 'senate'
	
	return render_template("homepage.html", LOGIN=isSenate)
	
##########################################
# Senate Login
##########################################
@app.route("/login", methods=['POST', 'GET'])

def login():
	
	if request.method == 'GET':
		return render_template("senate_login.html")

	else:
		login = SenateLoginForm(request)
		errors = login.validate()
		if (errors):
			return render_template("senate_login.html", ERRORS=errors)
		else:
			flash('Login successful.')
			
			resp = make_response(redirect("home"))
			resp.set_cookie('userID', login.user)
			
			return resp
			
##########################################
# Senate Login
##########################################
@app.route("/logout")

def logout():
	
	resp = make_response(redirect("home"))
	resp.set_cookie('userID', '', expires=0)
	
	return resp
	
	
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
					 ORG_ATTENDING_MEMBERS, TIER_REQUEST) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
			val = (form.org_name, form.org_acronym, form.org_email, form.description, None, form.num_members, form.attendance, 'Unfunded')
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
		sql = """SELECT ORG_NAME, ORG_EMAIL FROM organizations WHERE ORG_ID = '""" + str(request.form['org']) + "'" 
		mycursor.execute(sql)
		email = mycursor.fetchall()[0][1]
		token = generate_confirmation_token(email)
		confirm_url = url_for('confirm_email', token=token, _external=True)
		html = render_template('email.html', confirm_url=confirm_url)
		subject = "Please confirm your email"
		send_email(email, subject, html)

		flash('A confirmation email has been sent via email.', 'success')
		return redirect('home')
			
		
		
##########################################
# Email Verification
##########################################
			
@app.route('/confirm/<token>')
def confirm_email(token):
	try:
		email = confirm_token(token)
	except:
		flash('The confirmation link is invalid or has expired.', 'danger')



	mycursor = mydb.cursor()
	sql = """SELECT ORG_NAME, ORG_ACR, ORG_EMAIL, ORG_ID, ORG_DESCRIPTION, CONSTITUTION, ORG_MEMBERS, ORG_ATTENDING_MEMBERS, CURRENT_TIER FROM organizations WHERE 
	ORG_EMAIL = '""" + str(email) + "'" 
	mycursor.execute(sql)
	fetch = mycursor.fetchall()
	ID = str(fetch[0][3])
	
	sql = 'SELECT OFFICER_NAME, OFFICER_PHONE, OFFICER_EMAIL, TITLE FROM officers WHERE ORG_ID = ' + ID
	mycursor.execute(sql)
	officer_list = mycursor.fetchall()
	
	sql = sql = 'SELECT ADVISOR_NAME, ADVISOR_PHONE, ADVISOR_EMAIL FROM advisors WHERE ORG_ID = ' + ID
	mycursor.execute(sql)
	advisor_list = mycursor.fetchall()
	
	#TODO: Add officer/advisor info here, and make this cleaner.
	return render_template("rerecognition_form.html", NAME=fetch[0][0], ACR=fetch[0][1], EMAIL=fetch[0][2], ID=fetch[0][3], DESC=fetch[0][4], CONSTITUTION=fetch[0][5], MEMBERS=fetch[0][6], ATTENDANCE=fetch[0][7], TIER=fetch[0][8], OFF_LIST = officer_list, ADV_LIST = advisor_list)
	

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
			sql_update_query = """
			UPDATE organizations
			SET ORG_NAME=%s, ORG_ACR=%s, ORG_EMAIL=%s, TIER_REQUEST=%s, ORG_DESCRIPTION=%s, CONSTITUTION=%s, ORG_MEMBERS=%s,ORG_ATTENDING_MEMBERS=%s, APPROVAL_STATUS=%s
			WHERE ORG_ID = %s"""
			val = (form.org_name, form.org_acronym, form.org_email, form.tier_dest, form.description, None, form.num_members, form.attendance, None, ID)
			mycursor.execute(sql_update_query, val)
			mydb.commit()
			
			#ID = str(mycursor.lastrowid) #The ID for the last insert done by this cursor object
			
			sql_delete_query = "DELETE FROM officers WHERE ORG_ID = " + ID
			mycursor.execute(sql_delete_query)
			
			sql_insert_query = """INSERT INTO officers (OFFICER_NAME, OFFICER_PHONE, OFFICER_EMAIL, TITLE, ORG_ID, YEAR) VALUES (%s, %s, %s, %s, %s, %s)"""
			for i in range(form.num_officers):
				val = (form.off_names[i], form.off_phones[i], form.off_emails[i], form.off_pos[i], ID, datetime.datetime.now().year)
				mycursor.execute(sql_insert_query, val)
			mydb.commit()
			
			sql_delete_query = "DELETE FROM advisors WHERE ORG_ID = " + ID
			mycursor.execute(sql_delete_query)
			
			sql_insert_query = """INSERT INTO advisors (ADVISOR_NAME, ADVISOR_PHONE, ADVISOR_EMAIL, ORG_ID) VALUES (%s, %s, %s, %s)"""
			for i in range(form.num_advisors):
				val = (form.adv_names[i], form.adv_phones[i], form.adv_emails[i], ID)
				mycursor.execute(sql_insert_query, val)
			mydb.commit()
			
			return redirect('/orgs/'+ str(ID))
			
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
			advisor_list = mycursor.fetchall()
			
			
			return render_template("advisor_change_form.html", ADV_LIST=advisor_list, ID=ID)


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
@app.route("/new-advisors-submission/<ID>", methods=['POST'])
def advisor_change(ID):

	# read the user input into the RerecForm class
	form = AdvisorForm(request)
	errors = form.validate()
	if (errors):
		return(errors)
	else:
		
		mycursor = mydb.cursor()	
		
		sql_delete_query = "DELETE FROM advisors WHERE ORG_ID = " + ID
		mycursor.execute(sql_delete_query)
		sql_insert_query = """INSERT INTO advisors (ADVISOR_NAME, ADVISOR_PHONE, ADVISOR_EMAIL, ORG_ID, YEAR) VALUES (%s, %s, %s, %s, %s, %s)"""
		for i in range(form.num_advisors):
			val = (form.adv_names[i], form.adv_phones[i], form.adv_emails[i], ID, datetime.datetime.now().year)
			mycursor.execute(sql_insert_query, val)
		mydb.commit()

	return redirect('orgs/'+ str(ID))
	

##########################################
# The Org List
##########################################
@app.route("/orgs/")
@app.route("/orgs")
def org_list():

	cursor = mydb.cursor()
	cursor.execute("SELECT ORG_NAME, ORG_ACR, ORG_EMAIL, ORG_ID, CURRENT_TIER, TIER_REQUEST, APPROVAL_STATUS FROM organizations")
	rows = cursor.fetchall()
	names, ACRs, emails, IDs, tiers, tier_reqs, statuses = [], [], [], [], [], [], []
	
	for row in rows:
		name, ACR, email, ID, tier, tier_req, status = row
		names.append(name)
		ACRs.append(ACR)
		emails.append(email)
		IDs.append(ID)
		tiers.append(tier)
		tier_reqs.append(tier_req)
		statuses.append(status)
		
	
	return render_template("org_list.html", NAMES=names, ACRS=ACRs, EMAILS=emails, IDS=IDs, TIERS=tiers)
			
	
##########################################
# Org Approvals
##########################################
@app.route("/orgs-approval", methods=['POST', 'GET'])
@app.route("/orgs-approval/", methods=['POST', 'GET'])
def org_approval():

	if request.method == 'GET':
		cursor = mydb.cursor()
		cursor.execute("SELECT ORG_NAME, ORG_ACR, ORG_EMAIL, ORG_ID, CURRENT_TIER, TIER_REQUEST, APPROVAL_STATUS FROM organizations")
		rows = cursor.fetchall()
		names, ACRs, emails, IDs, tiers, tier_reqs, statuses = [], [], [], [], [], [], []
		
		for row in rows:
			name, ACR, email, ID, tier, tier_req, status = row
			if not status: 
				names.append(name)
				ACRs.append(ACR)
				emails.append(email)
				IDs.append(ID)
				tiers.append(tier)
				tier_reqs.append(tier_req)
				statuses.append(status)
			
		isSenate = request.cookies.get('userID') == 'senate'
		
		if isSenate:
			return render_template("org_list_form.html", NAMES=names, ACRS=ACRs, EMAILS=emails, IDS=IDs, TIERS=tiers, TIER_REQS=tier_reqs, STATUSES=statuses)
			
		else:
			return render_template("org_list.html", NAMES=names, ACRS=ACRs, EMAILS=emails, IDS=IDs, TIERS=tiers)
			
	else:
		mycursor = mydb.cursor()
		org_statuses, org_IDs = [], []
		for i in range(int(len(request.form)/2)):
			org_statuses.append(request.form['status' + str(i)])
			org_IDs.append(request.form['org_ID' + str(i)])
			
			if org_statuses[i] == 'accept':
				sql = "UPDATE organizations SET CURRENT_TIER=TIER_REQUEST, TIER_REQUEST=NULL, APPROVAL_STATUS=TRUE WHERE ORG_ID = " + str(org_IDs[i])
				mycursor.execute(sql)
				
			elif org_statuses[i] == 'reject':
				sql = "DELETE FROM organizations WHERE ORG_ID = " + str(org_IDs[i])
				mycursor.execute(sql)
				
			elif org_statuses[i] == 'reject_tier':
				sql = "UPDATE organizations SET TIER_REQUEST=NULL, APPROVAL_STATUS=TRUE WHERE ORG_ID = " + str(org_IDs[i])
				mycursor.execute(sql)
		mydb.commit()
		
		return(redirect('home'))
		
##########################################
# Archives
##########################################
@app.route("/archives")
@app.route("/archives/")
def archives():
	cursor = mydb.cursor()
	cursor.execute("SELECT ORG_NAME, ORG_ACR, ORG_EMAIL, ORG_ID, TIER, CHANGE_DATE FROM archives")
	rows = cursor.fetchall()
	names, ACRs, emails, IDs, tiers, dates, years = [], [], [], [], [], [], []

	
	for row in rows:
		name, ACR, email, ID, tier, date = row
		names.append(name)
		ACRs.append(ACR)
		emails.append(email)
		IDs.append(ID)
		tiers.append(tier)
		dates.append(date)
		years.append(date.year)
		
	years = sorted(set(years))
		
	

	return render_template("archives.html", NAMES=names, ACRS=ACRs, EMAILS=emails, IDS=IDs, TIERS=tiers, DATES=dates, YEARS=years)

		
##########################################
# Individual Org Page
##########################################

@app.route("/orgs/<ID>")
def org_page(ID):
	
	
	#Check the database for this org
	mycursor = mydb.cursor()
	mycursor.execute("SELECT ORG_ID, ORG_NAME, ORG_ACR, ORG_DESCRIPTION, ORG_EMAIL FROM organizations WHERE ORG_ID = " + str(ID))
	rows = mycursor.fetchall()
	
	
	
	#Aborts (teapot) if someone tries to query an org that doesn't exist
	if rows == []:
		abort(418)
	
	ID, name, ACR, desc, email = rows[0]
	ID = str(ID)
	
	sql = 'SELECT OFFICER_NAME, OFFICER_PHONE, OFFICER_EMAIL, TITLE FROM officers WHERE ORG_ID = ' + ID
	mycursor.execute(sql)
	officer_list = mycursor.fetchall()
	
	sql = sql = 'SELECT ADVISOR_NAME, ADVISOR_PHONE, ADVISOR_EMAIL FROM advisors WHERE ORG_ID = ' + ID
	mycursor.execute(sql)
	advisor_list = mycursor.fetchall()

	return render_template("org_ind.html", ID=ID, NAME=name, ACR=ACR, DESC=desc, EMAIL=email, OFF_LIST=officer_list, ADV_LIST=advisor_list)
	
	
	

