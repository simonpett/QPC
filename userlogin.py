from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# create a user class that inherits from UserMixin to support the flask login LoginManager do session authentication
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
    def check_password(self, password):
        return check_password_hash(self.password, password)
    