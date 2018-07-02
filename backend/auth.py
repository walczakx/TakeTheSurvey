import hashlib

class auth():
    def check_password(self, psw, psw_cfm):
        if psw == psw_cfm:
            return True
        return False

    def validate_email(self, email):
        # TODO if email contain @ and .
        return True

    def hash(self, string):
        return hashlib.md5(
            string + "secret_salt^^string").hexdigest()