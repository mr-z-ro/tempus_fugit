# utilities to interface with the OAXMLAPI Netsuite API wrapper
# import modules from Python wrapper around the NetSuite OpenAir XML API
from __future__ import absolute_import
import urllib2
import simplejson as json


from xml.dom import minidom
from oaxmlapi import utilities

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def make_api_call(xml_req):

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


def construct_element(input_elem, output_elem):
    # takes in an input_elem and creates an output_elem
    # check var_xml for attributes
    if len(input_elem.attrib) > 0:
        # iterate over attrib dictionary assigning openair_elem the attributes
        for k, v in input_elem.attrib.iteritems():
            output_elem.set(k, v)

    # check for existence of text or tail in the var_xml element
    if input_elem.text != None:
        output_elem.text = input_elem.text

    # check for existence of a tail in the var_xml element
    if input_elem.tail != None:
        output_elem.tail = input_elem.tail

    # check for children in the input_elem
    if len(input_elem.getchildren()) > 0:
        # loop through the children

        for node in input_elem:
            # create a subelement to the output_elem
            elem = ET.SubElement(output_elem, node.tag)

            # make a recursive call with elem as the input
            elem = construct_element(node, elem)

    return output_elem


def raw_call_wrapper(client ='Tempus Fugit', client_ver = '1.0', namespace = 'default', key ='', my_company = 'BFA', username = '', passwd = '', xml_str = ''):
    """ Function to construct XML for Netsuite API calls, this function allows programmer to directly create XML

    :param client: name of the app register with NS API key
    :param client_ver: versioning information for the app
    :param namespace: provided by Netsuite default is "default"
    :param key: key as provided by Netsuite OpenAir
    :param my_company: company name registered to the API
    :param username: email of user accessing NetSuite OpenAir
    :param passwd: password linked to the user credentials
    :param var_xml: XML to query, modify NetSuite OpenAir information
    :return: XML request ready for API call
    """
    header = '<?xml version="1.0" encoding="utf-8" standalone="yes"?>'
    request = ET.Element('request')
    request.attrib = {
        'API_ver': '1.0',
        'client': '%s' % client,
        'client_ver': "%s" % client_ver,
        'namespace': "%s" % namespace,
        'key': "%s" % key
    }

    # add SubElements
    auth = ET.SubElement(request, 'Auth')

    login = ET.SubElement(auth, 'Login')

    company = ET.SubElement(login, 'company')
    company.text = '%s' % my_company
    user = ET.SubElement(login, 'user')
    user.text = '%s' % username
    password = ET.SubElement(login, 'password')
    password.text = '%s' % passwd

    # convert xml_str to an xml Element
    var_xml = ET.XML(xml_str)

    # add subelement to request element
    openair_elem = ET.SubElement(request, var_xml.tag)

    # call the recursive function here
    openair_elem = construct_element(var_xml, openair_elem)

    xml_req = header + ET.tostring(request)

    return make_api_call(xml_req)

