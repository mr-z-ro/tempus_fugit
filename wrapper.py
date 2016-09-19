# utilities to interface with the OAXMLAPI Netsuite API wrapper
# import modules from Python wrapper around the NetSuite OpenAir XML API
import urllib2
from oaxmlapi import connections, datatypes, commands
import simplejson as json
from oaxmlapi import *


def call_wrapper(key, uname, pword, company=''):
    app = connections.Application('Tempus Fugit', '1.0', 'default', key)
    auth = connections.Auth(company, uname, pword)

    # Filter just this year
    date = datatypes.Datatype('Date', {'month': '01', 'day': '01', 'year': '2016'})
    filter1 = commands.Read.Filter('newer-than', 'date', date).getFilter()
    # Filter just FIBR tasks
    task = datatypes.Datatype('Task', {'projectid': '313'})  # Filter by FIBR
    filter2 = commands.Read.Filter(None, None, task).getFilter()

    # Prepare the request
    xml_data = []
    xml_data.append(
        commands.Read('Task', 'equal to', {'limit': '1000'}, [filter1, filter2], ['id', 'timesheetid']).read())
    xml_req = connections.Request(app, auth, xml_data).tostring()

    # Perform the request
    req = urllib2.Request(url='https://www.openair.com/api.pl', data=xml_req)
    res = urllib2.urlopen(req, timeout=60)
    xml_res = res.read()

    # might be easier working with json data
    json_string = utilities.xml2json(xml_res, strip=True)

    # create a json object
    json_obj = json.loads(json_string)
    # print "json_obj: {}".format(json_obj['response']['Auth']['@status'])

    return json_obj