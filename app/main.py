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
from flask import Flask, render_template, request,url_for, redirect, session,flash,g,Response
from flask_sqlalchemy import SQLAlchemy
from google.appengine.ext import ndb
from google.appengine.ext import db
from flask_wtf import Form
from wtforms import BooleanField, StringField, PasswordField,SubmitField, validators
from wrapper import *
from xmlwriter import *
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import LoginManager, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
#from webapp2_extras import security
from datetime import timedelta
from collections import OrderedDict
from functools import wraps
import pdb
from os import urandom
from datetime import datetime

from copy import deepcopy

import sys

# [END imports]

app = Flask(__name__)

##########################################################################################################################################
# global variables from config.py and instance/config.py
app.config.from_object('app.config') # normal config.py

app.config.from_pyfile('config.py') # instance/config.py access to secret keys
# Now we can access the configuration variables via app.config["VAR_NAME"].

# read company info from the config file out of verion control
my_company = app.config['COMPANY']
netsuite_key = app.config['NETSUITE_API_KEY'] # Retrieve key from instance/config file

# secret_key enables us to use csrf
secret_key = app.config['SECRET_KEY']
if not secret_key:
    secret_key = urandom(24)

# set a timeout for the session  to 5 days of inactivity /this  can change
app.permanent_session_lifetime = timedelta(seconds=432000)

# to prevent back button if logged out from opening previous page, ensure no caching happens
resp = Response("")
resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')

## create a dictionary to hold projects, users and bookings info
projects_dict = {}

users_dict = {}

bookings_dict = {}

#########################################################################################################################################
# the runtime process gave a bad HTTP response: got more than 65536 bytes when reading header line
# to avoid the error above we set _MAXLINE to 65536
# maximal amount of data to read at one time in _safe_read
MAXAMOUNT = 1048576

# maximal line length when calling readline().
_MAXLINE = 65536

#########################################################################################################################################
#format date value into a sensible value
def reformatDate(dictval):
	if dictval == 'None' or dictval == 'Null':
		myDate = 'None'
	else:
		simpledate = {}
		for attr in [u'year', u'month', u'day', u'hour', u'minute', u'second']:
			#print 'attr {}'.format(attr)
			try:
				simpledate[attr] = dictval[attr]
				# sanitize the value if None
			except KeyError,err:
				print 'error:: ',err
				# skip over missing values
				simpledate[attr] = ''
		# values that are missing time, minute and second values
		if simpledate['hour'] == None or simpledate['minute'] == None or simpledate['second'] == None:
			# if any elements of time is missing then exclude time from date
			myDate = "{}/{}/{}".format(simpledate['day'], simpledate['month'], simpledate['year'])
		else:
			myDate = "{}/{}/{} {}:{}:{}".format(simpledate['day'], simpledate['month'], simpledate['year'], simpledate['hour'], simpledate['minute'], simpledate['second'])
		return myDate

def date_percent_difference(start_date, end_date):
    """
    :param start_date:
    :param end_date:
    :return: dictionary of the form {'percent_days' : percent_days, 'days_consumed' : res_list['days_consumed'],
    'days_remaining' : res_list['days_remaining'], 'days_diff' : res_list['days_diff']}
    """
    res_list ={}

    curr_date = datetime.today()

    if start_date != 'None':
        day, mnth, yr = start_date[:10].split('/')
        starting_date = datetime(year = int(yr), month = int(mnth), day = int(day))

    if end_date != 'None':
        day, mnth, yr = end_date[:10].split('/')
        ending_date = datetime(year = int(yr), month = int(mnth), day = int(day))

    # verify that arguments passed have non-Nones
    if start_date == 'None' and end_date == 'None':
        res_list['days_consumed'] = 0
        res_list['days_diff'] = 0
        res_list['days_remaining'] = 0
    elif start_date == 'None' and end_date != 'None':
        res_list['days_consumed'] = 0
        res_list['days_diff'] = 0
        res_list['days_remaining'] = (ending_date - curr_date).days
    elif start_date != 'None' and end_date == 'None':
        res_list['days_consumed'] = (curr_date - starting_date).days
        res_list['days_diff'] = 0
        res_list['days_remaining'] = 0
    else:
        # compute total days from start to end date
        res_list['days_diff'] = (ending_date - starting_date).days
        res_list['days_consumed'] = (curr_date - starting_date).days
        res_list['days_remaining'] = (ending_date - curr_date).days

    if res_list['days_remaining'] > 0:
        percent_days = res_list['days_consumed'] * 100/ float(res_list['days_diff'])
    else:
        percent_days = 100.00

    return {'percent_days' : percent_days, 'days_consumed' : res_list['days_consumed'], 'days_remaining' : res_list['days_remaining'], 'days_diff' : res_list['days_diff']}

#########################################################################################################################################
#       models.py
#########################################################################################################################################

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

#################################################################################################################################################
# forms.py
#################################################################################################################################################


class LoginForm(Form):
    username = StringField('Username', validators=[validators.Required(), validators.Email()])
    password = PasswordField('Password:', validators=[validators.Required()])
    submit = SubmitField('Submit')


#################################################################################################################################################
# views.py
#################################################################################################################################################


@app.before_request
def before_request():
    session.modified = True

@app.context_processor
def inject_template_dict():
    return dict(users_dict = users_dict, projects_dict = projects_dict, bookings_dict = bookings_dict)

# [START 404]
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
# [END 404]


# [START 500]
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
# [END 500]

# create a dummy user
user = User(
            username=None,
            password=None,
            company=my_company
        )

# setting up flask-login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)
login_manager.login_view = 'login'


def login_required(func):
    """Requires standard login credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # if 'logged_in' not in session or 'username' not in session or session['username']=='' and not user.is_authenticated() and request.endpoint !=url_for('login'):
        session.modified = True
        try:
            # to catch keyerrors

            if ('logged_in' not in session) and ('username' not in session) and (session['username']=='' or session['username']== None) and (not user.is_authenticated()) and (request.endpoint !=url_for('login')):
                # session is non-existent but we still do the same
                return redirect(url_for('login',next=request.url))
        except Exception, err:
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)
    return decorated_view


@app.route('/logout',methods=['GET'])
@login_required
def logout():
    """Logout the current user"""
    #user = current_user;
    user.authenticated = False
    session['logged_in'] = False

    session['username']=''
    session['password'] = ''
    session['projects'] = ''
    session['logged_in']=''
    session.pop('username',None)
    session.pop('password', None)
    session.pop('logged_in',None)
    session.pop('projects', None)
    session.clear()

    #if all this does not clear the session
    # set a timeout for the session  to 1 seconds of inactivity /this  can change
    app.permanent_session_lifetime = timedelta(seconds=1)

    if 'username' not in session  or 'logged_in' not in session or session['username']=='' or session['logged_in']=='' and not user.is_authenticated():
        return redirect(url_for('login'))

    return render_template(url_for('login'))


# [START login]
@app.route('/login', methods=['GET', 'POST'])
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    # pdb.set_trace()
    # login functionality is implemented here
    # for GET requests, display the login form. For POST requests attempt to authenticate
    form = LoginForm(csrf_enabled=True) # instantiate the LoginForm with anti-CSRF enabled

    next = request.args.get('next')

    if form.validate_on_submit():
        # and request.method=='POST':
        # Login and validate the user

        # fetch the data from the form fields
        username = form.username.data
        password = form.password.data
        remember_me = False # ** need to implement on form

        # store username and password in encrypted session???
        session['username'] = username
        session['password'] = password

        if 'remember_me' in request.form:
            remember_me = True

        # make a call to the wrapper
        json_obj = get_whoami(key=netsuite_key, un=username, pw=password, company=my_company)
        # flash("json_obj : {}".format(json_obj['response']['Read']['Project']))
        auth = True if (json_obj['response']['Auth']['@status'])=='0' else False
        # set authentication on the user instance
        user.set_authentication(auth)
        if user.is_authenticated():
            # print "is_authenticated *********************************************************************************"
            # save the username to a session
            # session['username'] = form.username.data.split('@')[0] # Generate ID from email address
            session['associate'] = '%s, %s' % (json_obj['response']['Whoami']['User']['addr']['Address']['last'], json_obj['response']['Whoami']['User']['addr']['Address']['first'])
            session['associate_title'] = '%s' % (json_obj['response']['Whoami']['User']['type'])
            session['associate_email'] = '%s' % (json_obj['response']['Whoami']['User']['addr']['Address']['email'])
            session['associate_id'] = '%s' % (json_obj['response']['Whoami']['User']['id'])
            # login_user(user)
            session['logged_in'] = True
            # for session timeout to work we must set session permanent to True
            # session.permanent = True
            flash('Logged in successfully.')
            next = request.args.get('next')
            # next_is_valid should check if the user has validate
            # permission to access the 'next' url
            # if not next_is_valid(next):
            #    return abort(400)

            # user should be an instance of your 'User' class
            # login_user(user,remember=True)
            # redirect to projects page
            # return redirect(next or (url_for('index')))

            # flash("session Projects : {}".format(session['projects']))
            if next:
                session['currentpage'] = str(str(next).split('//')[-1:]).split('.')[:1]
            else:
                session['currentpage'] = 'projects'
            return redirect(next or url_for('index'))
        flash('Sorry! Your password or username is invalid. Kindly try again..')
    return render_template('login.html', form=form)

# [END login submitted]

# create a route to be called by jQuery to process data
# [START prepare_data]
@app.route('/prepare_data')
@login_required
def prepare_data():
    # project_dates will store dates related to projects, earliest used to estimate start date for projects with Null start date
    all_projects_dict = {}
    projects_dates = {}

    # make an API call to projects
    projects_json = raw_call_wrapper(key=netsuite_key,
                                     username=session['username'],
                                     passwd=session['password'], xml_str='''
                                                                                        <Read type= "Project" method = "equal to" limit = "500">
                                                                                            <Project>
                                                                                                <active>1</active>
                                                                                            </Project>
                                                                                        <_Return>
                                                                                            <id/>
                                                                                            <name/>
                                                                                            <active/>
                                                                                            <budget/>
                                                                                            <budget_time/>
                                                                                            <userid/>
                                                                                            <currency/>
                                                                                            <start_date/>
                                                                                            <finish_date/>
                                                                                            <project_stageid/>
                                                                                            <updated/>
                                                                                        </_Return>
                                                                                        </Read>
                                                                                   ''')
    # make API call to retrieve users name and rate
    users_json = raw_call_wrapper(key=netsuite_key,
                                  username=session['username'],
                                  passwd=session['password'], xml_str='''
                                                                                        <Read type= "User" method = "equal to" limit = "500">
                                                                                        <_Return>
                                                                                            <name/>
                                                                                            <active/>
                                                                                            <timezone/>
                                                                                            <currency/>
                                                                                            <id/>
                                                                                            <rate/>
                                                                                            <line_managerid/>
                                                                                            <nickname/>
                                                                                            <departmentid/>
                                                                                        </_Return>
                                                                                        </Read>
                                                                                   ''')

    # make API call to retrieve timesheet entries
    tasks_json = raw_call_wrapper(key=netsuite_key,
                                  username=session['username'],
                                  passwd=session['password'], xml_str='''
                                                                                        <Read type= "Task" method = "all" limit = "500">
                                                                                        <_Return>
                                                                                            <projectid/>
                                                                                            <projecttaskid/>
                                                                                            <decimal_hours/>
                                                                                            <userid/>
                                                                                            <date/>
                                                                                            <updated/>
                                                                                            <hours/>
                                                                                            <minutes/>
                                                                                            <timesheetid/>
                                                                                            <cost_centerid/>
                                                                                        </_Return>
                                                                                        </Read>
                                                                                   ''')

    # API call to retrieve Tickets info form Netsuite Openair
    tickets_json = raw_call_wrapper(key=netsuite_key,
                                    username=session['username'],
                                    passwd=session['password'], xml_str='''
                                                                                                    <Read type= "Ticket" method = "all" limit = "500">
                                                                                                    <_Return>
                                                                                                        <id/>
                                                                                                        <date/>
                                                                                                        <updated/>
                                                                                                        <unitm/>
                                                                                                        <total_no_tax/>
                                                                                                        <cost/>
                                                                                                        <total/>
                                                                                                        <project_taskid/>
                                                                                                        <userid/>
                                                                                                        <projectid/>
                                                                                                        <currency/>
                                                                                                        <city/>
                                                                                                        <quantity/>
                                                                                                        <acct_date/>
                                                                                                        <total_tax_paid/>
                                                                                                    </_Return>
                                                                                                    </Read>
                                                                                               ''')

    # Booking information is needed, pull only approved bookings
    bookings_json = raw_call_wrapper(key=netsuite_key,
                                     username=session['username'],
                                     passwd=session['password'], xml_str='''
                                                                                            <Read type= "Booking" method = "all" limit = "500">
                                                                                                <Booking>
                                                                                                    <approval_status>A</approval_status>
                                                                                                </Booking>
                                                                                                <_Return>
                                                                                                    <ownerid/>
                                                                                                    <userid/>
                                                                                                    <projectid/>
                                                                                                    <startdate/>
                                                                                                    <enddate/>
                                                                                                    <percentage/>
                                                                                                    <hours/>
                                                                                                    <project_taskid/>
                                                                                                    <as_percentage/>
                                                                                                </_Return>
                                                                                            </Read>
                                                                                            ''')

    users_name = session['username'].strip()
    # ensure that the user_dict is tagged with this user's name

    if users_name not in users_dict.iterkeys():
        users_dict[users_name] = {}

    # ensure that the projects_dict is tagged with this user's name
    if users_name not in projects_dict.iterkeys():
        projects_dict[users_name] = {}

    # ensure that the bookings_dict is tagged with this user's name
    if users_name not in bookings_dict.iterkeys():
        bookings_dict[users_name] = {}

    # loop through the users_json
    for a_user in users_json['response']['Read']['User']:

        # extract the user_id
        user_id = a_user['id']

        try:
            # populate with a user_id
            users_dict[users_name][user_id]['name'] = a_user['name']
            users_dict[users_name][user_id]['nickname'] = a_user['nickname']
            users_dict[users_name][user_id]['timezone'] = a_user['timezone']
            users_dict[users_name][user_id]['rate'] = float(a_user['rate']) if a_user['rate'] != None else 0.00
            users_dict[users_name][user_id]['line_managerid'] = a_user['line_managerid']
            users_dict[users_name][user_id]['currency'] = a_user['currency']
            users_dict[users_name][user_id]['departmentid'] = a_user['departmentid']
            users_dict[users_name][user_id]['active'] = a_user['active']
            # print 'user_dict try'

        except KeyError, err:
            users_dict[users_name][user_id] = {
                'name': a_user['name'],
                'nick_name': a_user['nickname'],
                'time_zone': a_user['timezone'],
                'rate': float(a_user['rate']) if a_user['rate'] != None else 0.00,
                'line_manager_id': a_user['line_managerid'],
                'currency': a_user['currency'],
                'department_id': a_user['departmentid'],
                'active': a_user['active']
            }
            # flash("users_dict[users_name] keyerror: %s %s" % (err, user_id))
            # non-existent user
            # print 'user_dict exception part'
        except Exception, err:
            flash('Detected error {} with users_json_obj'.format(err))

    # flash('users_dict[users_name]: %s' % users_dict[users_name])
    # loop through the projects_json
    for project in projects_json['response']['Read']['Project']:
        pid = project['id']
        calc_start_date = reformatDate(project['start_date']['Date'])
        calc_end_date = reformatDate(project['finish_date']['Date'])

        if calc_start_date != 'None':
            my_start_date = calc_start_date
            if len(calc_start_date) > 10:
                my_start_date = calc_start_date.split(' ')[0]
            my_day, my_mnth, my_yr = my_start_date.split('/')
            start_date_str = '{2}/{1:0>2}/{0:0>2}'.format(my_yr, my_mnth, my_day)
        else:
            my_start_date = 'None'
            start_date_str = 'None'

        if calc_end_date != 'None':
            my_end_date = calc_end_date
            if len(calc_end_date) > 10:
                my_end_date = calc_end_date.split(' ')[0]
            my_day, my_mnth, my_yr = my_end_date.split('/')
            end_date_str = '{2}/{1:0>2}/{0:0>2}'.format(my_yr, my_mnth, my_day)  # changed from '{2}/{1}/{0}
        else:
            my_end_date = 'None'
            end_date_str = 'None'
        project_days = date_percent_difference(start_date_str, end_date_str)

        try:
            projects_dict[users_name][pid]['name'] = project['name']
            projects_dict[users_name][pid]['budget'] = float(
                project['budget'])  # 'budget' : '{:,.2f}'.format(float(project['budget']))
            projects_dict[users_name][pid]['budget_time'] = float(project['budget_time']) if project[
                                                                                                 'budget_time'] != None else 0.00
            projects_dict[users_name][pid]['owner_id'] = project['userid']
            projects_dict[users_name][pid]['currency'] = project['currency']
            projects_dict[users_name][pid]['start_date'] = calc_start_date
            projects_dict[users_name][pid]['finish_date'] = calc_end_date
            projects_dict[users_name][pid]['project_stageid'] = project['project_stageid']
            projects_dict[users_name][pid]['updated'] = reformatDate(project['updated']['Date'])
            projects_dict[users_name][pid]['percent_complete_days'] = project_days['percent_days']
            projects_dict[users_name][pid]['days_consumed'] = project_days['days_consumed']
            projects_dict[users_name][pid]['days_remaining'] = project_days['days_remaining']
            projects_dict[users_name][pid]['days_diff'] = project_days['days_diff']
            projects_dict[users_name][pid]['tasks'] = {}
            projects_dict[users_name][pid]['users'] = {}
            projects_dict[users_name][pid]['fees_worked'] = 0.0

        except KeyError:
            projects_dict[users_name][pid] = {
                'name': project['name'],
                'budget': float(project['budget']),
                'budget_time': float(project['budget_time']) if project['budget_time'] != None else 0.00,
                'owner_id': project['userid'],
                'currency': project['currency'],
                'start_date': calc_start_date,
                'finish_date': calc_end_date,
                'project_stageid': project['project_stageid'],
                'updated': reformatDate(project['updated']['Date']),
                'percent_complete_days': project_days['percent_days'],
                'days_consumed': project_days['days_consumed'],
                'days_remaining': project_days['days_remaining'],
                'days_diff': project_days['days_diff'],
                'fees_worked': 0.0,
                'tasks': {},
                'users': {}
            }
            # print 'projects_dict except part'

        # maintain sets of start and end dates
        try:
            projects_dates[pid]['start_dates'].add(calc_start_date)
            projects_dates[pid]['end_dates'].add(calc_end_date)
        except KeyError:
            projects_dates[pid] = {'start_dates': set([calc_start_date, ]), 'end_dates': set([calc_end_date, ])}

    for tasks in tasks_json['response']['Read']['Task']:
        project_id = tasks['projectid']
        task_id = tasks['projecttaskid']
        user_id = tasks['userid']
        task_hours = float(tasks['hours']) if tasks['hours'] != None else 0.00

        # extract the rate for the user
        try:
            user_rate = float(users_dict[users_name][user_id]['rate']) if users_dict[users_name][user_id][
                                                                              'rate'] != None else 0.00
        except KeyError:
            user_rate = 0.00
            # flash('Error reading userid:{} rate, non-existent'.format(user_id))

        # compute total hours worked per project
        fees_worked = task_hours * user_rate

        if project_id not in projects_dict[users_name].keys():
            # track fees_worked, users and hours_worked in projects_dict
            projects_dict[users_name][project_id] = {
                'fees_worked': fees_worked,
                'hours_worked': task_hours,
                'users': {
                    user_id: {
                        task_id: {
                            'total_hours': task_hours,
                            'total_fees': fees_worked
                        }
                    }
                }
            }
        else:
            # update fees_worked and 'hours_worked
            try:
                projects_dict[users_name][project_id]['fees_worked'] += fees_worked
            except KeyError:
                projects_dict[users_name][project_id]['fees_worked'] = fees_worked
        try:
            projects_dict[users_name][project_id]['users'][user_id][task_id]['total_hours'] += task_hours
            projects_dict[users_name][project_id]['users'][user_id][task_id]['total_fees'] += fees_worked
        except KeyError:
            try:
                projects_dict[users_name][project_id]['users'][user_id][task_id]['total_hours'] = task_hours
                projects_dict[users_name][project_id]['users'][user_id][task_id]['total_fees'] = fees_worked
            except KeyError:
                try:
                    projects_dict[users_name][project_id]['users'][user_id][task_id] = {
                        'total_hours': task_hours,
                        'total_fees': fees_worked
                    }
                except KeyError:
                    try:
                        projects_dict[users_name][project_id]['users'][user_id] = {
                            task_id: {
                                'total_hours': task_hours,
                                'total_fees': fees_worked
                            }
                        }
                    except KeyError:
                        try:
                            projects_dict[users_name][project_id]['users'] = {
                                user_id: {task_id: {
                                    'total_hours': task_hours,
                                    'total_fees': fees_worked
                                }
                                }
                            }
                        except KeyError:
                            flash(
                                "Strange error for projects_dict[users_name][project_id]['users'] = {user_id: {task_id: "
                                "{'total_hours': task_hours, 'total_fees': task_hours * user_rate}}}")
        except Exception, err:
            flash("projects_dict[pid] errors: {}".format(err))

        # compute total hours used per project by each user and save in projects_dict[users_name][project_id]['users'][user_id]['total_hrs_used']
        try:
            projects_dict[users_name][project_id]['users'][user_id]['total_hrs_used'] += task_hours
            # flash("projects_dict[users_name][project_id]['users'][user_id]['total_hrs_used']+ ok ")
        except KeyError:
            try:
                projects_dict[users_name][project_id]['users'][user_id]['total_hrs_used'] = task_hours
                # flash("projects_dict[users_name][project_id]['users'][user_id]['total_hrs_used']= ok ")
            except KeyError:
                try:
                    projects_dict[users_name][project_id]['users'][user_id] = {
                        'total_hrs_used': task_hours
                    }
                    # flash("projects_dict[users_name][project_id]['users'][user_id] = {'total_hrs_used' : task_hours } ok ")
                except KeyError:
                    projects_dict[users_name][project_id]['users'] = {
                        user_id: {
                            'total_hrs_used': task_hours
                        }
                    }
                    flash("Strange error with projects_dict")

        # ensure dictionary values exist before trying to access them
        if 'tasks' not in projects_dict[users_name][project_id].keys():
            projects_dict[users_name][project_id]['tasks'] = {}

        if task_id not in projects_dict[users_name][project_id]['tasks'].keys():
            projects_dict[users_name][project_id]['tasks'][task_id] = {}

        try:
            # evaluate need for computation of tasks in projects_dict if succinct_projects_task already has this info
            projects_dict[users_name][project_id]['tasks'][task_id]['total_hours'] += task_hours
        except KeyError, err:
            projects_dict[users_name][project_id]['tasks'][task_id]['total_hours'] = task_hours

        # track total hours worked per user per project
        try:
            projects_dict[users_name][project_id]['users'][user_id]['total_hours'] += task_hours
        except KeyError:
            try:
                projects_dict[users_name][project_id]['users'][user_id]['total_hours'] = task_hours
            except KeyError:
                try:
                    projects_dict[users_name][project_id]['users'][user_id] = {'total_hours': task_hours}
                except KeyError, err:
                    try:
                        projects_dict[users_name][project_id]['users'] = {user_id: {'total_hours': task_hours}}
                    except KeyError:
                        flash(
                            "projects_dict[users_name][project_id]['users']= {user_id : {'total_hours': task_hours}} failed")

    # loop through the tickets and compute the additional expense
    for ticket in tickets_json['response']['Read']['Ticket']:
        total = float(ticket['total']) if ticket['total'] != None else 0.00
        project_id = ticket['projectid']
        user_id = ticket['userid']

        # track expenses per project/ per user
        try:
            projects_dict[users_name][project_id]['users'][user_id]['expenses'] += total
        except KeyError:
            try:
                projects_dict[users_name][project_id]['users'][user_id]['expenses'] = total
            except KeyError:
                try:
                    projects_dict[users_name][project_id]['users'][user_id] = {'expenses': total}
                except KeyError:
                    flash(
                        "Unexpected projects_dict[users_name][project_id]['users'][user_id] = {'expenses' : total} fail")

        try:
            projects_dict[users_name][project_id]['fees_worked'] += total
        except KeyError:
            projects_dict[users_name][project_id]['fees_worked'] = total

    for booking in bookings_json['response']['Read']['Booking']:
        """ restructure bookings into
            {project_id:{'tot_booked_hrs' : XY + 'hours',
                    task_id : {
                        user_id1 : {
                            'hours' : 40,
                            'percentage' : 45%,
                            'start_date' : date1,
                            'end_date'   : date2
                        },
                        user_id2 : {
                            'hours' : 30,
                            'percentage' : 35%,
                            'start_date' : date1,
                            'end_date'   : date2
                        }
                    },
                    'users_proj_hours' : {
                                19: XY# total_hours_booked,
                                23: YZ
                              }
                }
            }
        """
        project_id = booking['projectid']
        task_id = booking['project_taskid']
        user_id = booking['userid']
        hours_booked = float(booking['hours']) if booking['hours'] != None else 0.0
        hours_percent = float(booking['percentage']) if booking['percentage'] != None else 0.0

        # try the bookings_dict
        # try the bookings_dict
        """
        if users_name not in bookings_dict.iterkeys():
            # initialize the bookings_dict
            bookings_dict[users_name] = {project_id:
                    {

                    'tot_booked_hrs': 0.0,
                    'users_proj_hours': {user_id: 0.0},
                    task_id: {
                            'total_task_hrs': hours_booked,
                            user_id: {
                                'hours': hours_booked,
                                'percentage': hours_percent
                            }
                        }
                    }
            }
            """
        if project_id not in bookings_dict[users_name].iterkeys():
            # initialize the bookings_dict
            bookings_dict[users_name][project_id] = {
                'tot_booked_hrs': 0.0,
                'users_proj_hours': {user_id: 0.0},
                task_id: {
                    'total_task_hrs': hours_booked,
                    user_id: {
                        'hours': hours_booked,
                        'percentage': hours_percent
                    }
                }
            }

        try:
            bookings_dict[users_name][project_id]['tot_booked_hrs'] += hours_booked
        except KeyError:
            try:
                bookings_dict[users_name][project_id]['tot_booked_hrs'] = hours_booked
            except KeyError:
                bookings_dict[users_name][project_id] = {'tot_booked_hrs': hours_booked}
        # compute total project hours for a user (from all tasks booked)
        try:
            bookings_dict[users_name][project_id]['users_proj_hours'][user_id] += hours_booked
        except KeyError:
            try:
                bookings_dict[users_name][project_id]['users_proj_hours'][user_id] = hours_booked
            except KeyError:
                try:
                    bookings_dict[users_name][project_id]['users_proj_hours'] = {user_id: hours_booked}
                except Exception, err:
                    flash("Error :{} from bookings_dict".format(err))

        try:
            bookings_dict[users_name][project_id][task_id]['total_task_hrs'] += hours_booked
        except KeyError:
            try:
                bookings_dict[users_name][project_id][task_id]['total_task_hrs'] = hours_booked
            except KeyError:
                bookings_dict[users_name][project_id][task_id] = {'total_task_hrs': hours_booked}

        try:
            bookings_dict[users_name][project_id][task_id][user_id] = {
                'hours': hours_booked,
                'percentage': booking['percentage']
            }
        except KeyError:
            try:
                bookings_dict[users_name][project_id][task_id] = {user_id: {
                    'hours': hours_booked,
                    'percentage': booking['percentage']
                }
                }
            except KeyError, err:
                flash("Issues with bookings dict: {}".format(err))

    # create global dictionaries for projects, users
    app.add_template_global(users_dict, 'users_dict')
    app.add_template_global(projects_dict, 'projects_dict')
    app.add_template_global(bookings_dict, 'bookings_dict')
    return render_template(url_for('index'), users_dict = users_dict)

# [START projects]
@app.route('/projects')
@login_required
def projects():
    """ # Retrieve projects from API
    projects_json_obj = get_projects(key=netsuite_key,
                                     un=session['username'],
                                     pw=session['password'],
                                     company=my_company,
                                     userid=session['associate_id'])

    #print 'size [{} bytes]Projects json obj: {} '.format( sys.getsizeof(projects_json_obj), projects_json_obj)
    # Retrieve tasks from API
    tasks_json_obj = get_tasks(key=netsuite_key,
                               un=session['username'],
                               pw=session['password'],
                               company=my_company)

    project_dates = {}

    #users_dict = {}
    all_users_json_obj = raw_call_wrapper(key=netsuite_key,
                                           username=session['username'],
                                           passwd=session['password'], xml_str='''
                                                                                <Read type= "User" method = "all" limit = "500">
                                                                                <_Return>
                                                                                    <name/>
                                                                                    <picklist_label/>
                                                                                    <cost_centerid/>
                                                                                    <active/>
                                                                                    <timezone/>
                                                                                    <addr/>
                                                                                    <currency/>
                                                                                    <id/>
                                                                                    <rate/>
                                                                                    <line_managerid/>
                                                                                    <nickname/>
                                                                                    <departmentid/>
                                                                                </_Return>
                                                                                </Read>
                                                                           ''')

    #flash('Hey yah! mock users: {}'.format( all_users_json_obj))  # user_info))
    for a_user in all_users_json_obj['response']['Read']['User']:

        try:
            # populate with a user_id
            users_dict[a_user['id']] = {'name' : a_user['name'],
                                        'nick_name' : a_user['nickname'],
                                        'time_zone' : a_user['timezone'],
                                        'rate' : a_user['rate'],
                                        'cost_centerid' : a_user['cost_centerid'],
                                        'line_manager_id' : a_user['line_managerid'],
                                        'picklist_label' : a_user['picklist_label'],
                                        'department_id' : a_user['departmentid']}
        except KeyError:
            flash ('check the users_json_obj')
        except Exception, err:
            flash('Detected error {} with users_json_obj'.format(err))
    # adding the users_dict into the global namespace, available to all templates
    app.add_template_global(users_dict, 'users_dict')

    # Prepare a project list to pass to projects page
    for project in projects_json_obj['response']['Read']['Project']:

        # populate the dictionary
        pid = project['id']





        projects_dict[pid] = {'name' : project['name'],
                              'active' : project['active'],
                              'budget' : '{:,.2f}'.format(float(project['budget'])),
                              'budget_time' : project['budget_time'],
                              'customer_name' : project['customer_name'],
                              'user_id' : project['userid'],
                              'currency' : project['currency'],
                              'start_date' : project['start_date'],
                              'finish_date' : project['finish_date'],
                              'project_stageid' : project['project_stageid'],
                              'pm_approver_1' : project['pm_approver_1'],
                              'pm_approver_2': project['pm_approver_2'],
                              'pm_approver_3': project['pm_approver_3'],
                              'updated' : reformatDate(project['updated']['Date']),
                              'picklist_label' : project['picklist_label'],
                              'tasks' : {}}
        project_dates[pid] = {'start_dates' : set(), 'end_dates' : set()}

    # Prepare a task list to pass to projects page
    for project_tasks in tasks_json_obj['response']['Read']['Projecttask']:

        # Retrieve project and task ids
        pid = project_tasks['projectid']
        tid = project_tasks['id']

        # cycle through the project_tasks and populate the dictionary with active projects only
        if pid in projects_dict:
            calc_start_date = reformatDate(project_tasks['calculated_starts']['Date']) if project_tasks['calculated_starts']['Date'] != 'None' else 'None'
            calc_end_date = reformatDate(project_tasks['calculated_finishes']['Date']) if project_tasks['calculated_finishes']['Date'] != 'None' else 'None'

            if calc_start_date != 'None':
                my_start_date = calc_start_date
                if len(calc_start_date) > 10:
                    my_start_date = calc_start_date.split(' ')[0]
                my_day, my_mnth, my_yr = my_start_date.split('/')
                start_date_str = '{2}/{1}/{0}'.format(my_yr, my_mnth, my_day)
            else:
                my_start_date = 'None'
                start_date_str = 'None'

            if calc_end_date != 'None':
                my_end_date = calc_end_date
                if len(calc_end_date) > 10:
                    my_end_date = calc_end_date.split(' ')[0]
                my_day, my_mnth, my_yr = my_end_date.split('/')
                end_date_str = '{2}/{1}/{0}'.format(my_yr, my_mnth, my_day)
            else:
                my_end_date = 'None'
                end_date_str = 'None'
            task_days = date_percent_difference(start_date_str, end_date_str)

            #populate the project dates set
            if calc_start_date != 'None':
                day, mnth, yr = calc_start_date[:10].split('/')
                start_date_num = int('{}{}{}'.format(yr, mnth, day))
                try:
                    project_dates[pid]['start_dates'].add(start_date_num)

                except KeyError, err:
                    project_dates[pid] = {'start_dates' : set(start_date_num)}

            if calc_end_date != 'None':
                day, mnth, yr = calc_end_date[:10].split('/')
                end_date_num =  int('{}{}{}'.format(yr, mnth, day))
                try:
                    project_dates[pid]['end_dates'].add(end_date_num)

                except KeyError, err:
                    project_dates[pid] = {'end_dates' : set(end_date_num)}

            try:
                projects_dict[pid]['tasks'][tid] = {'name': project_tasks['name'],
                                                    'calcstartdate': calc_start_date,
                                                    'calcenddate': calc_end_date,
                                                    'priority': project_tasks['priority'],
                                                    'percent_complete': project_tasks['percent_complete'],
                                                    'estimated_hours': project_tasks['estimated_hours'],
                                                    'planned_hours': project_tasks['planned_hours'],
                                                    'updated': projects_dict[pid]['updated'],
                                                    'task_budget_cost' : project_tasks['task_budget_cost'],
                                                    'customer_name' : project_tasks['customer_name'],
                                                    'percent_days' : task_days['percent_days'],
                                                    'days_consumed' : task_days['days_consumed'],
                                                    'days_remaining' : task_days['days_remaining'],
                                                    'days_diff' : task_days['days_diff']}
            except KeyError, err:
                print 'Errors: ', err

    #session['projects_dict'] = str(projects_dict)

    # create an ordered dict
    ordered_project_tasks = OrderedDict()
    for key in sorted(projects_dict.keys()):
        key = unicode(key)

        # create an ordered dict for the task_keys
        ordered_tasks = OrderedDict()
        for task_key in sorted({int(k): v for (k, v) in projects_dict[key]['tasks'].items()}):
            task_key = unicode(task_key)
            ordered_tasks[task_key] = projects_dict[key]['tasks'][task_key]

        # populate the ordered_project_tasks with the ordered tasks list
        try:
            # if there are existing tasks, then update
            ordered_project_tasks[key]['tasks'].update(ordered_tasks)
        except KeyError, err:
            try:
                ordered_project_tasks[key] = {'tasks': ordered_tasks}
            except KeyError, err:
                print err, ' basically a cooked goose!!'

        my_start_date = str(min(project_dates[key]['start_dates']))
        start_date_str = '{}/{}/{}'.format(my_start_date[6:], my_start_date[4:6], my_start_date[:4])

        my_end_date = str(max(project_dates[key]['end_dates']))
        end_date_str =  '{}/{}/{}'.format(my_end_date[6:], my_end_date[4:6], my_end_date[:4])
        # add the other elements
        # print 'ordered_project_tasks[key] = {}'.format(ordered_project_tasks[key])
        ordered_project_tasks[key]['updated'] = projects_dict[key]['updated']
        ordered_project_tasks[key]['active'] = projects_dict[key]['active']
        ordered_project_tasks[key]['name'] = projects_dict[key]['name']
        ordered_project_tasks[key]['budget'] = projects_dict[key]['budget']
        ordered_project_tasks[key]['budget_time'] = projects_dict[key]['budget_time']
        ordered_project_tasks[key]['test_start_date'] = start_date_str
        ordered_project_tasks[key]['test_end_date'] = end_date_str
        days_consumption = date_percent_difference(start_date_str, end_date_str) # returns dict

        ordered_project_tasks[key]['percent_complete_days'] = days_consumption['percent_days']
        ordered_project_tasks[key]['days_consumed'] = days_consumption['days_consumed']
        ordered_project_tasks[key]['days_remaining'] = days_consumption['days_remaining']
        ordered_project_tasks[key]['days_diff'] = days_consumption['days_diff']
        ordered_project_tasks[key]['percent_complete_days'] = days_consumption['percent_days']

    # adding the orderedprojecttasks into the global namespace, available to all templates
    app.add_template_global(ordered_project_tasks, 'projects_dict')

    #flash('pword: {}'.format(session['password']))

    # clear some memory by clearing list and dict, the page never loads due to memory limitation
    # projects_dict.clear()
    projectslist = None
    # print 'Eventual projects dict: ', projects_dict
    """

    return render_template('projects.html')
# [END projects]


# [START project_detail]
@app.route('/projects/<project_id>', methods=['GET','POST'])
@login_required
def project_detail(project_id):
    if project_id and ("|" in project_id):

        # separate the project and task id for template processing
        project_id = project_id.strip()  # remove any trailing spaces
        pid, tid = project_id.split('|')
        pid = unicode(pid)
        tid = unicode(tid)

        # refresh task list?
        # json_obj = get_tasks(netsuite_key,
        #                     session['username'],
        #                     session['password'],
        #                     company=my_company,
        #                     projectid=pid)

        return render_template('richtasks.html', project_id=pid, taskid=tid)
    else:
        project_id = project_id.strip()  # remove any trailing spaces
        pid = unicode(project_id)

        return render_template('richproject.html', project_id =project_id)

    return redirect(url_for('projects'))
# [END project_detail]

# [START navbar]
@app.route('/navbar', methods=['GET','POST'])
@app.route('/navbar.html')
@login_required
def navbar():
    return render_template('navbar.html')
# [END navbar]

# [START resources]
@app.route('/resources/<user_id>', methods= ['GET', 'POST'])
@login_required
def resources(user_id):
    return render_template('profile.html', user_id = user_id)
# [END resources]
#############################################
#
#  All endpoints below are from the template
#  and are not yet customized. Make sure to
#  copy them to the section above and rename
#  the methods and routes if you plan to use
#  them for Tempus Fugit.
#
#############################################


# [START agile_board]
@app.route('/agile_board.html')
@login_required
def agile_board():
    return render_template('agile_board.html')
# [END agile_board]


# [START article]
@app.route('/article.html')
@login_required
def article():
    return render_template('article.html')
# [END boxed]


# [START badges_labels]
@app.route('/badges_labels.html')
@login_required
def badges_labels():
    return render_template('badges_labels.html')
# [END badges_labels]


# [START basic_gallery]
@app.route('/basic_gallery.html')
@login_required
def basic_gallery():
    return render_template('basic_gallery.html')
# [END basic_gallery]


# [START blog]
@app.route('/blog.html')
@login_required
def blog():
    return render_template('blog.html')
# [END basic_gallery]


# [START buttons]
@app.route('/buttons.html')
@login_required
def buttons():
    return render_template('buttons.html')
# [END buttons]


# [START c3]
@app.route('/c3.html')
@login_required
def c3():
    return render_template('c3.html')
# [END c3]

# [START c4]
@app.route('/c4.html')
@login_required
def c4():
    return render_template('c4.html')
# [END c4]

# [START calendar]
@app.route('/calendar.html')
@login_required
def calendar():
    return render_template('calendar.html')
# [END calendar]


# [START carousel]
@app.route('/carousel.html')
@login_required
def carousel():
    return render_template('carousel.html')
# [END carousel]


# [START chat_view]
@app.route('/chat_view.html')
@login_required
def chat_view():
    return render_template('chat_view.html')
# [END chat_view]


# [START clients]
@app.route('/clients.html')
@login_required
def clients():
    return render_template('clients.html')
# [END clients]


# [START clipboard]
@app.route('/clipboard.html')
@login_required
def clipboard():
    return render_template('clipboard.html')
# [END clipboard]


# [START code_editor]
@app.route('/code_editor.html')
@login_required
def code_editor():
    return render_template('code_editor.html')
# [END code_editor]


# [START contacts]
@app.route('/contacts.html')
@login_required
def contacts():
    return render_template('contacts.html')
# [END contacts]


# [START contacts_2]
@app.route('/contacts_2.html')
@login_required
def contacts_2():
    return render_template('contacts_2.html')
# [END contacts_2]


# [START css_animation]
@app.route('/css_animation.html')
@login_required
def css_animation():
    return render_template('css_animation.html')
# [END css_animation]


# [START dashboard_2]
@app.route('/dashboard_2.html')
@login_required
def dashboard_2():
    return render_template('dashboard_2.html')
# [END dashboard_2]


# [START dashboard_3]
@app.route('/dashboard_3.html')
@login_required
def dashboard_3():
    return render_template('dashboard_3.html')
# [END dashboard_3]


# [START dashboard_4]
@app.route('/dashboard_4.html')
@login_required
def dashboard_4():
    return render_template('dashboard_4.html')
# [END dashboard_4]


# [START dashboard_4_1]
@app.route('/dashboard_4_1.html')
@login_required
def dashboard_4_1():
    return render_template('dashboard_4_1.html')
# [END dashboard_4_1]


# [START dashboard_5]
@app.route('/dashboard_5.html')
@login_required
def dashboard_5():
    return render_template('dashboard_5.html')
# [END dashboard_5]


# [START diff]
@app.route('/diff.html')
@login_required
def diff():
    return render_template('diff.html')
# [END diff]


# [START draggable_panels]
@app.route('/draggable_panels.html')
@login_required
def draggable_panels():
    return render_template('draggable_panels.html')
# [END draggable_panels]


# [START ecommerce-cart]
@app.route('/ecommerce-cart.html')
@login_required
def ecommerce_cart():
    return render_template('ecommerce-cart.html')
# [END ecommerce-cart]


# [START ecommerce-orders]
@app.route('/ecommerce-orders.html')
@login_required
def ecommerce_orders():
    return render_template('ecommerce-orders.html')
# [END ecommerce-orders]


# [START ecommerce_payments]
@app.route('/ecommerce_payments.html')
@login_required
def ecommerce_payments():
    return render_template('ecommerce_payments.html')
# [END ecommerce_payments]


# [START ecommerce_product]
@app.route('/ecommerce_product.html')
@login_required
def ecommerce_product():
    return render_template('ecommerce_product.html')
# [END ecommerce_product]


# [START ecommerce_product_detail]
@app.route('/ecommerce_product_detail.html')
@login_required
def ecommerce_product_detail():
    return render_template('ecommerce_product_detail.html')
# [END ecommerce_product_detail]


# [START ecommerce_product_list]
@app.route('/ecommerce_product_list.html')
@login_required
def ecommerce_product_list():
    return render_template('ecommerce_product_list.html')
# [END ecommerce_product_list]


# [START ecommerce_product_grid]
@app.route('/ecommerce_product_grid.html')
@login_required
def ecommerce_product_grid():
    return render_template('ecommerce_product_grid.html')
# [END ecommerce_product_grid]


# [START email_template]
@app.route('/email_template.html')
@login_required
def email_template():
    return render_template('email_template.html')
# [END email_template]


# [START empty_page]
@app.route('/empty_page.html')
@login_required
def empty_page():
    return render_template('empty_page.html')
# [END empty_page]


# [START faq]
@app.route('/faq.html')
@login_required
def faq():
    return render_template('faq.html')
# [END faq]


# [START file_manager]
@app.route('/file_manager.html')
@login_required
def file_manager():
    return render_template('file_manager.html')
# [END file_manager]


# [START forgot_password]
@app.route('/forgot_password.html')
@app.route('/forgot')
def forgot_password():
    # redirect to the Netsuite OpenAir forgot password page
    return redirect('https://www.openair.com/index.pl?action=lost_info;')
    #return render_template('forgot_password.html')
# [END forgot_password]


# [START form_advanced]
@app.route('/form_advanced.html')
@login_required
def form_advanced():
    return render_template('form_advanced.html')
# [END form_advanced]


# [START form_basic]
@app.route('/form_basic.html')
@login_required
def form_basic():
    return render_template('form_basic.html')
# [END form_basic]


# [START form_editors]
@app.route('/form_editors.html')
@login_required
def form_editors():
    return render_template('form_editors.html')
# [END form_editors]


# [START form_file_upload]
@app.route('/form_file_upload.html')
@login_required
def form_file_upload():
    return render_template('form_file_upload.html')
# [END form_file_upload]


# [START form_markdown]
@app.route('/form_markdown.html')
@login_required
def form_markdown():
    return render_template('form_markdown.html')
# [END form_markdown]


# [START form_wizard]
@app.route('/form_wizard.html')
@login_required
def form_wizard():
    return render_template('form_wizard.html')
# [END form_wizard]


# [START forum_main]
@app.route('/forum_main.html')
@login_required
def forum_main():
    return render_template('forum_main.html')
# [END forum_main]


# [START forum_post]
@app.route('/forum_post.html')
@login_required
def forum_post():
    return render_template('forum_post.html')
# [END forum_post]


# [START full_height]
@app.route('/full_height.html')
@login_required
def full_height():
    return render_template('full_height.html')
# [END full_height]


# [START google_maps]
@app.route('/google_maps.html')
@login_required
def google_maps():
    return render_template('google_maps.html')
# [END google_maps]


# [START graph_chartist]
@app.route('/graph_chartist.html')
@login_required
def graph_chartist():
    return render_template('graph_chartist.html')
# [END graph_chartist]


# [START graph_chartjs]
@app.route('/graph_chartjs.html')
@login_required
def graph_chartjs():
    return render_template('graph_chartjs.html')
# [END graph_chartjs]


# [START graph_flot]
@app.route('/graph_flot.html')
@login_required
def graph_flot():
    return render_template('graph_flot.html')
# [END graph_flot]


# [START graph_morris]
@app.route('/graph_morris.html')
@login_required
def graph_morris():
    return render_template('graph_morris.html')
# [END graph_morris]


# [START graph_peity]
@app.route('/graph_peity.html')
@login_required
def graph_peity():
    return render_template('graph_peity.html')
# [END graph_peity]


# [START graph_rickshow]
@app.route('/graph_rickshow.html')
@login_required
def graph_rickshow():
    return render_template('graph_rickshow.html')
# [END graph_rickshow]


# [START graph_sparkline]
@app.route('/graph_sparkline.html')
@login_required
def graph_sparkline():
    return render_template('graph_sparkline.html')
# [END graph_sparkline]


# [START grid_options]
@app.route('/grid_options.html')
@login_required
def grid_options():
    return render_template('grid_options.html')
# [END grid_options]


# [START i18support]
@app.route('/i18support.html')
@login_required
def i18support():
    return render_template('i18support.html')
# [END i18support]


# [START icons]
@app.route('/icons.html')
@login_required
def icons():
    return render_template('icons.html')
# [END icons]


# [START idle_timer]
@app.route('/idle_timer.html')
@login_required
def idle_timer():
    return render_template('idle_timer.html')
# [END idle_timer]


# [START index]
@app.route('/', methods=['GET'])
@app.route('/index',methods=['GET','POST'])
@app.route('/index.html',methods=['GET','POST'])
@login_required
def index():

    #flash("all_bookings_json_obj: ***{}***".format(all_bookings_json_obj['response']['Read']['Booking']))
    #flash("all_users_json_obj:{} ".format(all_users_json_obj))
    # prepare projects dictionary
    '''dummy = prepare_dict(projects_json= all_projects_json_obj, users_json= all_users_json_obj, tasks_json= all_tasks_json_obj,
                 tickets_json= all_tickets_json_obj, bookings_json = all_bookings_json_obj)'''

    # create global variables


    '''flash("all_projects_json_obj: {}, all_users_json_obj: {}, all_tasks_info_obj: {}, all_timesheets_info_obj: {}, all_envelopes_info_obj: {}".format(all_projects_json_obj, all_users_json_obj, all_tasks_info_obj,
                                                                     all_timesheets_info_obj, all_envelopes_info_obj))
                                                                     '''

    return render_template(url_for('index'))
# [END index]


# [START invoice]
@app.route('/invoice.html')
@login_required
def invoice():
    return render_template('invoice.html')
# [END invoice]


# [START invoice_print]
@app.route('/invoice_print.html')
@login_required
def invoice_print():
    return render_template('invoice_print.html')
# [END invoice_print]


# [START issue_tracker]
@app.route('/issue_tracker.html')
@login_required
def issue_tracker():
    return render_template('issue_tracker.html')
# [END issue_tracker]


# [START jq_grid]
@app.route('/jq_grid.html')
@login_required
def jq_grid():
    return render_template('jq_grid.html')
# [END jq_grid]


# [START landing]
@app.route('/landing.html')
@login_required
def landing():
    return render_template('landing.html')
# [END landing]


# [START layouts]
@app.route('/layouts.html')
@login_required
def layouts():
    return render_template('layouts.html')
# [END layouts]


# [START loading_buttons]
@app.route('/loading_buttons.html')
@login_required
def loading_buttons():
    return render_template('loading_buttons.html')
# [END loading_buttons]


# [START lockscreen]
@app.route('/lockscreen.html')
@login_required
def lockscreen():
    return render_template('lockscreen.html')
# [END lockscreen]

'''
# [START login]
@app.route('/login.html', methods=['GET','POST'])
def login_html():
    return render_template('login.html',form=form)
# [END login]
'''

# [START login_two_columns]
@app.route('/login_two_columns.html', methods=['GET'])
def login_two_columns():
    return render_template('login_two_columns.html')
# [END login]


# [START mail_compose]
@app.route('/mail_compose.html')
@login_required
def mail_compose():
    return render_template('mail_compose.html')
# [END mail_compose]


# [START mail_detail]
@app.route('/mail_detail.html')
@login_required
def mail_detail():
    return render_template('mail_detail.html')
# [END mail_detail]


# [START mailbox]
@app.route('/mailbox.html')
@login_required
def mailbox():
    return render_template('mailbox.html')
# [END mailbox]


# [START masonry]
@app.route('/masonry.html')
@login_required
def masonry():
    return render_template('masonry.html')
# [END masonry]


# [START md-skin]
@app.route('/md-skin.html')
@login_required
def md_skin():
    return render_template('md-skin.html')
# [END md-skin]


# [START metrics]
@app.route('/metrics.html')
@login_required
def metrics():
    return render_template('metrics.html')
# [END metrics]


# [START modal_window]
@app.route('/modal_window.html')
@login_required
def modal_window():
    return render_template('modal_window.html')
# [END modal_window]


# [START nestable_list]
@app.route('/nestable_list.html')
@login_required
def nestable_list():
    return render_template('nestable_list.html')
# [END nestable_list]


# [START notifications]
@app.route('/notifications.html')
@login_required
def notifications():
    return render_template('notifications.html')
# [END notifications]


# [START off_canvas_menu]
@app.route('/off_canvas_menu.html')
@login_required
def off_canvas_menu():
    return render_template('off_canvas_menu.html')
# [END off_canvas_menu]


# [START package]
@app.route('/package.html')
@login_required
def package():
    return render_template('package.html')
# [END package]


# [START pin_board]
@app.route('/pin_board.html')
@login_required
def pin_board():
    return render_template('pin_board.html')
# [END pin_board]


# [START profile]
@app.route('/profile.html')
@login_required
def profile():
    return render_template('profile.html')
# [END profile]


# [START profile_2]
@app.route('/profile_2.html')
@login_required
def profile_2():
    return render_template('profile_2.html')
# [END profile_2]


# [START register]
@app.route('/register.html')
def register():
    return render_template('register.html')
# [END register]


# [START resizeable_panels]
@app.route('/resizeable_panels.html')
@login_required
def resizeable_panels():
    return render_template('resizeable_panels.html')
# [END resizeable_panels]


# [START search_results]
@app.route('/search_results.html')
@login_required
def search_results():
    return render_template('search_results.html')
# [END search_results]


# [START skin-config]
@app.route('/skin-config.html')
@login_required
def skin_config():
    return render_template('skin-config.html')
# [END skin-config]


# [START slick_carousel]
@app.route('/slick_carousel.html')
@login_required
def slick_carousel():
    return render_template('slick_carousel.html')
# [END slick_carousel]


# [START social_feed]
@app.route('/social_feed.html')
@login_required
def social_feed():
    return render_template('social_feed.html')
# [END social_feed]


# [START spinners]
@app.route('/spinners.html')
@login_required
def spinners():
    return render_template('spinners.html')
# [END spinners]


# [START sweetalert]
@app.route('/sweetalert.html')
@login_required
def sweetalert():
    return render_template('sweetalert.html')
# [END sweetalert]


# [START table_basic]
@app.route('/table_basic.html')
@login_required
def table_basic():
    return render_template('table_basic.html')
# [END table_basic]


# [START table_data_tables]
@app.route('/table_data_tables.html')
@login_required
def table_data_tables():
    return render_template('table_data_tables.html')
# [END table_data_tables]


# [START table_foo_table]
@app.route('/table_foo_table.html')
@login_required
def table_foo_table():
    return render_template('table_foo_table.html')
# [END table_foo_table]


# [START tabs]
@app.route('/tabs.html')
@login_required
def tabs():
    return render_template('tabs.html')
# [END tabs]


# [START tabs_panels]
@app.route('/tabs_panels.html')
@login_required
def tabs_panels():
    return render_template('tabs_panels.html')
# [END tabs_panels]


# [START teams_board]
@app.route('/teams_board.html')
@login_required
def teams_board():
    return render_template('teams_board.html')
# [END teams_board]


# [START timeline]
@app.route('/timeline.html')
@login_required
def timeline():
    return render_template('timeline.html')
# [END timeline]


# [START timeline_2]
@app.route('/timeline_2.html')
@login_required
def timeline_2():
    return render_template('timeline_2.html')
# [END timeline_2]


# [START tinycon]
@app.route('/tinycon.html')
@login_required
def tinycon():
    return render_template('tinycon.html')
# [END tinycon]


# [START toastr_notifications]
@app.route('/toastr_notifications.html')
@login_required
def toastr_notifications():
    return render_template('toastr_notifications.html')
# [END toastr_notifications]


# [START tour]
@app.route('/tour.html')
@login_required
def tour():
    return render_template('tour.html')
# [END tour]


# [START tree_view]
@app.route('/tree_view.html')
@login_required
def tree_view():
    return render_template('tree_view.html')
# [END tree_view]


# [START truncate]
@app.route('/truncate.html')
@login_required
def truncate():
    return render_template('truncate.html')
# [END truncate]


# [START typography]
@app.route('/typography.html')
@login_required
def typography():
    return render_template('typography.html')
# [END typography]


# [START validation]
@app.route('/validation.html')
@login_required
def validation():
    return render_template('validation.html')
# [END validation]


# [START video]
@app.route('/video.html')
@login_required
def video():
    return render_template('video.html')
# [END video]


# [START vote_list]
@app.route('/vote_list.html')
@login_required
def vote_list():
    return render_template('vote_list.html')
# [END vote_list]


# [START widgets]
@app.route('/widgets.html')
@login_required
def widgets():
    return render_template('widgets.html')
# [END widgets]

