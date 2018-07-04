
class user():
    def __init__(self, db):
        self.db_ = db

    def try_to_login(self, user_id, psw):
        return self.db_.get_user_password(user_id) == psw

    def has_admin_privileges(self, privileges):
        return privileges == "admin"

    def get_user_id(self, username):
        return self.db_.get_user_id(username)

    def is_survey_owner(self, survey_id, user_id):
        return self.db_.get_survey_owner(survey_id) == user_id

    def is_question_owner(self, question_id, user_id):
        return self.db_.get_question_owner(question_id) == user_id

    def get_user_data(self, user_id):
        return self.db_.get_user_data(user_id)

    def check_if_username_is_free(self, username):
        return self.db_.check_if_username_is_free(username)