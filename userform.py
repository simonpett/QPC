from wtforms import Form, BooleanField, StringField, validators, EmailField, PasswordField

class UserForm(Form):
    first_name     = StringField('First Name', [validators.Length(min=4, max=25)])
    last_name     = StringField('Last Name', [validators.Length(min=4, max=25)])
    occupation     = StringField('Occupation', [validators.Length(min=4, max=25)])
    email        = EmailField('Email Address', [validators.Length(min=6, max=35)])
    password   = PasswordField('Password', [validators.Length(min=6, max=35)])
    verify_password   = PasswordField('Password', [validators.Length(min=6, max=35)])
    is_in_realestate = BooleanField('I accept the site rules', [validators.InputRequired()])
    businessname = StringField('Business Name', [validators.Length(min=4, max=25)])
    
    #fancy validators that we write ourselves
    def validate(self):
        if not super().validate():
           return False

        if self.password.data != self.verifyPassword.data:
            self.verifyPassword.errors.append('Passwords do not match')
            return False

        if self.is_in_realestate.data and not self.real_estate_business.data:
            self.real_estate_business.errors.append('Business name is required for users in real estate')
            return False

        return True
    
   