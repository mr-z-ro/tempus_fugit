from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash


class User:
    def __init__(self,username,password,company):
        self.username = username
        self.company = company
        self.password = password

    @property
    def is_active(self):
        """ True, as all users are active."""
        return True

    def get_id(self):
        """ Return the email address to satisfy Flask-Login's requirements."""
        #return self.username
        try:
            return unicode(self.username) # Python 2
        except NameError:
            return str(self.username) # Python 3
#       return self.username


    def is_authenticated(self):
        """ Return True if the user is authenticated."""
        return self.authenticated

    def set_authentication(self, auth=False):
        # this sets authentication based on NetSuite API resp
        self.authenticated = auth

    def is_anonymous(self):
        """ return False, as anonymous users aren't supported. """
        return False

    @hybrid_property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        #return self.password


    @password.setter
    def password(self,plaintext):
        self.password = generate_password_hash(plaintext, length=12)#bcrypt.generate_password_hash(plaintext)

    def __repr__(self):
        return '<User %r>' % (self.username)