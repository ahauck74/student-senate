class SenateLoginForm:

	def __init__(self, request):
		self.user = request.form['username']
		self.password = request.form['password']
		
	def validate(self):
		error_message = ''
		if (self.user != 'senate' or self.password != '1234'):
			error_message += "Error: Usesrname or password incorrect.\n"

		if len(error_message) == 0:
			return None;
		return error_message

class RecForm:
	
	def __init__(self, request):
		#The string in the bracket matches the field name in the html
		self.org_name = request.form['org_name'] 
		self.org_email = request.form['org_email']
		self.org_acronym = request.form['acronym']
		self.tier = 'unfunded'
		
		self.description = request.form['description']
		self.events = request.form['events']
		self.attendance = request.form['reg_attendance']
		self.num_members = request.form['members_total']
		
		self.num_officers = int(request.form['num_officers'])
		self.off_names, self.off_phones, self.off_emails, self.off_pos = [], [], [], []
		for i in range(self.num_officers):
		
			self.off_names.append(request.form['off_name' + str(i)])
			self.off_phones.append(request.form['off_phone' + str(i)] )
			self.off_emails.append(request.form['off_email' + str(i)] )
			self.off_pos.append(request.form['off_pos' + str(i)] )
		
		self.num_advisors = int(request.form['num_advisors'])
		self.adv_names, self.adv_phones, self.adv_emails = [], [], []
		for i in range(self.num_advisors):
		
			self.adv_names.append(request.form['adv_name' + str(i)])
			self.adv_phones.append(request.form['adv_phone' + str(i)] )
			self.adv_emails.append(request.form['adv_email' + str(i)] )
		
		
		
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
			
		for i in range(self.num_officers):
			if not (self.off_names[i]):
				error_message += "Missing officer " + str(i+1) + " name.\n"
			if not (self.off_phones[i]):
				error_message += "Missing officer " + str(i+1) + " phone.\n"
			if not (self.off_emails[i]):
				error_message += "Missing officer " + str(i+1) + " email.\n"
			if not (self.off_pos[i]):
				error_message += "Missing officer " + str(i+1) + " position.\n"
				
		for i in range(self.num_advisors):
			if not (self.adv_names[i]):
				error_message += "Missing advisor " + str(i+1) + " name.\n"
			if not (self.adv_phones[i]):
				error_message += "Missing advisor " + str(i+1) + " phone.\n"
			if not (self.adv_emails[i]):
				error_message += "Missing advisor " + str(i+1) + " email.\n"
				
		
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
		
		self.change_tier = request.form['change_tier']#<y> or <n>
		if self.change_tier == 'n' : 
			self.tier_dest = request.form['tier']#<1>, <2>, <3>, or <Unfunded>
		else:
			self.tier_dest = request.form['tier_destination']#<1>, <2>, <3>, or <Unfunded>
		self.description = request.form['description']
		self.attendance = request.form['reg_attendance']
		self.num_members = request.form['members_total']
		
		self.num_officers = int(request.form['num_officers'])
		self.off_names, self.off_phones, self.off_emails, self.off_pos = [], [], [], []
		for i in range(self.num_officers):
		
			self.off_names.append(request.form['off_name' + str(i)])
			self.off_phones.append(request.form['off_phone' + str(i)] )
			self.off_emails.append(request.form['off_email' + str(i)] )
			self.off_pos.append(request.form['off_pos' + str(i)] )
		
		self.num_advisors = int(request.form['num_advisors'])
		self.adv_names, self.adv_phones, self.adv_emails = [], [], []
		for i in range(self.num_officers):
		
			self.adv_names.append(request.form['adv_name' + str(i)])
			self.adv_phones.append(request.form['adv_phone' + str(i)] )
			self.adv_emails.append(request.form['adv_email' + str(i)] )
		
		
		
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
		for i in range(self.num_officers):
			if not (self.off_names[i]):
				error_message += "Missing officer " + str(i+1) + " name.\n"
			if not (self.off_phones[i]):
				error_message += "Missing officer " + str(i+1) + " phone.\n"
			if not (self.off_emails[i]):
				error_message += "Missing officer " + str(i+1) + " email.\n"
			if not (self.off_pos[i]):
				error_message += "Missing officer " + str(i+1) + " position.\n"
				
		for i in range(self.num_advisors):
			if not (self.adv_names[i]):
				error_message += "Missing advisor " + str(i+1) + " name.\n"
			if not (self.adv_phones[i]):
				error_message += "Missing advisor " + str(i+1) + " phone.\n"
			if not (self.adv_emails[i]):
				error_message += "Missing advisor " + str(i+1) + " email.\n"
				
		
		if len(error_message) == 0:
			return None;
		return error_message
		
		
class OfficerForm:
	
	def __init__(self, request):
		self.num_officers = int(request.form['num_members'])
		self.off_names, self.off_phones, self.off_emails, self.off_pos = [], [], [], []
		for i in range(self.num_officers):
		
			self.off_names.append(request.form['off_name' + str(i)])
			self.off_phones.append(request.form['off_phone' + str(i)] )
			self.off_emails.append(request.form['off_email' + str(i)] )
			self.off_pos.append(request.form['off_pos' + str(i)] )
			
	def validate(self):
		error_message = ''
		for i in range(self.num_officers):
			if not (self.off_names[i]):
				error_message += "Missing officer " + str(i+1) + " name.\n"
			if not (self.off_phones[i]):
				error_message += "Missing officer " + str(i+1) + " phone.\n"
			if not (self.off_emails[i]):
				error_message += "Missing officer " + str(i+1) + " email.\n"
			if not (self.off_pos[i]):
				error_message += "Missing officer " + str(i+1) + " position.\n"
		#TODO: Check if valid email using regex, and possibly add other validation requirements

		return error_message
		
class AdvisorForm:
	
	def __init__(self, request):
		self.num_advisors = int(request.form['num_members'])
		self.adv_names, self.adv_phones, self.adv_emails = [], [], []
		for i in range(self.num_advisors):
		
			self.adv_names.append(request.form['adv_name' + str(i)])
			self.adv_phones.append(request.form['adv_phone' + str(i)] )
			self.adv_emails.append(request.form['adv_email' + str(i)] )
			
	def validate(self):
		error_message = ''
		for i in range(self.num_advisors):
			if not (self.adv_names[i]):
				error_message += "Missing advisor " + str(i+1) + " name.\n"
			if not (self.adv_phones[i]):
				error_message += "Missing advisor " + str(i+1) + " phone.\n"
			if not (self.adv_emails[i]):
				error_message += "Missing advisor " + str(i+1) + " email.\n"
		#TODO: Check if valid email using regex, and possibly add other validation requirements

		return error_message
		
		
class YeetSender:

	def __init__(self):
		print("Prepared to yeet!")
	def deploy_yeet(self):
		return "Yeet"
	def deploy_n_yeets(self, n):
		for i in range(n):
			print(self.deploy_yeet())
		
