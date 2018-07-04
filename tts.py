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
	return redirect(url_for('msg_page'))

@app.route('/login', methods=["POST"])
def login():
	assert request.path == '/login'
	assert request.method == "POST"
	psw = main_.auth_.hash(request.form['psw'])

	if main_.do_the_login(request.form['usrname'], psw, request.form['rememberme']):
		return render_template('index.html', msg = "Success! You're now logged in")
	return  redirect(url_for('msg_page'))

@app.route('/logout', methods=["GET"])
def logout():
	try:
		main_.logout()
	except:
		return redirect(url_for('msg_page'))
	return redirect(url_for('msg_page', msg = "You're now logged off"))

@app.route('/user_account', methods=["GET"])
def user_account():
	user_data = main_.get_user_data()
	if user_data:
		return render_template('user.html', user_data = user_data)
	return redirect(url_for('msg_page'))

@app.route('/delete_account',methods=['POST'])
def delete_user_account():
	assert request.path == '/delete_account'
	assert request.method == "POST"
	psw = main_.auth_.hash(request.form['psw'])

	if main_.do_the_login(request.form['usrname'], psw):
		main_.delete_account(request.form['usrname'])
	return render_template('index.html', msg = "Your account was successfully deleted. So long.")

@app.route('/add_survey')
def add_survey():
	return render_template('survey_add_new.html')

@app.route('/create',methods=['GET','POST'])
def create_new_survey():
	#todo jakie parametry?
	try:
		survey_id = main_.create_survey()
		return redirect(url_for('show_specific_survey', survey_id = survey_id, msg = "Success"))
	except:
		return redirect(url_for('msg_page', msg = "Success"))

@app.route('/edit/<survey_id>')
def edit_specific_survey(survey_id):
	survey = main_.get_survey(survey_id)
	if survey:
		return render_template('edit_survey.html', survey = survey)
	return redirect(url_for('msg_page'))

@app.route('/delete/<survey_id>', methods=['POST'])
def delete_survey(survey_id):
	if has_admin_priviliges() or is_survey_owner(survey_id):
		if main_.delete_survey(survey_id):
			return render_template('index.html')
	return redirect(url_for('msg_page'))

@app.route('/add_question', methods=['POST'])
def add_question():
	# todo params
	if main_.add_question():
		return redirect(url_for('show_questions', msg="ok"))
	return redirect(url_for('msg_page'))

@app.route('/edit_question/<question_id>',methods=['GET'])
def edit_specific_question(question_id):
	if main_.get_question(question_id) and (is_question_owner(question_id) or has_admin_priviliges()):
		return render_template('question_edit.html')

@app.route('/delete_question/<question_id>')
def delete_question(question_id):
	try:
		main_.delete_question(question_id)
		return render_template('index.html')
	except:
		return redirect(url_for('msg_page'))

@app.route('/show_survey')
def show_survey():
	surveys = main_.get_survey_list()
	return render_template('survey.html', surveys = surveys)

@app.route('/show_survey/<survey_id>', methods=['GET'])
def show_specific_survey(survey_id):
	survey = main_.get_survey(survey_id)
	if survey:
		if request.form['msg']:
			return render_template('survey.html', survey = survey, msg = "Your survey was successfully added. You can see it below.")
		return  render_template('survey.html', survey = survey)
	return redirect

@app.route('/show_questions', methods=['GET'])
def show_questions():
	return render_template('questions.html', msg = request.form['msg']) #not sure it'll work

@app.route('/msg', methods=['GET'])
def msg_page():
	if request.method == "GET" and request.args.get('msg'):
		return render_template('error.html', msg = request.args.get('msg'))
	else:
		return render_template('error.html')


#helper functions for templates
def is_user_logged():
	return main_.is_user_logged()

def has_admin_priviliges():
	return main_.user_.has_admin_privileges(main_.get_logged_user_privileges())

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