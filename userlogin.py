from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# user class that inherits UserMixin so the flask login LoginManager can do session authentication
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
    def set_password(self, password):   # method to set password, hash the password before storing
        self.password = generate_password_hash(password)
    def check_password(self, password): # compare the arg password with the hashed password
        return check_password_hash(self.password, password)
    