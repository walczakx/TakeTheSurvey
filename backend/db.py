from flaskext.mysql import MySQL

class database:
    def __init__(self, app, config):
        self.mysql = MySQL(app)

        app.config['MYSQL_DATABASE_USER'] = config.db_username
        app.config['MYSQL_DATABASE_PASSWORD'] = config.db_pass
        app.config['MYSQL_DATABASE_DB'] = config.db_name
        app.config['MYSQL_DATABASE_HOST'] = config.db_host

        self.mysql.init_app(app)
    def mysql_connect(self):
        conn = self.mysql.connect()
        return conn.cursor()


    def do_some_query(self, name, id):
        cursor = self.mysql_connect()
        try:
            cmd = "update people set name=%s where id=%s"
            cursor.execute(cmd, (name, id))
            return cursor.fetchall()
        except:
            #do something
            return

    def get_user_id(self, username):
        cursor = self.mysql_connect()
        try:
            cmd = "select user_id from users where username = %s"
            cursor.execute(cmd, (username,))
            return cursor.fetchone()
        except:
            # do something
            return

    def user_register(self, username, email, password, conf_password):
        # some sql, if succes, return true
        return True

    def check_if_username_is_free(self, username):
        # if select username from users where username = username is null
        return True

    def get_user_data(self, user_id):
        # need to select user data from sql na parse it to some dictionary {"username": row[0], "email": row[1] } etc
        return { "username":"Jasio","email":"jasio@jasio.ja"}

    def delete_account(self, user_id):
        # sql delete account
        pass

    def get_survey_list(self):
        # sql query
        # jakos to trzeba zwrocic, zrob tak aby bylo dobrze:)
        pass

    def get_survey(self, survey_id):
        # jw
        pass
