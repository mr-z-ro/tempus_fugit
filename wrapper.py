# utilities to interface with the OAXMLAPI Netsuite API wrapper
# import modules from Python wrapper around the NetSuite OpenAir XML API
import urllib2
from oaxmlapi import connections, datatypes, commands
import simplejson as json
from oaxmlapi import *


# Private method to make the final call including all the general parameters
# NOTE: This method should be called by all subsequent methods in this file
def _call_wrapper(key, un, pw, company, xml_data):

    # Prepare the request
    app = connections.Application('Tempus Fugit', '1.0', 'default', key)
    auth = connections.Auth(company, un, pw)
    xml_req = connections.Request(app, auth, xml_data).tostring()
    req = urllib2.Request(url='https://www.openair.com/api.pl', data=xml_req)
    # print 'Request url=%s' % req.get_full_url()
    # print 'Request req=%s' % xml_req
    # print 'Request data=%s' % xml_data

    # Perform the request
    res = urllib2.urlopen(req, timeout=60)
    xml_res = res.read()
    # print 'Response %s' % xml_res

    # might be easier working with json data
    json_string = utilities.xml2json(xml_res, strip=True)

    # create a json object
    json_obj = json.loads(json_string)
    # print "json_obj: {}".format(json_obj['response']['Auth']['@status'])
    return json_obj


# Get auth info from server, of currently authorized user
def get_whoami(key, un, pw, company):

    auth = connections.Auth(company, un, pw)
    whoami_req = connections.Whoami(auth).whoami()

    # Prepare the request
    xml_data = [whoami_req]

    return _call_wrapper(key, un, pw, company, xml_data)

# get user information based on user id only
def get_user_info(key, un, pw, company, userid):

        auth = connections.Auth(company, un, pw)
        user = datatypes.Datatype('User', {'id': userid})

        # Prepare the request
        whoami_req = connections.Whoami(user).whoami()
        xml_data = [whoami_req]

        return _call_wrapper(key, un, pw, company, xml_data)

# Get the time from the server
def get_time(key, un, pw, company):

    time_req = commands.Time().time()

    # Prepare the request
    xml_data = [time_req]

    return _call_wrapper(key, un, pw, company, xml_data)


# Get a list of projects from the server
def get_projects(key, un, pw, company='', userid = ''):

    project = datatypes.Datatype('Project', {'active': '1'})
    filter1 = commands.Read.Filter(None, None, project).getFilter()

    # limit the field names returned to absolute necessary fields to prevent long waits after login
    field_names = ['id', 'name', 'active', 'budget', 'budget_time', 'customer_name', 'userid', 'currency', 'start_date',
                   'finish_date', 'project_stageid','pm_approver_1', 'pm_approver_2', 'pm_approver_3', 'updated', 'picklist_label']  # to limit

    # Prepare the request
    xml_data = [commands.Read('Project', 'equal to', {'limit': '1000'}, [filter1], field_names).read()]

    return _call_wrapper(key, un, pw, company, xml_data)


# Get a list of tasks by project id from the server
def get_tasks(key, un, pw, company='', projectid = ''):

    # if filter(s) provided create an array of filters
    filters = []
    if projectid:
        # Filter just tasks for the project that aren't closed
        task = datatypes.Datatype('Projecttask', {'projectid': projectid, 'closed': '0'})
        filter1 = commands.Read.Filter(None, None, task).getFilter()
        filters.append(filter1)

    # Prepare the request
    xml_data = [commands.Read('Projecttask',
                              'equal to',
                              {'limit': '500'},
                              filters,
                              ['id', 'parent_id', 'ancestry', 'cost_center_id', 'projecttask_type_id', 'name',
                               'projectid', 'planned_hours', 'estimated_hours', 'completed_days', 'priority',
                               'percent_complete', 'task_budget_cost', 'customer_name', 'calculated_finishes',
                               'calculated_starts', 'start_date', 'currency', 'assign_user_names', 'project_name']
                              ).read()]

    return _call_wrapper(key, un, pw, company, xml_data)

# Get user Ids of users assigned to a project
def get_userids(key, un, pw, company, projectid =''):
    # filter by projectid
    print 'projectid = {}'.format(projectid)
    project = datatypes.Datatype('Task', {'project_id' : projectid})
    filter1 = commands.Read.Filter(None, None, project).getFilter()

    # prepare the request
    xml_data = [commands.Read('Task', 'equal to', {'limit' : '500'}, [filter1], None ).read()]

    # call wrapper
    return _call_wrapper(key, un, pw, company, xml_data)

# Get user Ids of users assigned to a project
def get_task_info(key, un, pw, company, projectid =''):
    # filter by projectid
    #print 'projectid = {}'.format(projectid)
    project = datatypes.Datatype('Task', {'projectid' : projectid})
    filter1 = commands.Read.Filter(None, None, project).getFilter()

    # prepare the request
    xml_data = [commands.Read('Task', 'equal to', {'limit' : '500'}, [filter1], ['projectid', 'projecttaskid',
                'decimal_hours', 'userid', 'loaded_cost', 'date', 'updated', 'timetypeid', 'projecttask_typeid',
                'project_loaded_cost', 'hours', 'timesheetid', 'cost_centerid'] ).read()]

    # call wrapper
    return _call_wrapper(key, un, pw, company, xml_data)

# get the user's rate
def get_user_rate(key, un, pw, company, projectid =''):
    print "project_id: {}".format(projectid)
    # filter by projectid
    #print 'projectid = {}'.format(projectid)
    uprate = datatypes.Datatype('Uprate', {'projectid' : '{}'.format(projectid)})
    #user = datatypes.Datatype('Uprate', {'userid': userid})

    filter1 = commands.Read.Filter(None, None, uprate).getFilter()
    #filter2 = commands.Read.Filter(None, None, user).getFilter()

    # prepare the request
    xml_data = [commands.Read('Uprate', 'equal to', {'limit' : '500'}, [filter1], ['projectid', 'id', 'userid', 'rate'] ).read()]

    # call wrapper
    return _call_wrapper(key, un, pw, company, xml_data)

def get_user_details(key, un, pw, company, projectid = ''):
    # filter by userida
    user = datatypes.Datatype('User', {'active': '1'})
    #nickname = datatypes.Datatype('User', {'nickname': 'bgathecha@bankablefrontier.com'})
    filter1 = commands.Read.Filter(None, None, user).getFilter()
    #filter2 = commands.Read.Filter(None, None, nickname).getFilter()

    # prepare the request
    xml_data = [commands.Read('User', 'equal to', {'limit': 1000}, [filter1], None).read()]

    # call the wrapper
    return _call_wrapper(key, un, pw, company, xml_data)

