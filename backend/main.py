from flask import session, render_template
from backend import user, db, auth, config

class main():
	def __init__(self, app):
		self.config_ = config.config(app)
		self.db_ = db.database(app, self.config_)
		self.user_ = user.user(self.db_)
		self.auth_ = auth.auth()

	def do_the_login(self, username, password, rememberme):
		if self.user_.try_to_login(self.user_.get_user_id(username), password):
			session['username'] = username
			if self.user_.has_admin_privileges(self.user_.get_user_id(username)):
				session['privileges'] = "admin"
			else:
				session['privileges'] = "user"
			return True
		return False

	def do_the_register(self, username, email, password, conf_password):
		if self.auth_.check_password(password, conf_password)\
				and self.auth_.validate_email(email)\
				and self.user_.check_if_username_is_free(username):
			return self.db_.user_register(username, email, password)
		return False

	def logout(self):
		session.pop('username', None)
		session.pop('privileges', None)

	def is_user_logged(self):
		return 'username' in session

	def get_user_data(self):
		return self.db_.get_user_data(self.user_.get_user_id(session['username']))

	def delete_account(self, usr):
		if usr == session['username']:
			self.db_.delete_account(self.user_.get_user_id(session['username']))

	def get_survey_list(self):
		return self.db_.get_survey_list()

	def get_survey(self, survey_id):
		return self.db_.get_specific_survey(survey_id)

	def create_survey(self):
		#todo
		return 1

	def delete_survey(self, survey_id):
		return True #self.db_.delete_survey()  ## todo check if exist

	def add_question(self):
		# todo, verification etc
		return True # self.db_add_question()

	def get_logged_user_id(self):
		return session['username']

	def get_logged_user_privileges(self):
		return session['privileges']