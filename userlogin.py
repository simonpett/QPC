from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, firstname, lastname, occupation, email, password, businessname, is_admin):
        self.id = id
        self.first_name = firstname
        self.last_name = lastname
        self.occupation = occupation
        self.email = email
        self.password = password
        self.businessname = businessname
        self.is_admin = is_admin
       
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    # Check if the password argued is the same as the password in this User
    def check_password(self, password):
        return check_password_hash(self.password, password)