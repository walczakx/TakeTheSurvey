from flask import session, render_template, redirect, url_for
from backend import user, db, auth, config

class main():
	def __init__(self, app):
		self.config_ = config.config(app)
		self.db_ = db.database(app, self.config_)
		self.user_ = user.user(self.db_)
		self.auth_ = auth.auth()

	def do_the_login(self, username, password):
		if self.user_.try_to_login(self.user_.get_user_id(username), password):
			session['username'] = username
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
		session.pop('survey_name', None)
		return redirect(url_for('msg_page', msg = "You've been logged out"))

	def is_user_logged(self):
		return 'username' in session

	def get_user_data(self):
		if not self.is_user_logged():
			return self.logout()
		return self.db_.get_user_data(self.user_.get_user_id(session.get('username')))

	def delete_account(self, usr):
		if usr == session.get('username'):
			return self.db_.delete_account(self.user_.get_user_id(session.get('username')))
		return False

	def get_survey_list(self):
		return self.db_.get_survey_list()

	def get_survey(self, survey_id):
		return self.db_.get_specific_survey(survey_id)

	def get_survey_id(self, survey_name):
		return self.db_.get_specific_survey_id(survey_name)

	def create_survey(self, questions, name):
		try:
			self.db_.add_survey(self.get_logged_user_id(), name)
			id = self.get_survey_id(self.get_survey_name())
			print "id: " + str(id)
			for q in questions:
				print "pyt: " + str(q[0])
				self.db_.add_surveytemplate(id, q[0])
				
			self.clear_new_survey()
			return True
		except:
			return False

	def delete_survey(self, survey_id):
		try:
			self.db_.delete_survey(survey_id)
			return True
		except:
			return False

	def add_question_to_new_survey(self, question_id):
		if not self.is_user_logged():
			return self.logout()

		a = session.get('question_list')
		if a is None:
			a = []

		if question_id not in a:
			a.append(question_id)
			session['question_list'] = a
		else:
			return False
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
		return self.db_.get_possible_answers(question_id)

	def get_question_list(self):
		return self.db_.get_all_question_in_questionbase()

	def delete_question(self, question_id):
		if self.is_user_logged() and self.has_admin_privileges():
			return self.db_.delete_question(question_id)
		return False

	def set_survey_name(self, name):
		if not self.is_user_logged():
			return self.logout()

		if self.auth_.validate_username(name):
			session['survey_name'] = name
			return True
		return False

	def get_saved_questions(self):
		questions = session.get('question_list')
		saved_questions = [0]

		for i in questions:
			saved_questions.append(self.db_.get_specific_question_name(i))

		if len(saved_questions) == 1:
			return None

		saved_questions.remove(0)
		return saved_questions

	def get_survey_name(self):
		return session.get('survey_name')

	def delete_question_from_survey(self, question_id):
		if not self.is_user_logged():
			return self.logout()

		a = session.get('question_list')

		if question_id in a:
			a.remove(question_id)
			session['question_list'] = a
		else:
			return False
		return True

	def clear_new_survey(self):
		session['question_list'] = []
		session['survey_name'] = ""

	def disable_survey(self, id):
		if self.db_.disable_survey(id):
			return True
		return False