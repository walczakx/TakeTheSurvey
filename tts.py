from flask import Flask, render_template, request
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
		return render_template('index.html', msg = "Ops, something went wrong. Try again")

# login existing user
@app.route('/login', methods=["POST"])
def login():
	assert request.path == '/login'
	psw = main.auth_.hash(request.form['psw'])

	if request.method == "POST" and main.do_the_login(request.form['usrname'], psw, request.form['rememberme']):
		return render_template('index.html', msg = "Success! You're now logged in")
	else:
		return render_template('index.html', msg = "Ops, something went wrong. Try again")

@app.route('/logout', methods=["GET"])
def logout():
	main.logout()
	return render_template('index.html', msg = "You're now logged off")

@app.route('/user_account', methods=["GET"])
def user_account():
	user_data = main.get_user_data()
	return render_template('user.html', user_data = user_data)

# delete user account
@app.route('/delete_account',methods=['POST'])
def delete_user_account():
	assert request.path == '/delete_account'
	psw = main.auth_.hash(request.form['psw'])
	if request.method == "POST" and main.do_the_login(request.form['usrname'], psw):
		main.delete_account(request.form['usrname'])
	return render_template('index.html')

# create new survey
@app.route('/create',methods=['GET'])
def create_new_survey():
	return render_template('index.html')

# edit existing survey
@app.route('/edit/<survey_id>')
@app.route('/edit')
def edit_survey():
	return render_template('index.html')

# delete own survey
@app.route('/delete/<survey_id>',methods=['POST'])
def delete_survey():
	return render_template('index.html')

# add new question
@app.route('/add_question',methods=['POST'])
def add_question():
	return render_template('index.html')

# edit question
@app.route('/edit',methods=['GET'])
@app.route('/edit_question/<question_id>',methods=['GET'])
def edit_question():
	return render_template('index.html')

# delete question
@app.route('/delete_question/<question_id>')
def delete_question():
	return render_template('index.html')

# view survey
@app.route('/show_survey')
def show_survey():
	surveys = main.get_survey_list()
	return render_template('survey.html', surveys = surveys)

@app.route('/show_survey/<survey_id>')
def show_specific_survey(survey_id):
	survey = main.get_survey(survey_id)
	if survey:
		return render_template('survey.html', survey = survey)
	else:
		return "error, no data"


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