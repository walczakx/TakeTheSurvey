from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL

import backend.main as main

app = Flask(__name__)
 
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')
	 
@app.route('/register',methods=['POST'])
def register():
	return render_template('index.html')

# login existing user
@app.route('/login',methods=['POST'])
def login():
	return render_template('index.html', user_logged=True)
 
# delete user account
@app.route('/delete_account',methods=['POST'])
def delete_user_account():
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

# fill out survey


if __name__ == '__main__':
	app.run()
