# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]

# [START imports]
from os import urandom

from flask import Flask
from flask_login import LoginManager

from app.controllers.tempus_fugit import mod_tempus_fugit
from datetime import timedelta
# [END imports]
from app.models import db

app = Flask(__name__)

##########################################################################################################################################
# global variables from config.py and instance/config.py
app.config.from_object('app.config') # normal config.py
app.config.from_pyfile('config.py') # instance/config.py access to secret keys
# Now we can access the configuration variables via app.config["VAR_NAME"].

# set a timeout for the session  to 5 days of inactivity /this  can change
app.permanent_session_lifetime = timedelta(seconds=432000)

#########################################################################################################################################
# the runtime process gave a bad HTTP response: got more than 65536 bytes when reading header line
# to avoid the error above we set _MAXLINE to 65536
# maximal amount of data to read at one time in _safe_read
MAXAMOUNT = 1048576

# maximal line length when calling readline().
_MAXLINE = 65536

# setting up flask-login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)
login_manager.login_view = 'mod_tempus_fugit.login'

secret_key = app.config['SECRET_KEY']
if not secret_key:
    secret_key = urandom(24)

# Define the database object which is imported by modules and controllers
# (See http://stackoverflow.com/a/9695045/604003 for explanation)
db.init_app(app)

# Register Blueprints
app.register_blueprint(mod_tempus_fugit)