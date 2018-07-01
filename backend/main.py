from flask import session
from backend import user

user = user.user()

def do_the_login(username, password, rememberme):
	if user.try_to_login(username, password):
		session['username'] = username
		session['privileges'] = user.get_user_privileges(username)
		return True
	else:
		return False

def do_the_register(username, email, password, conf_password):
	return True

def logout():
	session.pop('username', None)
	session.pop('privileges', None)

def is_user_logged():
	return 'username' in session

def has_admin_priviliges(user_id):
	return False #todo

def is_survey_owner(survey_id, user_id):
	return False #todo