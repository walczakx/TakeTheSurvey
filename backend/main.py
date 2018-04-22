from flask import render_template

def index(user):
	return render_template('index.html', name=user)
