from flaskext.mysql import MySQL

class database:
    def __init__(self, app):
        mysql = MySQL(app)

        app.config['MYSQL_DATABASE_USER'] = 'tts'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'tts_secret_password'
        app.config['MYSQL_DATABASE_DB'] = 'tts_db'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        mysql.init_app(app)
        conn = mysql.connect()
