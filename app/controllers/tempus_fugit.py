import logging
import httplib2
import os
import json
import pdb

from datetime import timedelta

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import g
from flask import render_template
from flask import session
from werkzeug.contrib.cache import SimpleCache

from app.models.Daily import Daily
from app.models.Rate import Rate
from app.models.Booking import Booking
from app.models.Project import Project
from app.models.Task import Task
from app.models.Ticket import Ticket
from app.models.User import User
from login_form import LoginForm

from functools import wraps
from flask import request, session, redirect, url_for
from app.oaxmlapi.utils import date_percent_difference
from app.oaxmlapi.wrapper import get_whoami

from apiclient import discovery
from apiclient.discovery import build
from google.appengine.ext import webapp
from oauth2client.contrib.appengine import OAuth2Decorator
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OAuth2Credentials
from googleapiclient import discovery

import datetime

from time import gmtime, strftime


mod_tempus_fugit = Blueprint('mod_tempus_fugit', __name__)

# Set up cache
cache = SimpleCache()


def get_unexpired_dicts():
    users_dict = cache.get('users_dict')
    projects_dict = cache.get('projects_dict')
    bookings_dict = cache.get('bookings_dict')
    rates_dict = cache.get('rates_dict')

    if users_dict is None or projects_dict is None or bookings_dict is None or rates_dict is None:
        return None, None, None, None

    return users_dict, projects_dict, bookings_dict, rates_dict


@mod_tempus_fugit.before_request
def before_request():
    session.modified = True

    if request.endpoint not in ['mod_tempus_fugit.index', 'mod_tempus_fugit.login', 'mod_tempus_fugit.logout', 'mod_tempus_fugit.prepare_data']:
        g.users_dict, g.projects_dict, g.bookings_dict, g.rates_dict = get_unexpired_dicts()
        if g.users_dict is None or g.projects_dict is None or g.bookings_dict is None or g.rates_dict is None:
            return redirect(url_for('mod_tempus_fugit.index'))


# [START 404]
@mod_tempus_fugit.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
# [END 404]


# [START 500]
@mod_tempus_fugit.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
# [END 500]


def login_required(func):
    """Requires standard login credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # if 'logged_in' not in session or 'username' not in session or session['username']=='' and not user.is_authenticated() and request.endpoint !=url_for('login'):
        session.modified = True
        try:
            # to catch keyerrors

            if ('logged_in' not in session) or 'username' not in session or session['username'] is None or session['logged_in'] is None:
                # session is non-existent but we still do the same
                return redirect(url_for('mod_tempus_fugit.login', next=request.url))
        except Exception, err:
            return redirect(url_for('mod_tempus_fugit.login', next=request.url))
        return func(*args, **kwargs)
    return decorated_view


# [START index]
@mod_tempus_fugit.route('/', methods=['GET'])
@mod_tempus_fugit.route('/index',methods=['GET','POST'])
@mod_tempus_fugit.route('/index.html',methods=['GET','POST'])
@login_required
def index():
    g.users_dict, g.projects_dict, g.bookings_dict, g.rates_dict = get_unexpired_dicts()
    return render_template(url_for('mod_tempus_fugit.index'), users_dict=g.users_dict, projects_dict=g.projects_dict,
                               bookings_dict=g.bookings_dict, rates_dict=g.rates_dict)
# [END index]

@mod_tempus_fugit.route('/logout',methods=['GET'])
@login_required
def logout():
    """Logout the current user"""
    session['logged_in'] = False
    session['username']=''
    session['password'] = ''
    session['projects'] = ''
    session['logged_in']=''
    session.pop('username', None)
    session.pop('password', None)
    session.pop('logged_in',None)
    session.pop('projects', None)
    session.clear()

    #if all this does not clear the session
    # set a timeout for the session  to 1 seconds of inactivity /this  can change
    current_app.permanent_session_lifetime = timedelta(seconds=1)

    return redirect(url_for('mod_tempus_fugit.login'))


# [START login]
@mod_tempus_fugit.route('/login', methods=['GET', 'POST'])
@mod_tempus_fugit.route('/login.html', methods=['GET', 'POST'])
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
        my_company = current_app.config['COMPANY']
        netsuite_key = current_app.config['NETSUITE_API_KEY']  # Retrieve key from instance/config file
        json_obj = get_whoami(key=netsuite_key, un=username, pw=password, company=my_company)
        # flash("json_obj : {}".format(json_obj['response']['Read']['Project']))

        auth = False

        if 'response' in json_obj and 'Auth' in json_obj['response']:
            auth = True if (json_obj['response']['Auth']['@status'])=='0' else False
        else:
            flash('There seems to be a problem with the OpenAir or Netsuite Server:' + str(json_obj))
            return render_template('login.html', form=form)

        if auth:
            session['associate'] = '%s, %s' % (json_obj['response']['Whoami']['User']['addr']['Address']['last'], json_obj['response']['Whoami']['User']['addr']['Address']['first'])
            session['associate_title'] = '%s' % (json_obj['response']['Whoami']['User']['type'])
            session['associate_email'] = '%s' % (json_obj['response']['Whoami']['User']['addr']['Address']['email'])
            session['associate_id'] = '%s' % (json_obj['response']['Whoami']['User']['id'])
            session['logged_in'] = True

            # for session timeout to work we must set session permanent to True
            # session.permanent = True
            flash('Logged in successfully.')

            next = request.args.get('next')
            if next:
                session['currentpage'] = str(str(next).split('//')[-1:]).split('.')[:1]
            else:
                session['currentpage'] = 'projects'
            return redirect(next or url_for('mod_tempus_fugit.index'))

        flash('Sorry! Your password or username is invalid. Kindly try again.')
    return render_template('login.html', form=form)

# [END login submitted]

# create a route to be called by jQuery to process data
#
# At some point this needs to be refactored
#
# [START prepare_data]
@mod_tempus_fugit.route('/prepare_data')
@login_required
def prepare_data():

    users_dict, projects_dict, bookings_dict, rates_dict = get_unexpired_dicts()

    if users_dict is None or projects_dict is None or bookings_dict is None or rates_dict is None:
            # Re-initialize
            users_dict = {}
            projects_dict = {}
            bookings_dict = {}
            rates_dict = {}

            # project_dates will store dates related to projects, earliest used to estimate start date for projects with Null start date
            projects_dates = {}

            # get active projects
            projects_list = Project.get_my_projects(session['username']) # TODO: evaluate for sql injection via session
            projects_list = [project.to_dict() for project in projects_list]

            # make API call to retrieve users name and rate
            users_list = User.query.all()
            users_list = [user.to_dict() for user in users_list]

            # make API call to retrieve timesheet entries
            tasks_list = Task.get_my_tasks(session['username'])
            tasks_list = [task.to_dict() for task in tasks_list]

            # API call to retrieve Tickets info form Netsuite Openair
            tickets_list = Ticket.get_my_tickets(session['username'])
            tickets_list = [ticket.to_dict() for ticket in tickets_list]

            # Booking information is needed, pull only approved bookings
            bookings_list = Booking.get_my_bookings(session['username'])
            bookings_list = [booking.to_dict() for booking in bookings_list]

            # Rates list is needed
            rates_list = Rate.get_all_rates()
            rates_list = [rate.to_dict() for rate in rates_list]

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

            # loop through the rates json
            for rate in rates_list:
                if session['username'] not in rates_dict.keys():
                    rates_dict[session['username']] = {}

                rates_dict[session['username']][rate['user_id'], rate['project_id']] = {
                    'rate': rate['rate'],
                    'currency': rate['currency']
                }

            # loop through the users_json
            for a_user in users_list:

                # extract the user_id
                user_id = a_user['id']

                try:
                    # populate with a user_id
                    users_dict[users_name][user_id]['name'] = a_user['name']
                    users_dict[users_name][user_id]['nickname'] = a_user['nickname']
                    users_dict[users_name][user_id]['timezone'] = a_user['timezone']
                    users_dict[users_name][user_id]['line_manager_id'] = a_user['line_manager_id']
                    users_dict[users_name][user_id]['department_id'] = a_user['department_id']
                    users_dict[users_name][user_id]['active'] = a_user['active']
                    # print 'user_dict try'

                except KeyError, err:
                    users_dict[users_name][user_id] = {
                        'name': a_user['name'],
                        'nick_name': a_user['nickname'],
                        'time_zone': a_user['timezone'],
                        'line_manager_id': a_user['line_manager_id'],
                        'department_id': a_user['department_id'],
                        'active': a_user['active']
                    }
                    # flash("users_dict[users_name] keyerror: %s %s" % (err, user_id))
                    # non-existent user
                    # print 'user_dict exception part'
                except Exception, err:
                    flash('Detected error {} with users_json_obj'.format(err))

            # flash('users_dict[users_name]: %s' % users_dict[users_name])
            # loop through the projects_json
            for project in projects_list:
                pid = project['id']
                if (pid==425L):
                    pass
                calc_start_date = project['start_date']
                calc_end_date = project['finish_date']

                if calc_start_date is not None:
                    my_start_date = calc_start_date
                    if len(calc_start_date) > 10:
                        my_start_date = calc_start_date.split(' ')[0]
                    my_day, my_mnth, my_yr = my_start_date.split('/')
                    start_date_str = '{2}/{1:0>2}/{0:0>2}'.format(my_yr, my_mnth, my_day)
                else:
                    my_start_date = 'None'
                    start_date_str = 'None'

                if calc_end_date is not None:
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
                                                                                                         'budget_time'] is not None else 0.00
                    projects_dict[users_name][pid]['owner_id'] = project['owner_id']
                    projects_dict[users_name][pid]['currency'] = project['currency']
                    projects_dict[users_name][pid]['start_date'] = calc_start_date
                    projects_dict[users_name][pid]['finish_date'] = calc_end_date
                    projects_dict[users_name][pid]['project_stage_id'] = project['project_stage_id']
                    projects_dict[users_name][pid]['updated'] = project['updated']
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
                        'budget_time': float(project['budget_time']) if project['budget_time'] is not None else 0.00,
                        'owner_id': project['user_id'],
                        'currency': project['currency'],
                        'start_date': calc_start_date,
                        'finish_date': calc_end_date,
                        'project_stage_id': project['project_stage_id'],
                        'updated': project['updated'],
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

            for tasks in tasks_list:
                project_id = tasks['project_id']
                project_name = tasks['project_name']
                task_id = tasks['project_task_id']
                task_name = tasks['project_task_name']
                user_id = tasks['user_id']
                task_hours = float(tasks['hour']) if tasks['hour'] is not None else 0.00

                # extract the rate for the user
                try:
                    user_rate = float(rates_dict[session['username']][user_id, project_id]['rate']) if rates_dict[session['username']][user_id, project_id]['rate'] else 0.00
                except KeyError:
                    user_rate = 0.00

                # compute total hours worked per project
                fees_worked = task_hours / 8.00 * user_rate
                if project_id not in projects_dict[users_name].keys():
                    # track fees_worked, users and hours_worked in projects_dict
                    projects_dict[users_name][project_id] = {
                        'name': project_name,
                        'fees_worked': fees_worked,
                        'hours_worked': task_hours,
                        'users': {
                            user_id: {
                                task_id: {
                                    'name': task_name,
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
                    projects_dict[users_name][project_id]['tasks'][task_id] = {'name': task_name}

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
            for ticket in tickets_list:
                total = float(ticket['total']) if ticket['total'] is not None else 0.00
                project_id = ticket['project_id']
                project_name = ticket['project_name']
                user_id = ticket['user_id']

                if project_id not in projects_dict[users_name].keys():
                    # track fees_worked, users and hours_worked in projects_dict
                    projects_dict[users_name][project_id] = {
                        'name': project_name,
                        'fees_worked': 0.00,
                        'hours_worked': 0.00,
                        'users': {
                            user_id: {
                                'expenses': total
                            }
                        }
                    }
                else:
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
                                try:
                                    projects_dict[users_name][project_id]['users'].append({user_id:{'expenses': total}})
                                except KeyError:
                                    try:
                                        projects_dict[users_name][project_id] = {'name': project_name, 'users': [{user_id: {'expenses' : total}}]}
                                    except KeyError:
                                        flash(
                                            "Unexpected projects_dict[users_name][project_id]['users'][user_id] = {'expenses' : total} fail")

                    try:
                        projects_dict[users_name][project_id]['fees_worked'] += total
                    except KeyError:
                        projects_dict[users_name][project_id]['fees_worked'] = total

            for booking in bookings_list:
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
                project_id = booking['project_id']
                task_id = booking['project_task_id']
                user_id = booking['user_id']
                hours_booked = float(booking['hours']) if booking['hours'] is not None else 0.0
                hours_percent = float(booking['percentage']) if booking['percentage'] is not None else 0.0

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

            timeout = 60 * 60 * 4 # 4 hours
            cache.set('users_dict', users_dict, timeout=timeout)
            cache.set('projects_dict', projects_dict, timeout=timeout)
            cache.set('bookings_dict', bookings_dict, timeout=timeout)
            cache.set('rates_dict', rates_dict, timeout=timeout)

    return render_template(url_for('mod_tempus_fugit.index'),
                           users_dict=users_dict,
                           projects_dict=projects_dict,
                           bookings_dict=bookings_dict,
                           rates_dict=rates_dict)


# [START project_detail]
@mod_tempus_fugit.route('/projects/<project_id>', methods=['GET','POST'])
@login_required
def project_detail(project_id):

    if project_id and ("|" in project_id):

        # separate the project and task id for template processing
        project_id = project_id.strip()  # remove any trailing spaces
        pid, tid = project_id.split('|')
        pid = long(pid)
        tid = long(tid)

        return render_template('richtasks.html', project_id=pid, task_id=tid, users_dict=g.users_dict, projects_dict=g.projects_dict,
                               bookings_dict=g.bookings_dict, rates_dict=g.rates_dict)
    else:
        project_id = project_id.strip()  # remove any trailing spaces
        pid = long(project_id)

        return render_template('richproject.html', project_id=pid, users_dict=g.users_dict, projects_dict=g.projects_dict,
                               bookings_dict=g.bookings_dict, rates_dict=g.rates_dict)

    return redirect(url_for('mod_tempus_fugit.index'))
# [END project_detail]

#@mod_tempus_fugit.route('/projects/<project_id>/user_bookings/<user_id>', methods=['GET'])
@mod_tempus_fugit.route('/user_bookings', methods=['GET'])
@login_required
def user_bookings():
    if 'oauth_credentials' in session:
        url = '/oauth?code='
    else:
        url = get_google_oauth_url()

    return json.dumps({'oauth_url': url, 'spreadsheet_id': '1bnZvQ6QCMmuBc_QX4YmSi3askdty9oi_eZiZ6BCqbCM'})


@mod_tempus_fugit.route('/oauth', methods=['GET'])
@login_required
def oauth_callback():
    flash('Authorized: ' + request.args.get('code'))
    return render_template('bookingtest.html', oauth_key=request.args.get('code'))


@mod_tempus_fugit.route('/create_spreadsheet/<project_id>', methods=['GET'])
@login_required
def create_spreadsheet(project_id):

    if project_id and ("|" in project_id):

        # separate the project and task id for template processing
        project_id = project_id.strip()  # remove any trailing spaces
        pid, tid = project_id.split('|')
        pid = long(pid)
        tid = long(tid)
    else:
        pid = project_id

    # If we pass in OAuth stuff, then we need to do an exchange probably
    credentials = None
    if 'oauth_key' in request.args:
        key = request.args.get('oauth_key')
        flow = get_google_oauth_flow()
        if key is not None and len(key) > 0:
            credentials = flow.step2_exchange(key)

        # Save the credentials if we have nothing
        if credentials is not None:
            session['oauth_credentials'] = credentials.to_json()

    # If we have no credentials we try to pull from storage
    if credentials is None:
        credentials = get_google_oauth_credentials();

    # If there's nothing then we send it back to the auth cycle and bail
    # pdb.set_trace()

    if credentials is None:
        url = get_google_oauth_url()
        return json.dumps({'oauth_url': url, 'spreadsheet_id': '1bnZvQ6QCMmuBc_QX4YmSi3askdty9oi_eZiZ6BCqbCM'})

    service = discovery.build('sheets', 'v4', credentials=credentials)

    new_spreadsheet_id, new_spreadsheet_url = new_spreadsheet(service)
    original_spreadsheet_id = '1bnZvQ6QCMmuBc_QX4YmSi3askdty9oi_eZiZ6BCqbCM'
    logging.warning("New Spreadsheet URL: " + new_spreadsheet_url)

    sheet_id = 0

    sheet_id = copy_sheet(service, original_spreadsheet_id, new_spreadsheet_id, sheet_id)
    delete_sheet_and_rename(service, new_spreadsheet_id, sheet_id)
    users = users_for_project(pid)
    names = []
    rates = []
    for user in users:
        if user.name not in names:
            names.append(user.name)
            rate = Rate.get_rate(user.id, pid)
            if not rate:
                rates.append("")
            else:
                rates.append(str(rate.rate))


    replace_consultants(service, new_spreadsheet_id, names)
    replace_rates(service, new_spreadsheet_id, rates)

    return json.dumps({'spreadsheet_url': new_spreadsheet_url})


# [START navbar]
@mod_tempus_fugit.route('/navbar', methods=['GET','POST'])
@mod_tempus_fugit.route('/navbar.html')
@login_required
def navbar():
    return render_template('navbar.html')
# [END navbar]


# [START resources]
@mod_tempus_fugit.route('/update_booking/<project_name>/<task_name>/<user_name>', methods=['GET', 'POST'])
@login_required
def resources(project_name, task_name, user_name):
    dailies = Daily.get_dailies(project_name, task_name, user_name)

    return render_template('dailies.html', dailies=dailies, project_name=project_name, task_name=task_name, user_name=user_name)
# [END resources]


def get_google_oauth_flow():
    # Restrict access to users who've granted access to Calendar info.
    flow = flow_from_clientsecrets(current_app.config["CLIENT_SECRET_FILE"],
                                   scope='https://www.googleapis.com/auth/spreadsheets',
                                   redirect_uri='https://tempusfugit-bfa.pagekite.me/oauth')
    return flow


# Returns none if not valid
def get_google_oauth_credentials():
    credentials = OAuth2Credentials.from_json(session['oauth_credentials'])
    if credentials.token_expiry > datetime.datetime.now():
        return credentials

    return None


def get_google_oauth_url():
    flow = get_google_oauth_flow()
    url = flow.step1_get_authorize_url()
    return url


# User management

def users_for_project(project_id):
    users = []

    tasks = Task.tasks_for_project_id(project_id)
    for task in tasks:
        user = User.get(task.user_id)
        users.append(user)

    return users



# Tempus Fugit specific functions
def new_spreadsheet(service):
    spreadsheet_body = {
        # TODO: Add desired entries to the request body.
    }

    google_request = service.spreadsheets().create(body=spreadsheet_body)
    response = google_request.execute()

    # Here we get the new id from the response
    return response.get('spreadsheetId'), response.get('spreadsheetUrl')


def copy_sheet(service, original_spreadsheet_id, new_spreadsheet_id, sheet_id):
    copy_sheet_to_another_spreadsheet_request_body = {
        # The ID of the spreadsheet to copy the sheet to.
        'destination_spreadsheet_id': new_spreadsheet_id,  # TODO: Update placeholder value.

        # TODO: Add desired entries to the request body.
    }
    google_request = service.spreadsheets().sheets().copyTo(spreadsheetId=original_spreadsheet_id, sheetId=sheet_id,
                                                     body=copy_sheet_to_another_spreadsheet_request_body)
    response = google_request.execute()
    return response.get('sheetId')


def delete_sheet_and_rename(service, spreadsheet_id, sheet_id):
    # This will delete the original sheet, name everything correctly and in general do cleanup.
    batch_update_spreadsheet_request_body = {
        # A list of updates to apply to the spreadsheet.
        # Requests will be applied in the order they are specified.
        # If any request is not valid, no requests will be applied.
        'requests': [{'deleteSheet': {'sheetId': 0}},
                     {'updateSheetProperties':
                          {'properties':
                               {'sheetId': sheet_id, 'title': 'Project Bookings'},
                           'fields':
                               'title'
                           }
                      }
                     ]
    }

    google_request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                 body=batch_update_spreadsheet_request_body)

    google_request.execute()



def get_consultant_names(service, spreadsheet_id):
    results = read_spreadsheet(service, spreadsheet_id, 'A7:A5000')
    names = results.get('values')
    return names


def add_consultant(service, spreadsheet_id, name):
    names = get_consultant_names(service, spreadsheet_id)
    next_cell = "A" + str(len(names) + 7)
    write_spreadsheet_row(service, spreadsheet_id, next_cell, [name])


def add_consultants(service, spreadsheet_id, names):
    current_names = get_consultant_names(service, spreadsheet_id)
    next_cell = "A" + str(len(current_names) + 7)
    final_cell = "A" + str(len(current_names) + 7 + len(names))
    write_spreadsheet_column(service, spreadsheet_id, next_cell + ":" + final_cell, names)


def replace_consultants(service, spreadsheet_id, names):
    next_cell = "A7"
    final_cell = "A" + str(7 + len(names))
    write_spreadsheet_column(service, spreadsheet_id, next_cell + ":" + final_cell, names)

def replace_rates(service, spreadsheet_id, rates):
    next_cell = "B7"
    final_cell = "B" + str(7 + len(rates))
    write_spreadsheet_column(service, spreadsheet_id, next_cell + ":" + final_cell, rates)


# Helper functions
def read_spreadsheet(service, spreadsheet_id, range):
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range).execute()

    return result


def write_spreadsheet_row(service, spreadsheet_id, spreadsheet_range, values):
    write_spreadsheet_range(service, spreadsheet_id, spreadsheet_range, 'ROWS', values)


def write_spreadsheet_column(service, spreadsheet_id, spreadsheet_range, values):
    write_spreadsheet_range(service, spreadsheet_id, spreadsheet_range, 'COLUMNS', values)


def write_spreadsheet_range(service, spreadsheet_id, spreadsheet_range, dimension, values):
    if dimension != 'ROWS' and dimension != 'COLUMNS':
        raise Exception

    sheet_range = spreadsheet_range

    write_spreadsheet_request_body = {
        "range": sheet_range,
        "majorDimension": dimension,
        "values": [values]
    }

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=spreadsheet_range,
        valueInputOption='RAW', body=write_spreadsheet_request_body).execute()


