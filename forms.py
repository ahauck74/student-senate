class RecForm:
	
	def __init__(self, request):
		#The string in the bracket matches the field name in the html
		self.org_name = request.form['org_name'] 
		self.org_email = request.form['org_email']
		self.org_acronym = request.form['acronym']
		
		#These fields will need to become arrays once we dress up the html to have a 
		#variable number of officer fields
		'''
		self.name = request.form['name'] 
		self.phone = request.form['phone'] 
		self.email = request.form['email'] 
		self.position = request.form['position']
		'''
		self.description = request.form['description']
		self.events = request.form['events']
		self.attendance = request.form['reg_attendance']
		self.num_members = request.form['members_total']
		
		self.num_officers = request.form['num_officers']
		
		
		
	def get_org_link(self):
		return self.org_name.replace(" ","-")
		
	def validate(self):
		error_message = ''
		if not (self.org_name):
			error_message += "Missing organization name.\n"
		if not (self.org_email):
			error_message += "Missing organization email.\n"
		#TODO: Check if valid email using regex, and possibly add other validation requirements
		'''if not isinstance(self.num_officers, int):
			error_message += ("Number of officers needs to be an integer, instead got " + self.num_officers + ".\n")
		if not isinstance(self.num_advisors, int):
			error_message += ("Number of advisors needs to be an integer, instead got " + self.num_advisors + ".\n")'''
		if (self.change_tier == 'y' and not self.tier_dest):
			error_message += "Missing tier destination. Please select a tier or set change tier to no.\n"
		if len(error_message) == 0:
			return None;
		return error_message
		
	def commit_to_database(self):
		#TODO: Write this method
		print('hi')
		
		
class RerecForm:
	
	def __init__(self, request):
		#The string in the bracket matches the field name in the html
		self.org_name = request.form['org_name'] 
		self.org_email = request.form['org_email']
		self.org_acronym = request.form['acronym']
		
		#These fields will need to become arrays once we dress up the html to have a 
		#variable number of officer fields
		'''
		self.name = request.form['name'] 
		self.phone = request.form['phone'] 
		self.email = request.form['email'] 
		self.position = request.form['position']
		'''
		self.is_recgonized = request.form['currently_recognized']#returns <y> or <n>
		self.last_recognized = request.form['last_recognized']#This will likely be removed
		self.cur_tier = request.form['tier']#<1>, <2>, <3>, or <null> for unfunded
		self.change_tier = request.form['change_tier']#<y> or <n>
		self.tier_dest = request.form['tier_destination']#<1>, <2>, <3>, or <null> for unfunded
		self.description = request.form['description']
		self.events = request.form['events']
		self.attendance = request.form['reg_attendance']
		self.num_members = request.form['members_total']
		
		self.num_officers = request.form['num_officers']

	def get_org_link(self):
		return self.org_name.replace(" ","-")
		
	def validate(self):
		error_message = ''
		if not (self.org_name):
			error_message += "Missing organization name.\n"
		if not (self.org_email):
			error_message += "Missing organization email.\n"
		#TODO: Check if valid email using regex, and possibly add other validation requirements
		'''if not isinstance(self.num_officers, int):
			error_message += ("Number of officers needs to be an integer, instead got " + self.num_officers + ".\n")
		if not isinstance(self.num_advisors, int):
			error_message += ("Number of advisors needs to be an integer, instead got " + self.num_advisors + ".\n")'''
		if (self.change_tier == 'y' and not self.tier_dest):
			error_message += "Missing tier destination. Please select a tier or set change tier to no.\n"
		if len(error_message) == 0:
			return None;
		return error_message
		
	def commit_to_database(self):
		#TODO: Write this method
		print('hi')
		
class OfficerForm:
	
	def __init__(self, request):
		self.names, self.phones, self.emails, self.positions = [], [], [], []
		self.num_officers = int((len(request.form)-1)/4) #Divide by the number of unique fields (name,phone,email,pos) and subtract one for the question asking about number of advisors
		for i in range(self.num_officers):
		
			self.names.append(request.form['name' + str(i)])
			self.phones.append(request.form['phone' + str(i)] )
			self.emails.append(request.form['email' + str(i)] )
			self.positions.append(request.form['position' + str(i)] )
			
	def validate(self):
		error_message = ''
		for i in range(self.num_officers):
			if not (self.names[i]):
				error_message += "Missing officer " + str(i+1) + " name.\n"
			if not (self.phones[i]):
				error_message += "Missing officer " + str(i+1) + " phone.\n"
			if not (self.emails[i]):
				error_message += "Missing officer " + str(i+1) + " email.\n"
			if not (self.positions[i]):
				error_message += "Missing officer " + str(i+1) + " position.\n"
		#TODO: Check if valid email using regex, and possibly add other validation requirements
		'''if not isinstance(self.num_officers, int):
			error_message += ("Number of officers needs to be an integer, instead got " + self.num_officers + ".\n")
		if not isinstance(self.num_advisors, int):
			error_message += ("Number of advisors needs to be an integer, instead got " + self.num_advisors + ".\n")'''

		return error_message
		
class AdvisorForm:
	
	def __init__(self, request):
		self.names, self.phones, self.emails, self.positions = [], [], [], []
		self.num_advisors = int(len(request.form)/3) #Divide by the number of fields
		for i in range(self.num_advisors):
		
			self.names.append(request.form['name' + str(i)])
			self.phones.append(request.form['phone' + str(i)] )
			self.emails.append(request.form['email' + str(i)] )
			
	def validate(self):
		error_message = ''
		for i in range(self.num_officers):
			if not (self.names[i]):
				error_message += "Missing advisor " + str(i+1) + " name.\n"
			if not (self.phones[i]):
				error_message += "Missing advisor " + str(i+1) + " phone.\n"
			if not (self.emails[i]):
				error_message += "Missing advisor " + str(i+1) + " email.\n"
		#TODO: Check if valid email using regex, and possibly add other validation requirements
		'''if not isinstance(self.num_officers, int):
			error_message += ("Number of officers needs to be an integer, instead got " + self.num_officers + ".\n")
		if not isinstance(self.num_advisors, int):
			error_message += ("Number of advisors needs to be an integer, instead got " + self.num_advisors + ".\n")'''

		return error_message
		
		
			
		
