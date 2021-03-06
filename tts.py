from flask import Flask, render_template, request, redirect, url_for
import backend.main as main

app = Flask(__name__)
main_ = main.main(app)

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/register', methods=["POST"])
def register():
	assert request.path == '/register'
	assert request.method == "POST"	

	psw = main_.auth_.hash(request.form['psw'])
	psw_c = main_.auth_.hash(request.form['psw_confirm'])

	if main_.do_the_register(request.form['usrname'], request.form['email'], psw, psw_c):
		return redirect(url_for('msg_page', msg = "Great success! You can now log-in"))
	return redirect(url_for('msg_page', msg = "Ops, can't register. Remember that:\n * username must contain at least 4 characters\n * username has to be unused<br> * password and password confirmation must be identical"))

@app.route('/login', methods=["POST"])
def login():
	assert request.path == '/login'
	assert request.method == "POST"
	psw = main_.auth_.hash(request.form['psw'])

	if main_.do_the_login(request.form['usrname'], psw):
		return redirect(url_for('msg_page', msg = "Success! You're now logged in"))
	return redirect(url_for('msg_page'))

@app.route('/logout', methods=["GET"])
def logout():
	try:
		main_.logout()
	except:
		return redirect(url_for('msg_page'))
	return redirect(url_for('msg_page', msg = "You're now logged off"))

@app.route('/user_account', methods=['GET'])
def user_account():
	user_data = main_.get_user_data()
	if user_data:
		return render_template('user.html', user_data = user_data)
	return redirect(url_for('msg_page'))

@app.route('/edit_user_data', methods=['GET'])
def edit_user_data():
	user_data = main_.get_user_data()
	if user_data:
		return render_template('edit_user_data.html', user_data = user_data)
	return redirect(url_for('msg_page'))

@app.route('/delete_account_confirmation', methods=['GET'])
def delete_account_confirmation():
	user_data = main_.get_user_data()
	if user_data:
		return render_template('delete_account.html', user_data = user_data)
	return redirect(url_for('msg_page'))

@app.route('/delete_account',methods=['POST'])
def delete_user_account():
	assert request.path == '/delete_account'
	assert request.method == 'POST'
	psw = main_.auth_.hash(request.form['psw'])

	if main_.do_the_login(request.form['usrname'], psw):
		main_.delete_account(request.form['usrname'])
		main_.logout()
		return redirect(url_for('msg_page', msg = "Your account was successfully deleted. So long."))
	return redirect(url_for('msg_page'))

@app.route('/add_survey')
def add_survey():
	questions = main_.get_saved_questions()
	name = main_.get_survey_name()

	if questions:
		return render_template('survey_add_new.html', questions = questions, name = name)
	return render_template('survey_add_new.html', name = name)

@app.route('/add_to_survey/<question_id>')
def add_question_to_survey(question_id):
	if main_.add_question_to_new_survey(question_id):
		return redirect(url_for('show_questions', msg = "Question \"" + str(main_.get_question(question_id)[0][1]) + "\" was successfully added to new survey"))
	return redirect(url_for('show_questions', msg = "Can't add question to survey. Remeber that you can't add same question twice"))

@app.route('/create',methods=['POST'])
def create_new_survey():
	questions = main_.get_saved_questions()
	name = main_.get_survey_name()

	if main_.create_survey(questions, name):
		return redirect(url_for('show_survey'))
	return redirect(url_for('msg_page'))

@app.route('/edit/<survey_id>')
def edit_specific_survey(survey_id):
	survey = main_.get_survey(survey_id)
	if survey:
		return render_template('edit_survey.html', survey = survey)
	return redirect(url_for('msg_page'))

@app.route('/delete/<survey_id>', methods = ['GET'])
def delete_survey(survey_id):
	if has_admin_priviliges() or is_survey_owner(survey_id):
		if main_.delete_survey(survey_id):
			return redirect(url_for('show_survey'))
	return redirect(url_for('msg_page'))

@app.route('/add_question')
def add_squestion():
	name = main_.get_question_name()
	return render_template('question_add_new.html', name = name)

@app.route('/add_questions', methods=['GET'])
def add_question():
	if main_.add_question():
		return redirect(url_for('show_questions', msg="All done, your question was added"))
	return redirect(url_for('msg_page'))

@app.route('/edit_question/<question_id>',methods=['GET'])
def edit_specific_question(question_id):
	question = main_.get_question(question_id)
	if question and (is_question_owner(question_id) or has_admin_priviliges()):
		return render_template('question_edit.html', question = question)

@app.route('/delete_question/<question_id>')
def delete_question(question_id):
	if main_.delete_question(question_id):
		return redirect(url_for('show_questions'))
	return redirect(url_for('msg_page'))

@app.route('/show_survey', methods = ['GET'])
def show_survey():
	return render_template('survey.html', surveys = main_.get_survey_list())

@app.route('/show_survey/<survey_id>')
def show_specific_survey(survey_id):
	survey = main_.get_survey(survey_id)
	if survey:
		if request.form.get('msg'):
			return render_template('survey.html', survey = survey, msg = "Your survey was successfully added. You can see it below.")
		return render_template('survey.html', survey = survey)
	return redirect(url_for('msg_page', msg = "Survey you're looking for, is non-available at the moment. Sorry for that"))

@app.route('/show_questions', methods = ['GET'])
def show_questions():
	question = main_.get_question_list()
	return render_template('questions.html', questions = question, msg = request.args.get('msg'))

@app.route('/show_questions/<question_id>')
def show_question(question_id):
	question = main_.get_question(question_id)
	answers = main_.get_answers_to_questions(question_id)

	if answers and question:
		return render_template('questions.html', question = question, answers = answers)
	return redirect(url_for('msg_page'))

@app.route('/msg', methods=['GET','POST'])
def msg_page():
	if request.method == "GET" and request.args.get('msg'):
		return render_template('error.html', msg = request.args.get('msg'))
	return render_template('error.html')

@app.route('/set_new_survey_name', methods=['GET'])
def set_survey_name():
	if main_.set_survey_name(request.args.get('name')):
		return redirect(url_for('add_survey'))
	return redirect(url_for('msg_page'))

@app.route('/question_delete/<question_id>')
def question_delete(question_id):
	if main_.delete_question_from_survey(question_id):
		return redirect(url_for('add_survey'))
	return redirect(url_for('msg_page'))

@app.route('/disable/<survey_id>')
def disble_survey(survey_id):
	if main_.disable_survey(survey_id):
		return redirect(url_for('show_survey', msg = 'Selected survey was temporary disabled'))
	return redirect(url_for('show_survey', msg = 'Ops, something went wrong... Try again?'))

@app.route('/set_new_question_name', methods=['GET'])
def set_new_question_name():
	if main_.set_question_name(request.args.get('name')):
		return redirect(url_for('add_squestion'))
	return redirect(url_for('msg_page'))

#helper functions for templates, all done
def is_user_logged():
	return main_.is_user_logged()

def has_admin_priviliges():
	if main_.is_user_logged():
		return main_.has_admin_privileges()
	return False

def is_survey_owner(survey_id):
	if main_.is_user_logged():
		return main_.user_.is_survey_owner(survey_id, main_.get_logged_user_id())
	return False

def is_question_owner(question_id):
	if main_.is_user_logged():
		return main_.user_.is_question_owner(question_id, main_.get_logged_user_id())
	return False

def is_user_have_questions():
	if main_.is_user_logged():
		return main_.db_.is_user_have_any_questions(main_.get_logged_user_id())
	return False

def is_user_have_surveys():
	if main_.is_user_logged():
		return main_.db_.is_user_have_any_surveys(main_.get_logged_user_id())
	return False

app.jinja_env.globals.update(is_user_logged = is_user_logged,
                             has_admin_priviliges = has_admin_priviliges,
                             is_survey_owner = is_survey_owner,
                             is_question_owner = is_question_owner,
                             is_user_have_questions = is_user_have_questions,
                             is_user_have_surveys = is_user_have_surveys)

if __name__ == '__main__':
	app.run()
