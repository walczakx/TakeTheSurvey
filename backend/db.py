from flask import redirect, url_for
from flaskext.mysql import MySQL


class database:
    def __init__(self, app, config):
        self.mysql = MySQL()

        app.config['MYSQL_DATABASE_USER'] = config.db_username
        app.config['MYSQL_DATABASE_PASSWORD'] = config.db_pass
        app.config['MYSQL_DATABASE_DB'] = config.db_name
        app.config['MYSQL_DATABASE_HOST'] = config.db_host

        self.mysql.init_app(app)
        self.conn = None

    def mysql_connect(self):
        self.conn = self.mysql.connect()
        return self.conn.cursor()

    def mysql_finalize(self):
        self.conn.commit()
        self.conn.close()

    def get_user_id(self, username):
        cursor = self.mysql_connect()
        try:
            cmd = "select id_user from users where login = %s"
            cursor.execute(cmd, (username))
            return cursor.fetchone()
        except:
            return redirect(url_for('msg_page'))

    def user_register(self, username, email, password):
        cursor = self.mysql_connect()
        try:
            cmd = "INSERT INTO `users`( `login`, `pass`, `email`) VALUES (%s,%s,%s)"
            cursor.execute(cmd, (username, password, email))
            return True
        except:
            return False
        finally:
            self.mysql_finalize()

    def check_if_username_is_free(self, username):
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT id_user FROM `users` WHERE login = %s"
            cursor.execute(cmd, (username))
            return cursor.fetchone() is None
        except:
            return False
        finally:
            self.mysql_finalize()

    def get_user_data(self, user_id):
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT id_user, login, email FROM `users` WHERE id_user = %s"
            cursor.execute(cmd, (user_id))
            return cursor.fetchall()
        except:
            return redirect(url_for('msg_page'))
        finally:
            self.mysql_finalize()

    def get_user_privileges(self, user_id):
        cursor = self.mysql_connect()
        try:
            cmd = "select role from `users` where id_user = %s"
            cursor.execute(cmd, (user_id))
            return cursor.fetchone()[0]
        except:
            return False
        finally:
            self.mysql_finalize()

    def delete_account(self, user_id):
        # sql delete account
        cursor = self.mysql_connect()
        try:
            cmd = "DELETE FROM `users` WHERE id_user = %s"
            cursor.execute(cmd, (user_id))
            return cursor.fetchone()
        except:
            return redirect(url_for('msg_page'))
        finally:
            self.mysql_finalize()

    def get_survey_list(self):
        # zwraca wszystkie aktywne do wypelnienia ankiety
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT id_survey, survey_description, datetime FROM `survey` where active = 1"
            cursor.execute(cmd)
            return cursor.fetchall()
        except:
            return False
        finally:
            self.mysql_finalize()

    def get_specific_question_name(self, id_question):
        cursor = self.mysql_connect()
        try:
            cmd = "select * from `questionbase` where id_question = %s"
            cursor.execute(cmd, (id_question))
            return cursor.fetchall()[0]
        except:
            return redirect(url_for('msg_page'))
        finally:
            self.mysql_finalize()

    def get_specific_survey_id(self, name):
        cursor = self.mysql_connect()
        try:
            cmd = "select id_survey from `survey` where survey_description = %s"
            cursor.execute(cmd, (name))
            return cursor.fetchall()[0][0]
        except:
            return redirect(url_for('msg_page'))
        finally:
            self.mysql_finalize()

    # works
    def get_specific_survey(self, survey_id):
        # jw zwraca cala ankiete  z pytaniami do wypelnienia z mozliwymi odpowiedziami
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT * FROM `survey` " \
                  "JOIN surveytemplate ON survey.id_survey = surveytemplate.id_survey " \
                  "JOIN questionbase ON surveytemplate.id_question = questionbase.id_question " \
                  "JOIN possibleanswers ON questionbase.id_question = possibleanswers.id_question " \
                  "WHERE survey.id_survey = %s"
            cursor.execute(cmd, (survey_id))
            return cursor.fetchall()
        except:
            return redirect(url_for('msg_page'))
        finally:
            self.mysql_finalize()

    def add_question_to_questionbase(self, question_description, id_question_type):
        # dodaje pytanie do bazy pytan wraz z typem pytania (1 jednokrotny wybor, 2 wielokrotny wybor)
        cursor = self.mysql_connect()
        try:
            cmd = "INSERT INTO `questionbase`(`question_description`, `id_questiontype`) VALUES (%s, %s)"
            cursor.execute(cmd, (question_description, id_question_type))
            return cursor.fetchone()
        except:
            return redirect(url_for('msg_page'))

    # works
    def get_all_question_in_questionbase(self):
        # zwraca tylko dostepne pytania (te ktore moga byc uzyte w tworzeniu ankiety)
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT * FROM `questionbase` where active = 1"
            cursor.execute(cmd)
            return cursor.fetchall()
        except:
            return False

    def get_question_from_questionbase_by_tag(self, tag_description):
        # listuje pytania po tagacah
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT * FROM questiontags JOIN tags ON questiontags.id_tag = tags.id_tag JOIN questionbase ON questiontags.id_question = questionbase.id_question WHERE tag_description = %s"
            cursor.execute(cmd, (tag_description,))
            return cursor.fetchone()
        except:
            # do something
            return

    # works
    def get_possible_answers(self, id_question):
        # zwraca mozliwe odpowiedzi dla pytania
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT `id_answer`, `id_question`, `answerdescription` FROM `possibleanswers` WHERE id_question = %s and active = 1"
            cursor.execute(cmd, (id_question))
            return cursor.fetchall()
        except:
            return False

    def add_possible_answers(self, id_question, answerdescription):
        # dodaje mozliwe odpowiedzi do pytania
        cursor = self.mysql_connect()
        try:
            cmd = "INSERT INTO `possibleanswers`(`id_question`, `answerdescription`) VALUES (%s, %s)"
            cursor.execute(cmd, (id_question, answerdescription))
            return cursor.fetchone()
        except:
            # do something
            return redirect(url_for('msg_page'))

    def delete_possible_answer(self, id_answer):
        # admin oznacza mozliwa odpowiedz jako nieaktywna (actve = 0)
        cursor = self.mysql_connect()
        try:
            cmd = "UPDATE `possibleanswers` SET active = 0 where id_answer = %s"
            cursor.execute(cmd, (id_answer))
            return cursor.fetchone()
        except:
            # do something
            return redirect(url_for('msg_page'))

    # works
    def get_user_password(self, user_id):
        cursor = self.mysql_connect()
        cmd = "SELECT `pass` FROM `users` WHERE id_user = %s"
        try:
            cursor.execute(cmd, (user_id))
            return cursor.fetchone()[0]
        except:
            return False
        finally:
            self.mysql_finalize()

    def get_survey_owner(self, survey_id):
        # zwraca wlasciciela ankiety, to zwraca tworce szablonu a nie usera ktory wypelnil ankiete
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT  `id_user` FROM `survey` WHERE id_survey = %s"
            cursor.execute(cmd, (survey_id))
            return cursor.fetchone()
        except:
            return redirect(url_for('msg_page'))

    def get_survey_respondent(self, completedsurvey_id):
        # zwraca usera ktory wypelnil ankiete (respondenta)
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT  `id_user` FROM `completedsurvey` WHERE id_completedsurvey = %s"
            cursor.execute(cmd, (completedsurvey_id))
            return cursor.fetchone()
        except:
            return redirect(url_for('msg_page'))

    def get_question_owner(self, survey_id):
        return False

    def is_user_have_any_questions(self, user_id):
         return False

    def is_user_have_any_surveys(self, user_id):
        # zwraca liczbe ankiet (wzorccow) usera
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT  * FROM `survey` WHERE id_user = %s"
            cursor.execute(cmd, (user_id))
            return cursor.fetchone()
        except:
            return False

    def is_user_have_any_completed_surveys(self, user_id):
        # zwraca liczbe ankiet wypelnionych przez usera
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT  count(id_completedsurvey) AS NumberOfCompletedSurveys FROM `completedsurvey` WHERE id_user = = %s"
            cursor.execute(cmd, (user_id))
            return cursor.fetchone()
        except:
            return False

    def get_completedanswers_in_completedsurvey(self, completedsurvey_id):
        # zwraca, id szablonu, id pytan, id odpoodpowiedzi dla wypelnionej ankiety
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT * FROM `completedanswers` WHERE id_completedsurvey = %s"
            cursor.execute(cmd, (completedsurvey_id))
            return cursor.fetchone()
        except:
            return redirect(url_for('msg_page'))

    def get_completed_surveys(self, user_id):
        # zwraca wypelnione ankiety przez uzytownika (lista completedsurvey.id_completedsurvey, survey.id_survey, survey.survey_description, completedsurvey.datetime, completedsurvey.id_user)
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT completedsurvey.id_completedsurvey, survey.id_survey, survey.survey_description, completedsurvey.datetime, completedsurvey.id_user FROM `survey` left Join `completedsurvey` ON survey.id_survey = completedsurvey.id_survey WHERE completedsurvey.id_user = %s"
            cursor.execute(cmd, (user_id))
            completed_surveys = cursor.fetchall()
            return completed_surveys
        except:
            return redirect(url_for('msg_page'))

    def delete_question(self, question_id):
        # admin usuwa pytanie z bazy (tak naprawde wylaczymy pytanie active na '0', baza jest na ta chwile jednoczesnie slownikiem, wiec wywalenie rekordu usunie go z wypelnionych juz ankiet)
        cursor = self.mysql_connect()
        try:
            cmd = "UPDATE `questionbase` SET `active` = 0 WHERE id_question = %s"
            cursor.execute(cmd, question_id)
            return cursor.fetchone()
        except:
            return redirect(url_for('msg_page'))
        finally:
            self.mysql_finalize()

    def get_question_from_questionbase_by_id(self, question_id):
        cursor = self.mysql_connect()
        try:
            cmd = "SELECT * FROM `questionbase` where id_question = %s and active = 1"
            cursor.execute(cmd, (question_id))
            return cursor.fetchall()
        except:
            return False

    def get_correct_answer_for_specific_question(self, question_id):
        pass

    def add_completed_survey(self, id_survey, id_user):
        # wypelniona ankiete (uzupelnia tabele completedsurvey) add_completed_survey i add_completed_answers_for_completed_survey nalezy wywolac w momencie submit ( w podanej kolejnosci)# add_completed_answers_for_completed_survey nalezy wywolac dla kazdej dodwanej odpowiedzi #add_completed_survey dla ankiety trzeba wykonac tylko raz na samym poczatku po submit
        cursor = self.mysql_connect()
        try:
            cmd = "INSERT INTO `completedsurvey`(`id_survey`, `id_user`) VALUES (%s, %s)"
            cursor.execute(cmd, (id_survey, id_user))
            return cursor.fetchone()
        except:
            # do something
            return redirect(url_for('msg_page'))

    def add_completed_answers_for_completed_survey(self, id_surveytemplate, id_question, id_answer):
        cursor = self.mysql_connect()
        try:
            cmd = "INSERT INTO `completedanswers` (id_surveytemplate, id_question, id_answer, id_completedsurvey) VALUES (%s, %s, %s, (SELECT MAX(id_completedsurvey) from `completedsurvey` ))"
            cursor.execute(cmd, (id_surveytemplate, id_question, id_answer))
            return cursor.fetchone()
        except:
            # do something
            return redirect(url_for('msg_page'))

    def add_survey(self, id_user, survey_description):
        # tworzy nowa ankiete bez pytan sam "kontener"
        cursor = self.mysql_connect()
        try:
            cmd = "INSERT INTO `survey`(`id_user`, `survey_description`) VALUES (%s, %s)"
            cursor.execute(cmd, (id_user, survey_description))
            return cursor.fetchone()
        except:
            return redirect(url_for('msg_page'))
        finally:
			self.mysql_finalize()

    def add_surveytemplate(self, id_survey, id_question):
        # dodaje pytania do szablonu utworzonej ankiety (tej ktora zostala utworzona za pomoca add_survey)
        cursor = self.mysql_connect()
        try:
            cmd = "INSERT INTO `surveytemplate`(`id_survey`, `id_question`) VALUES (%s, %s)"
            cursor.execute(cmd, (id_survey, id_question))
        except:
            return redirect(url_for('msg_page'))
        finally:
			self.mysql_finalize()

    def delete_survey(self, id):
        cursor = self.mysql_connect()
        try:
            cmd = "delete from `surveytemplate` where id_survey = %s"
            cursor.execute(cmd, (id))
            cmd = "delete from `survey` where id_survey = %s"
            cursor.execute(cmd, (id))
        except:
            return redirect(url_for('msg_page'))
        finally:
            self.mysql_finalize()

    def disable_survey(self, id):
        cursor = self.mysql_connect()
        try:
            cmd = "update `survey` set active = 0 where id_survey = %s"
            cursor.execute(cmd, (id))
        except:
            return redirect(url_for('msg_page'))
        finally:
            self.mysql_finalize()
