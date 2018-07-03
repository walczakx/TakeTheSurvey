from flask import Flask, render_template, request, redirect, url_for
import backend.main as main

app = Flask(__name__)
main = main.main(app)

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')
	 
@app.route('/register', methods=["POST"])
def register():
	assert request.path == '/register'

	psw = main.auth_.hash(request.form['psw'])
	psw_c = main.auth_.hash(request.form['psw_confirm'])

	if request.method == "POST" and main.do_the_register(request.form['usrname'], request.form['email'], psw, psw_c):
		return render_template('index.html', msg = "Success! You can now sign in")
	else:
		return main.error_page()

@app.route('/login', methods=["POST"])
def login():
	assert request.path == '/login'
	psw = main.auth_.hash(request.form['psw'])

	if request.method == "POST" and main.do_the_login(request.form['usrname'], psw, request.form['rememberme']):
		return render_template('index.html', msg = "Success! You're now logged in")
	else:
		return main.error_page()

@app.route('/logout', methods=["GET"])
def logout():
	try:
		main.logout()
	except:
		return main.error_page()
	return render_template('index.html', msg = "You're now logged off")

@app.route('/user_account', methods=["GET"])
def user_account():
	user_data = main.get_user_data()
	if user_data:
		return render_template('user.html', user_data = user_data)
	return main.error_page()

@app.route('/delete_account',methods=['POST'])
def delete_user_account():
	assert request.path == '/delete_account'
	psw = main.auth_.hash(request.form['psw'])

	if request.method == "POST" and main.do_the_login(request.form['usrname'], psw):
		main.delete_account(request.form['usrname'])
	return render_template('index.html')

@app.route('/add_survey')
def add_survey():
	return render_template('survey_add_new.html')

@app.route('/create',methods=['GET','POST'])
def create_new_survey():
	#todo jakie parametry?
	try:
		survey_id = main.create_survey()
		return redirect(url_for('show_specific_survey', survey_id = survey_id, msg = "Success"),)
	except:
		return main.error_page()

@app.route('/edit/<survey_id>')
def edit_specific_survey(survey_id):
	survey = main.get_survey(survey_id)
	if survey:
		return render_template('edit_survey.html', survey = survey)
	else:
		return main.error_page()

@app.route('/delete/<survey_id>', methods=['POST'])
def delete_survey(survey_id):
	if has_admin_priviliges() or is_survey_owner():
		if main.delete_survey(survey_id):
			return render_template('index.html')
	return main.error_page()

@app.route('/add_question', methods=['POST'])
def add_question():
	# todo params
	if main.add_question():
		return redirect(url_for('show_questions', msg="ok"))
	return main.error_page()

@app.route('/edit_question/<question_id>',methods=['GET'])
def edit_specific_question(question_id):
	if main.get_question(question_id) and (is_question_owner(question_id) or has_admin_priviliges()):
		return render_template('question_edit.html')

@app.route('/delete_question/<question_id>')
def delete_question(question_id):
	try:
		main.delete_question(question_id)
		return render_template('index.html')
	except:
		return main.error_page()

@app.route('/show_survey')
def show_survey():
	surveys = main.get_survey_list()
	return render_template('survey.html', surveys = surveys)

@app.route('/show_survey/<survey_id>', methods=['GET'])
def show_specific_survey(survey_id):
	survey = main.get_survey(survey_id)
	if survey:
		if request.form['msg']:
			return render_template('survey.html', survey = survey, msg = "Your survey was successfully added. You can see it below.")
		return  render_template('survey.html', survey = survey)
	else:
		return main.error_page()

@app.route('/show_questions', methods=['GET'])
def show_questions():
	return render_template('questions.html', msg = request.form['msg']) #not sure it'll work

#helper functions for templates
def is_user_logged():
	return main.is_user_logged()

def has_admin_priviliges():
	return main.user.has_admin_priviliges(user_id)

def is_survey_owner(survey_id):
	return main.user.is_survey_owner(survey_id, user_id)

def is_question_owner(question_id):
	return main.user.is_question_owner(question_id, user_id)

app.jinja_env.globals.update(is_user_logged = is_user_logged,
							 has_admin_priviliges = has_admin_priviliges,
							 is_survey_owner = is_survey_owner,
							 is_question_owner = is_question_owner)

if __name__ == '__main__':
	app.run()