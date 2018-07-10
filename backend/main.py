from flask import session, render_template, redirect, url_for
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
			session['question_counter'] = 0
			session['question_list'] = []
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
		session.pop('question_list', None)
		session.pop('question_counter', None)
		session.pop('survey_name', None)
		return redirect(url_for('msg_page', msg = "You've been logged out"))

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

	def add_question_to_new_survey(self, question_id):
		if not self.is_user_logged():
			return self.logout()

		a = session.get('question_list')
		print "adding: before" + str(a)
		if a is None:
			a = []

		if question_id not in a:
			a.append(question_id)
			session['question_list'] = a
		else:
			return False
		print "adding: after" + str(session.get('question_list'))
		return True

	def add_question_to_database(self):
		# todo, verification etc 
		return True # self.db_add_question()

	def get_logged_user_id(self):
		return self.db_.get_user_id(session.get('username'))

	def has_admin_privileges(self):
		return self.db_.get_user_privileges(self.get_logged_user_id())

	def get_question(self, question_id):
		return self.db_.get_question_from_questionbase_by_id(question_id)

	def get_answers_to_questions(self, question_id):
		d =  self.db_.get_possible_answers(question_id)
		print d
		return d

	def get_question_list(self):
		return self.db_.get_all_question_in_questionbase()

	def delete_question(self, question_id):
		if self.is_user_logged() and self.has_admin_privileges():
			return self.db_.delete_question(question_id)
		return False

	def get_saved_questions(self):
		print "get: before list: " + str(session.get('question_list'))
		print "get: before login: " + str(session.get('username'))

		name = session.get('survey_name')
		questions = session.get('question_list')

		saved_questions = []

		for i in questions:
			saved_questions.append(i)
			print i

		return [saved_questions, name]
	
