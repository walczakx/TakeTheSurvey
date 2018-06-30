from flask import session

def do_the_login(username, password, rememberme):
	session['username'] = username
	return True

def do_the_register(username, email, password, conf_password):
	return True

def logout():
	session.pop('username', None)

def is_user_logged():
	return 'username' in session

def has_admin_priviliges():
	return False #todo

def is_survey_owner(survey_id):
	return False #todo