# models.py
"""
models.py - module with database models defined. If there will be need to use a DB for this project then this will be used
"""
from sqlalchemy.ext.hybrid import hybrid_property

from . import bcrypt, db

# configurations for the databases
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' + os.path.join(basedir, 'data.sqlite')

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(128))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)
		
	def is_correct_password(self,plaintext):
		return bcrypt.check_password_hash(self._password,plaintext)
	
	def is_user_openair_allowed(self,password,netsuite_key):
		return True