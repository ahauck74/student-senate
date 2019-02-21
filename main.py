from flask import Flask, render_template, json, request, redirect, url_for

app = Flask("Sprint2")

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
		#The string in the bracket matches the field name in the html
		_org_name = request.form['org_name'] 
		_org_email = request.form['org_email']
		_org_acronym = request.form['acronym']
		
		#These fields will need to become arrays once we dress up the html to have a 
		#variable number of officer fields
		_name = request.form['name'] 
		_phone = request.form['phone'] 
		_email = request.form['email'] 
		_position = request.form['position']
			
		_cur_recgonized = request.form['currently_recognized']#returns <y> or <n>
		_last_recognized = request.form['last_recognized']#This will likely be removed
		_cur_tier = request.form['tier']#<1>, <2>, <3>, or <null> for unfunded
		_change_tier = request.form['change_tier']#<y> or <n>
		_tier_dest = request.form['tier_destination']#<1>, <2>, <3>, or <null> for unfunded
		_description = request.form['description']
		_events = request.form['events']
		_attendance = request.form['reg_attendance']
		_members = request.form['members_total']
		
		
		# validate the received values
		if _org_name and _org_email:
		    return ("<h1>" + _org_name + "</h1>")
		else:
		    return (redirect(url_for('new')))

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
