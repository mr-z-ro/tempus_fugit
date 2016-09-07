# __init__.py
"""
__init__.py - this is the package controller for our app
"""
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
import logging

# [START imports]
from flask import Flask, render_template, request
from .models import User
from flask_login import LoginManager

# [END imports]

app = Flask(__name__,instance_relative_config=True)


login_manager = LoginManager() # create instance of LoginManager
login_manager.init_app(app) # initialize LoginManager instance with our app object
login_manager.login_view = 'login' # define the login view

@login_manager.user_loader
def load_user(userid):
	return User.query.filter(User.id==userid).first() # how to get a user object with user's id
	
# access config.py variables
app.config.from_object('config') # normal config.py
# Now we can access the configuration variables via app.config["VAR_NAME"].

app.config.from_pyfile('config.py') # instance/config.py access to secret keys
