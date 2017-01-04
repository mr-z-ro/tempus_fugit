import json
from datetime import timedelta
from os import urandom

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import render_template

from app.models.Booking import Booking
from app.models.Project import Project
from app.models.Task import Task
from app.models.TempusFugitUser import TempusFugitUser
from app.models.Ticket import Ticket
from app.models.User import User
from login_form import LoginForm

from functools import wraps
from flask import request, session, redirect, url_for
from app.oaxmlapi.utils import date_percent_difference
from app.oaxmlapi.wrapper import get_whoami

mod_tempus_fugit = Blueprint('mod_tempus_fugit', __name__)

## create a dictionary to hold projects, users and bookings info, create dummy user
projects_dict = {}
users_dict = {}
bookings_dict = {}
tempus_fugit_user = TempusFugitUser(
            username=None,
            password=None,
            company=None
        )

@mod_tempus_fugit.before_request
def before_request():
    session.modified = True


@mod_tempus_fugit.context_processor
def inject_template_dict():
    return dict(users_dict = users_dict, projects_dict = projects_dict, bookings_dict = bookings_dict)


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

            if ('logged_in' not in session) and ('username' not in session) and (session['username']=='' or session['username']== None) and (not tempus_fugit_user.is_authenticated()) and (request.endpoint !=url_for('mod_tempus_fugit.login')):
                # session is non-existent but we still do the same
                return redirect(url_for('mod_tempus_fugit.login',next=request.url))
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
    return render_template(url_for('mod_tempus_fugit.index'))
# [END index]

@mod_tempus_fugit.route('/logout',methods=['GET'])
@login_required
def logout():
    """Logout the current user"""
    #user = current_user;
    tempus_fugit_user.authenticated = False
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
    current_app.permanent_session_lifetime = timedelta(seconds=1)

    if 'username' not in session  or 'logged_in' not in session or session['username']=='' or session['logged_in']=='' and not tempus_fugit_user.is_authenticated():
        return redirect(url_for('mod_tempus_fugit.login'))

    return render_template(url_for('mod_tempus_fugit.login'))


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
        auth = True if (json_obj['response']['Auth']['@status'])=='0' else False
        # set authentication on the user instance
        tempus_fugit_user.set_authentication(auth)
        if tempus_fugit_user.is_authenticated():

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

        flash('Sorry! Your password or username is invalid. Kindly try again..')
    return render_template('login.html', form=form)

# [END login submitted]

# create a route to be called by jQuery to process data
# [START prepare_data]
@mod_tempus_fugit.route('/prepare_data')
@login_required
def prepare_data():
    # project_dates will store dates related to projects, earliest used to estimate start date for projects with Null start date
    all_projects_dict = {}
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
    for a_user in users_list:

        # extract the user_id
        user_id = a_user['id']

        try:
            # populate with a user_id
            users_dict[users_name][user_id]['name'] = a_user['name']
            users_dict[users_name][user_id]['nickname'] = a_user['nickname']
            users_dict[users_name][user_id]['timezone'] = a_user['timezone']
            users_dict[users_name][user_id]['rate'] = float(a_user['rate']) if a_user['rate'] != None else 0.00
            users_dict[users_name][user_id]['line_manager_id'] = a_user['line_manager_id']
            users_dict[users_name][user_id]['currency'] = a_user['currency']
            users_dict[users_name][user_id]['department_id'] = a_user['department_id']
            users_dict[users_name][user_id]['active'] = a_user['active']
            # print 'user_dict try'

        except KeyError, err:
            users_dict[users_name][user_id] = {
                'name': a_user['name'],
                'nick_name': a_user['nickname'],
                'time_zone': a_user['timezone'],
                'rate': float(a_user['rate']) if a_user['rate'] != None else 0.00,
                'line_manager_id': a_user['line_manager_id'],
                'currency': a_user['currency'],
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
        calc_start_date = project['start_date']
        calc_end_date = project['finish_date']

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
                'budget_time': float(project['budget_time']) if project['budget_time'] != None else 0.00,
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
        task_hours = float(tasks['hour']) if tasks['hour'] != None else 0.00

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
    current_app.add_template_global(users_dict, 'users_dict')
    current_app.add_template_global(projects_dict, 'projects_dict')
    current_app.add_template_global(bookings_dict, 'bookings_dict')
    return render_template(url_for('mod_tempus_fugit.index'), users_dict=users_dict)

# [START projects]
@mod_tempus_fugit.route('/projects')
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
@mod_tempus_fugit.route('/projects/<project_id>', methods=['GET','POST'])
@login_required
def project_detail(project_id):
    if project_id and ("|" in project_id):

        # separate the project and task id for template processing
        project_id = project_id.strip()  # remove any trailing spaces
        pid, tid = project_id.split('|')
        pid = long(pid)
        tid = long(tid)

        # refresh task list?
        # json_obj = get_tasks(netsuite_key,
        #                     session['username'],
        #                     session['password'],
        #                     company=my_company,
        #                     projectid=pid)

        return render_template('richtasks.html', project_id=pid, taskid=tid)
    else:
        project_id = project_id.strip()  # remove any trailing spaces
        pid = long(project_id)

        return render_template('richproject.html', project_id=pid)

    return redirect(url_for('mod_tempus_fugit.projects'))
# [END project_detail]

# [START navbar]
@mod_tempus_fugit.route('/navbar', methods=['GET','POST'])
@mod_tempus_fugit.route('/navbar.html')
@login_required
def navbar():
    return render_template('navbar.html')
# [END navbar]

# [START resources]
@mod_tempus_fugit.route('/resources/<user_id>', methods= ['GET', 'POST'])
@login_required
def resources(user_id):
    return render_template('profile.html', user_id = user_id)
# [END resources]