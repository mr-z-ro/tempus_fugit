# utilities to interface with the OAXMLAPI Netsuite API wrapper
# import modules from Python wrapper around the NetSuite OpenAir XML API
import urllib2

import simplejson as json

from app.oaxmlapi import connections, datatypes, commands, utilities


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


# Get auth info from server
def get_whoami(key, un, pw, company):

    auth = connections.Auth(company, un, pw)
    whoami_req = connections.Whoami(auth).whoami()

    # Prepare the request
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

    # Prepare the request
    xml_data = [commands.Read('Project', 'equal to', {'limit': '1000'}, [filter1], None).read()]

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
                               'calculated_starts', 'start_date', 'currency']
                              ).read()]

    return _call_wrapper(key, un, pw, company, xml_data)
