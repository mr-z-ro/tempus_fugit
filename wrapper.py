# utilities to interface with the OAXMLAPI Netsuite API wrapper
# import modules from Python wrapper around the NetSuite OpenAir XML API
import urllib2
import httplib
from oaxmlapi import connections, datatypes, commands
import simplejson as json
from oaxmlapi import *


###########################################
# Begin Monkey-Patch for bad server implementation
# (see http://stackoverflow.com/questions/14149100/incompleteread-using-httplib)
###########################################
def patch_http_response_read(func):
    httplib.HTTPConnection._http_vsn = 10
    httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner
###########################################
# End Monkey-Patch for bad server implementation
###########################################


# Private method to make the final call including all the general parameters
# NOTE: This method should be called by all subsequent methods in this file
def _call_wrapper(key, un, pw, company, xml_data):
    # Monkey Patch
    httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)

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

    # Filter just this year
    date = datatypes.Datatype('Date', {'month': '01', 'day': '01', 'year': '2016'})
    filter1 = commands.Read.Filter('newer-than', 'Date', date).getFilter()

    # Filter just tasks for the project
    task = datatypes.Datatype('Task', {'projectid': projectid})  # 1544 prev, Filter by FIBR
    filter2 = commands.Read.Filter(None, None, task).getFilter()

    # Prepare the request
    xml_data = [commands.Read('Task',
                              'equal to',
                              {'limit': '10'},
                              [filter1, filter2],
                              ['id', 'name', 'updated', 'priority', 'percent_complete']
                              ).read()]

    return _call_wrapper(key, un, pw, company, xml_data)

