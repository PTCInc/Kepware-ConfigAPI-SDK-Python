# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


r""":mod:`connection` exposes an API that manages the RESTful requests 
for the Kepware Configuration API. 
"""

import json
import codecs
import datetime
from urllib import request, parse, error
from base64 import b64encode
# import socket


class server:
    '''A class to represent a connection to an instance of Kepware. This object is used to 
    create the Authentication and server parameters to taget a Kepware instance. An instance of this is 
    used in all configuration calls done.

    Properties:

    "host" - host name or IP address
    "port" - port of Configuration API
    "username" - username to conduct "Basic Authentication"
    "password" - password to conduct "Basic Authentication"
    "url" (STATIC) - base URL for the server connection

    Methods:

    "reinitialize()" - Reinitialize the Kepware server
    "get_trans_log()" - retrieve the Configuration API transaction logs
    "get_event_log()" - retrieve the Kepware Event Log
    '''
    __root_url = '/config'
    __version_url = '/v1'
    __project_services_url = '/project/services'
    __event_log_url = '/event_log'
    __trans_log_url = '/log'



    def __init__(self,  host = None, port = None, user = None, pw = None):
        self.host = host
        self.port = port
        self.username = user
        self.password = pw
    
    @property
    def url(self):
        return  'http://{}:{}{}{}'.format(self.host, self.port, self.__root_url, self.__version_url)


    def reinitialize(self):
        '''Executes a Reinitialize call to the Kepware instance.
        '''
        url = self.url + self.__project_services_url + '/ReinitializeRuntime'
        return self._config_update(url, None)

    def get_trans_log(self, start = None, end = None, limit = None):
        ''' Get the Transaction Log from the Kepware instance.

        "start" (optional) - datetime.datetime type and should be UTC

        "end" (optional) - datetime.datetime type and should be UTC

        "limit" (optional) -  number of event log entries to request
        '''
        query = self.__create_query(start, end, limit)
        url = self.url + self.__trans_log_url + '?' + parse.urlencode(query)
        return self._config_get(url)

    def get_event_log(self, limit = None, start = None, end = None):
        ''' Get the Event Log from the Kepware instance.

        "start" (optional) - datetime.datetime type and should be UTC

        "end" (optional) - datetime.datetime type and should be UTC

        "limit" (optional) - number of event log entries to request
        '''
        query = self.__create_query(start, end, limit)
        url = self.url + self.__event_log_url + '?' + parse.urlencode(query)
        return self._config_get(url)

    #Function used to Add an object to Kepware (HTTP POST)
    def _config_add(self, url, DATA):
        '''Conducts an POST method at *url* to add an object in the Kepware Configuration
        *DATA* is required to be a properly JSON object (dict) of the item to be posted to *url* 
        '''
        data = json.dumps(DATA).encode('utf-8')
        url_obj = self.__url_validate(url)
        q = request.Request(url_obj, data, method='POST')
        q.add_header("Authorization", "Basic %s" % self.__build_auth_str(self.username, self.password))
        q.add_header("Content-Type", "application/json")
        return self.__connect(q)

    #Function used to del an object to Kepware (HTTP DELETE)
    def _config_del(self, url):
        '''Conducts an DELETE method at *url* to delete an object in the Kepware Configuration'''
        url_obj = self.__url_validate(url)
        q = request.Request(url_obj, method='DELETE')
        q.add_header("Authorization", "Basic %s" % self.__build_auth_str(self.username, self.password))
        q.add_header("Content-Type", "application/json")
        return self.__connect(q)

    #Function used to Update an object to Kepware (HTTP PUT)
    def _config_update(self, url, DATA = None):
        '''Conducts an PUT method at *url* to modify an object in the Kepware Configuration.
        *DATA* is required to be a properly JSON object (dict) of the item to be put to *url*
        '''
        url_obj = self.__url_validate(url)
        if DATA == None:            
            q = request.Request(url_obj, method='PUT')
        else:
            data = json.dumps(DATA).encode('utf-8')
            q = request.Request(url_obj, data, method='PUT')
        q.add_header("Authorization", "Basic %s" % self.__build_auth_str(self.username, self.password))
        q.add_header("Content-Type", "application/json")
        return self.__connect(q)

    #Function used to Read an object from Kepware (HTTP GET) and return the JSON response
    def _config_get(self, url):
        '''Conducts an GET method at *url* to retrieve an objects properties in the Kepware Configuration.'''
        url_obj = self.__url_validate(url)
        q = request.Request(url_obj, method='GET')
        q.add_header("Authorization", "Basic %s" % self.__build_auth_str(self.username, self.password))
        q.add_header("Content-Type", "application/json")
        return self.__connect(q)
    
    def _force_update_check(self, force, DATA):
        if force == True:
            DATA['FORCE_UPDATE'] = True
        else:
            # Get Project ID if it doesn't exist and if FORCE_UPDATE is existing and FALSE
            if 'PROJECT_ID' not in DATA:
                if 'FORCE_UPDATE' in DATA:
                    if 'FORCE_UPDATE' == False:
                        project_data = self._config_get(self.url + '/project')
                        DATA['PROJECT_ID'] = project_data['PROJECT_ID']
                else:
                    project_data = self._config_get(self.url + '/project')
                    DATA['PROJECT_ID'] = project_data['PROJECT_ID']
        return DATA

# 
# Supporting Functions
#

# General connect call to manage HTTP responses for all methods
    def __connect(self,request_obj):
        try:
            with request.urlopen(request_obj) as server:
    ##            response = codecs.decode(server.read(),'utf-8-sig')
                if request_obj.method == 'GET':
                    return json.loads(codecs.decode(server.read(),'utf-8-sig'))
                else:
                    return 'HTTP Code: {} - {}'.format(server.code,server.reason)
                #return 'HTTP Code: ' + str(server.code) + ' - ' + server.reason
        except error.HTTPError as err:
            # return 'HTTP Code: ' + str(err.code) + '\n' + codecs.decode(err.read(),'utf-8-sig')
            return 'HTTP Code: {}\n{}'.format(err.code, codecs.decode(err.read(),'utf-8-sig'))
        except error.URLError as err:
            return 'URLError: {} URL: {}'.format(err.reason, request_obj.get_full_url())

    # Fucntion used to ensure special characters are handled in the URL
    # Ex. = Space will be turned to %20
    def __url_validate(self, url):
        parsed_url = parse.urlparse(url)
        updated_path = parse.quote(parsed_url.path)
        return parsed_url._replace(path=updated_path).geturl()

    # Function used to build the basic authentication string
    def __build_auth_str(self, username, password):
        if isinstance(username, str):
            username = username.encode('latin1')
        if isinstance(password, str):
            password = password.encode('latin1')
        authstr = b64encode(b':'.join((username, password))).strip().decode('ascii')
        return authstr
    
    def __create_query(self, start = None, end = None, limit = None):
        query = {}
        if start != None and isinstance(start, datetime.datetime):
            query['start'] = start.isoformat()
        if end != None and isinstance(end, datetime.datetime):
            query['end'] = end.isoformat()
        if limit != None:
            query['limit'] = limit
        return query
