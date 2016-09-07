# app/forms.py - Forms for the project
from flask_wtf import Form
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import Required,Email,DataRequired

class loginForm(Form):
	username = StringField('User name:',validators=[Required(),Email()])
	password = PasswordField('Password:',validators=[Required()])
	submit = SubmitField('Submit')
	
class UsernamePasswordForm(Form):
	username = StringField('Username',validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired()])