from config import *
from oaxmlapi import connections, datatypes, commands
from oaxmlapi import *
import urllib2
import sys
import ConfigParser
import io
import simplejson as json
import xml2json

# Load the configuration file
with open('instance/config.ini') as f:
    sample_config = f.read()

config = ConfigParser.RawConfigParser(allow_no_value=True)
config.readfp(io.BytesIO(sample_config))

# list all contents
print 'List all contents'
for section in config.sections():
    print 'Section {}'.format(section)
    for options in config.options(section):
        pass#print 'X {}::{}::{}'.format(options,config.get(section,options),str(type(options)))


NETSUITE_API_KEY = config.get('netsuite','NETSUITE_API_KEY').strip()
COMPANY = config.get('netsuite','COMPANY').strip()
USER_NAME = config.get('netsuite','USER_NAME').strip()
PASSWORD = config.get('netsuite','PASSWORD').strip()
"""
print 'API Key {} Company {} User {} Pass {}'.format(NETSUITE_API_KEY, COMPANY, USER_NAME, PASSWORD)
app = connections.Application('Tempus Fugit', '1.0', 'default', NETSUITE_API_KEY)
auth = connections.Auth(COMPANY, USER_NAME, PASSWORD)

date = datatypes.Datatype('Date',{'month' : '10', 'day' : '01', 'year' : '2016'})
task = datatypes.Datatype('Task',{'projectid' : '1544'})

filter1 = commands.Read.Filter('newer-than', 'date', date).getFilter()
filter2 = commands.Read.Filter(None, None, task).getFilter()

xml_data = []
xml_data.append(commands.Read('Task', 'equal to', {'limit': '1000'}, [filter1, filter2], ['id', 'timesheetid']).read())

xml_req = connections.Request(app, auth, xml_data).tostring()

# Perform the request
req = urllib2.Request(url='https://www.openair.com/api.pl', data=xml_req)
res = urllib2.urlopen(req, timeout=60)
xml_res = res.read()
print 'xml_res {}'.format(xml_res)
# might be easier working with json data
json_string = xml2json.xml2json(xml_res)
print 'json_string: {}'.format(json_string)
# create a json object
json_obj = json.loads(json_string)
# print "json_obj: {}".format(json_obj['response']['Auth']['@status'])
print 'xml_data: {}'.format(xml_data)
"""

app = connections.Application('Tempus Fugit', '1.0', 'default', NETSUITE_API_KEY)
auth = connections.Auth(COMPANY, USER_NAME, PASSWORD)
#def getTasks(NETSUITE_API_KEY, USER_NAME, PASSWORD, company= COMPANY, projectid = '29'):

# Filter just this year
date = datatypes.Datatype('Date', {'month': '01', 'day': '01', 'year': '2016'})
filter1 = commands.Read.Filter('newer-than', 'Date', date).getFilter()
# Filter just FIBR tasks
task = datatypes.Datatype('Task', {'projectid': '313'})  # 1544 prev, Filter by FIBR
# modified task with uprate
# uprate = datatypes.Datatype('Uprate',{'userid':uname})
project = datatypes.Datatype('Project', {'projectid': '16632'})  # Filter by Projects, Tempus Fugit
# filter2 = commands.Read.Filter(None, None, task).getFilter()

# modified filter 2 to use uprate
# filter2 = commands.Read.Filter(None, None, uprate).getFilter()
# filter2 = commands.Read.Filter(None, None, task).getFilter()
filter2 = commands.Read.Filter(None, None, project).getFilter()

# Prepare the request
xml_data = []
"""
xml_data.append(
    commands.Read('Task', 'equal to', {'limit': '1000'}, [filter1, filter2], ['id', 'timesheetid']).read())

xml_data.append(
    commands.Read('Project', 'equal to', {'limit': '1000'}, [filter1, filter2], ['id', 'timesheetid']).read())
"""

# modified read to return uprate
xml_data.append(
    commands.Read('Project', 'equal to', {'limit': '500'}, [filter2],
                  ['projectid', 'userid', 'name', 'updated', 'planned_hours']).read())
xml_req = connections.Request(app, auth, xml_data).tostring()

# Perform the request
req = urllib2.Request(url='https://www.openair.com/api.pl', data=xml_req)
res = urllib2.urlopen(req, timeout=60)
xml_res = res.read()
# print 'Response %s' % xml_res

# might be easier working with json data
json_string = utilities.xml2json(xml_res, strip=True)

# create a json object
json_obj = json.loads(json_string)

print "json_obj: {}".format(json_obj)

def call_wrapper(key, uname, pword, company=''):
    app = connections.Application('Tempus Fugit', '1.0', 'default', key)
    auth = connections.Auth(company, uname, pword)

    # Filter just this year
    date = datatypes.Datatype('Date', {'month': '01', 'day': '01', 'year': '2016'})
    filter1 = commands.Read.Filter('newer-than', 'Date', date).getFilter()
    # Filter just FIBR tasks
    task = datatypes.Datatype('Task', {'projectid': '313'})  # 1544 prev, Filter by FIBR
    # modified task with uprate
    #uprate = datatypes.Datatype('Uprate',{'userid':uname})
    project = datatypes.Datatype('Project',{'projectid':'16632'}) # Filter by Projects, Tempus Fugit
    #filter2 = commands.Read.Filter(None, None, task).getFilter()

    # modified filter 2 to use uprate
    #filter2 = commands.Read.Filter(None, None, uprate).getFilter()
    #filter2 = commands.Read.Filter(None, None, task).getFilter()
    filter2 = commands.Read.Filter(None, None, project).getFilter()

    # Prepare the request
    xml_data = []
    """
    xml_data.append(
        commands.Read('Task', 'equal to', {'limit': '1000'}, [filter1, filter2], ['id', 'timesheetid']).read())

    xml_data.append(
        commands.Read('Project', 'equal to', {'limit': '1000'}, [filter1, filter2], ['id', 'timesheetid']).read())
    """

    #modified read to return uprate
    xml_data.append(
        commands.Read('Project', 'equal to', {'limit': '500'}, [filter2], ['projectid', 'userid', 'name','updated','planned_hours']).read())
    xml_req = connections.Request(app, auth, xml_data).tostring()

    # Perform the request
    req = urllib2.Request(url='https://www.openair.com/api.pl', data=xml_req)
    res = urllib2.urlopen(req, timeout=60)
    xml_res = res.read()
    #print 'Response %s' % xml_res

    # might be easier working with json data
    json_string = utilities.xml2json(xml_res, strip=True)

    # create a json object
    json_obj = json.loads(json_string)
    # print "json_obj: {}".format(json_obj['response']['Auth']['@status'])

    return json_obj