from flask_wtf import Form
from wtforms import BooleanField, StringField, PasswordField,SubmitField, validators


class LoginForm(Form):
    username = StringField('Username', validators=[validators.Required(), validators.Email()])
    password = PasswordField('Password:', validators=[validators.Required()])
    submit = SubmitField('Submit')
