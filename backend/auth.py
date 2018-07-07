import hashlib

class auth():
    def check_password(self, psw, psw_cfm):
        if psw == psw_cfm:
            return True
        return False

    def validate_email(self, email):
        return "@" in email and "." in email and len(email) >= 6

    def validate_username(self, username):
        return len(username) >= 4
    
    def hash(self, string):
        return hashlib.md5(
            string + "secret_salt^^string").hexdigest()