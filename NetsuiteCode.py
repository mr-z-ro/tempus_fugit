import urllib2
from oaxmlapi import connections, datatypes, commands 
# import modules from Python wrapper around the NetSuite OpenAir XML API
# [END imports]

# [START wrapper]

def call_wrapper(key,company='BFA',uname,pword):
	app = connections.Application('Tempus Fugit','1.0','default',key)
	auth = connections.Auth(company, uname, pword)
	
	# Filter just this year
	date = datatypes.Datatype('Date', {'month': '01', 'day': '01', 'year': '2016'})
	filter1 = commands.Read.Filter('newer-than', 'date', date).getFilter()
	# Filter just FIBR tasks
	task = datatypes.Datatype('Task', {'projectid': '313'}) # Filter by FIBR
	filter2 = commands.Read.Filter(None, None, task).getFilter()

	# Prepare the request
	xml_data = []
	xml_data.append(commands.Read('Task', 'equal to', {'limit': '1000'}, [filter1, filter2], ['id', 'timesheetid']).read())
	xml_req = connections.Request(app, auth, xml_data).tostring()

	# Perform the request
	req = urllib2.Request(url='https://www.openair.com/api.pl', data=xml_req)
	res = urllib2.urlopen(req)
	xml_res = res.read()
	print "response: %s" % xml_res​
	return xml_res