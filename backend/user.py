
class user():
    def __init__(self, db):
        self.db_ = db

    def try_to_login(self, username, psw):
        return True

    def has_admin_privileges(self, user_id):
        return False #todo

    def get_user_id(self, username):
        return self.db_.get_user_id(username)

    def is_survey_owner(self, survey_id, user_id):
        return False #todo

    def is_question_owner(self, question_id, user_id):
        return False #todo

    def get_user_data(self, user_id):
        return {"username" : "jasio", "email" : "jasio@jasio.pl"}
        #return db.get_user(session['username'])

    def check_if_username_is_free(self, username):
        return self.db_.check_if_username_is_free(username)