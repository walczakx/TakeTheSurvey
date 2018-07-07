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
			return True
		return False

	def do_the_register(self, username, email, password, conf_password):
		if self.auth_.check_password(password, conf_password)\
            and self.auth_.validate_email(email)\
			and self.auth_.validate_username(username)\
            and self.user_.check_if_username_is_free(username):
			return self.db_.user_register(username, email, password)
		return False

	def logout(self):
		session.pop('username', None)

	def is_user_logged(self):
		return 'username' in session

	def get_user_data(self):
		return self.db_.get_user_data(self.user_.get_user_id(session.get('username')))

	def delete_account(self, usr):
		if usr == session.get('username'):
			self.db_.delete_account(self.user_.get_user_id(session.get('username')))

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
		return self.db_.get_user_id(session.get('username'))

	def has_admin_privileges(self):
		return self.db_.get_user_privileges(self.get_logged_user_id())

	def get_question(self, question_id):
		return self.db_.get_question_from_questionbase_by_id(question_id)

	def delete_question(self, question_id):
		if self.is_user_logged() and self.has_admin_privileges():
			return self.db_.delete_question(question_id)
		return False