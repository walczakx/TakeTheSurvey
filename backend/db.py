from flask import redirect, url_for
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

    def get_user_id(self, username):
        cursor = self.mysql_connect()
        try:
            cmd = "select id_user from users where login = %s"
            cursor.execute(cmd, (username,))
            return cursor.fetchone()
        except:
            return redirect(url_for('msg_page'))

    def user_register(self, username, email, password):
        # some sql, if succes, return true
        cursor = self.mysql_connect()
        try:
            cmd = "INSERT INTO `users`( `login`, `pass`, `email`) VALUES (%s,%s,%s)"
            cursor.execute(cmd, (username, password, email))
        except:
            return False
        return True

    def check_if_username_is_free(self, username):
        # if select username from users where username = username is null
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT id_user FROM `users` WHERE login = %s"
            cursor.execute(cmd, (username,))
            return cursor.fetchone()
        except:
            # do something
            return

    def get_user_data(self, user_id):
        # need to select user data from sql na parse it to some dictionary {"username": row[0], "email": row[1] } etc
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT id_user, login, email FROM `users` WHERE id_user = %d"
            cursor.execute(cmd, (user_id))
            return cursor.fetchall()
        except:
            return redirect(url_for('msg_page'))

    def delete_account(self, user_id):
        # sql delete account
        cursor = self.mysql_connect()
        try:
            cmd = "DELETE * FROM `users` WHERE id_user = %d"
            cursor.execute(cmd, (user_id,))
            return cursor.fetchone()
        except:
            return redirect(url_for('msg_page'))

    def get_survey_list(self):
        # sql query
        # jakos to trzeba zwrocic, zrob tak aby bylo dobrze:)
        # zwraca wszystkie aktywne do wypelnienia ankiety
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT id_survey, survey_description, datetime FROM `survey` where active = '1'"
            cursor.execute(cmd)
            surveys = cursor.fetchall()
            return surveys
        except:
            # do something
            return

    def get_specific_survey(self, survey_id):
        # jw zwraca cala ankiete  z pytaniami do wypelnienia z mozliwymi odpowiedziami
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT * FROM `survey` JOIN surveytemplate ON survey.id_survey = surveytemplate.id_survey JOIN questionbase ON surveytemplate.id_question = questionbase.id_question JOIN possibleanswers ON questionbase.id_question = possibleanswers.id_question WHERE survey.id_survey = %d"
            cursor.execute(cmd, (survey_id))
            return cursor.fetchall()

        except:
            return redirect(url_for('msg_page'))

    def add_question_to_questionbase(self, question_description, id_question_type):
        # dodaje pytanie do bazy pytan wraz z typem pytania (1 jednokrotny wybor, 2 wielokrotny wybor)
        cursor = self.mysql_connect()
        try:
            cmd = "INSERT INTO `questionbase`(`question_description`, `id_questiontype`) VALUES (%s, %d)"
            cursor.execute(cmd, (question_description, id_question_type))
            return cursor.fetchone()
        except:
            return redirect(url_for('msg_page'))

    def get_all_question_in_questionbase(self):
        # listuje wsyztkie pytania dostepne w bazie pytan
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT * FROM `questionbase`"
            cursor.execute(cmd)
            return cursor.fetchone()
        except:
            return redirect(url_for('msg_page'))

    def get_question_from_questionbase_by_tag(self, tag_description):
        # listuje pytania po tagacah
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT * FROM questiontags JOIN tags ON questiontags.id_tag = tags.id_tag JOIN questionbase ON questiontags.id_question = questionbase.id_question WHERE tag_description = %s"
            cursor.execute(cmd, (tag_description, ))
            return cursor.fetchone()
        except:
            # do something
            return

    def get_possible_answers(self, id_question):
        # zwraca mozliwe odpowiedzi dla pytania
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT `id_answer`, `id_question`, `answerdescription` FROM `possibleanswers` WHERE id_question = %d"
            cursor.execute(cmd, (id_question, ))
            return cursor.fetchone()
        except:
            # do something
            return

    def add_possible_answers(self, id_question, answerdescription):
        # dodaje mozliwe odpowiedzi do pytania
        cursor = self.mysql_connect()
        try:
            cmd = "INSERT INTO `possibleanswers`(`id_question`, `answerdescription`) VALUES (%d, %s)"
            cursor.execute(cmd, (id_question, answerdescription))
            return cursor.fetchone()
        except:
            # do something
            return redirect(url_for('msg_page'))

    def get_user_password(self, user_id):
        # zwraca haslo usera
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT  `pass` FROM `users` WHERE id_user = %d"
            cursor.execute(cmd, (user_id))
            return cursor.fetchone()
        except:
            return redirect(url_for('msg_page'))

    def get_survey_owner(self, survey_id):
        # zwraca wlasciciela ankiety, to zwraca tworce szablonu a nie usera ktory wypelnil ankiete
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT  `id_user` FROM `survey` WHERE id_survey = %d"
            cursor.execute(cmd, (survey_id))
            return cursor.fetchone()
        except:
            return redirect(url_for('msg_page'))

    def get_survey_respondent(self, completedsurvey_id):
         # zwraca usera ktory wypelnil ankiete (respondenta)
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT  `id_user` FROM `completedsurvey` WHERE id_completedsurvey = %d"
            cursor.execute(cmd, (completedsurvey_id))
            return cursor.fetchone()
        except:
            return redirect(url_for('msg_page'))

    def get_question_owner(self, survey_id):
        # TODO tego nie ma baza pytan jest wspolna, na ta chwile nie ma identyfikacji kto dodal pytanie do bazy
        owner_id = 1
        return owner_id

    def is_user_have_any_questions(self, user_id):
        #TODO tego nie ma baza pytan jest wspolna, na ta chwile nie ma identyfikacji kto dodal pytanie do bazy
        return False #czy uzytkownik ma jakies swoje pytania?

    def is_user_have_any_surveys(self, user_id):
        #zwraca liczbe ankiet (wzorccow) usera
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT  count(id_survey) AS NumberOfSurveys FROM `survey` WHERE id_user = %d"
            cursor.execute(cmd, (user_id))
            return cursor.fetchone()
        except:
            return False
    def is_user_have_any_completed_surveys(self, user_id):
        #zwraca liczbe ankiet wypelnionych przez usera
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT  count(id_completedsurvey) AS NumberOfCompletedSurveys FROM `completedsurvey` WHERE id_user = = %d"
            cursor.execute(cmd, (user_id))
            return cursor.fetchone()
        except:
            return False

    def get_completedanswers_in_completedsurvey(self, completedsurvey_id):
        # zwraca, id szablonu, id pytan, id odpoodpowiedzi dla wypelnionej ankiety
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT * FROM `completedanswers` WHERE id_completedsurvey = %d"
            cursor.execute(cmd,(completedsurvey_id))
            return cursor.fetchone()
        except:
            return redirect(url_for('msg_page'))
			
	 def get_completed_surveys(self, user_id):
        # zwraca wype³nione ankiety przez u¿ytownika (lista completedsurvey.id_completedsurvey, survey.id_survey, survey.survey_description, completedsurvey.datetime, completedsurvey.id_user)
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT completedsurvey.id_completedsurvey, survey.id_survey, survey.survey_description, completedsurvey.datetime, completedsurvey.id_user FROM `survey` left Join `completedsurvey` ON survey.id_survey = completedsurvey.id_survey WHERE completedsurvey.id_user = %d"
            cursor.execute(cmd,(user_id))
			completed_surveys = cursor.fetchall()
            return completed_surveys
        except:
            return redirect(url_for('msg_page'))
