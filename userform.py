from wtforms import Form, BooleanField, StringField, validators, EmailField, PasswordField

class UserForm(Form):
    first_name     = StringField('First Name', [validators.Length(min=4, max=25), validators.DataRequired()], render_kw={"placeholder": "First Name"})
    last_name     = StringField('Last Name', [validators.Length(min=4, max=25), validators.DataRequired()], render_kw={"placeholder": "Last Name"})
    occupation     = StringField('Occupation', [validators.Length(min=4, max=25), validators.DataRequired()], render_kw={"placeholder": "Occupation"})
    email        = EmailField('Email Address', [validators.Length(min=6, max=35), validators.DataRequired()], render_kw={"placeholder": "Email"})
    password   = PasswordField('Password', [validators.Length(min=6, max=35), validators.DataRequired()], render_kw={"placeholder": "Password"})
    verify_password   = PasswordField('Re Enter Password', [validators.Length(min=6, max=35), validators.DataRequired()], render_kw={"placeholder": "Re-Enter Password"})
    is_in_realestate = BooleanField('I work in Real-Estate')
    businessname = StringField('Business Name', [validators.Length(min=4, max=25), validators.Optional()], render_kw={"placeholder": "Business Name"})
    
    #fancy validators that we write ourselves
    def validate(self):
        if not super().validate():
           return False

        if self.password.data != self.verify_password.data:
            self.verify_password.errors.append('Passwords do not match')
            return False

        if self.is_in_realestate.data and not self.businessname.data:
            self.businessname.errors.append('Business name is required for users in real estate')
            return False

        return True
    
   