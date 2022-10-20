# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`connection` exposes an API that manages the RESTful requests 
for the Kepware Configuration API. 
"""

import json
import codecs
import datetime
from urllib import request, parse, error
from base64 import b64encode
from .error import KepError, KepHTTPError, KepURLError
import socket
import ssl
import sys

class KepServiceResponse:
    '''A class to represent a return object when calling a "service" API of Kepware. This is
    used to return the responses when a "service" is executed appropriately

    Properties:

    "code" - HTTP code returned
    "message" - return from the "service" call
    "href" - URL reference to the JOB that is created by the service API
    '''

    def __init__(self, code = '', message = '', href = ''):
        self.code = code
        self.message = message
        self.href = href
    
    def __str__(self):
        return '{"code": %s, "message": %s, "href": %s}' % (self.code, self.message, self.href)

class KepServiceStatus:
    '''A class to represent a status object when checking on a "service" API job state in Kepware. This is
    used to return the status of a "service" job

    Properties:

    "complete" - Boolean of service job completion status
    "status" - Status code of job
    "message" - Error message if service job fails
    
    '''
    def __init__(self, complete = '', status = '', message = ''):
        self.status = status
        self.message = message
        self.complete = complete
    
    def __str__(self):
        return '{"complete": %s, "status": %s, "message": %s}' % (self.complete, self.status, self.message)

class _HttpDataAbstract:
    def __init__(self):
        self.payload = ''
        self.code = ''
        self.reason = ''

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
    "SSL_on" - Identify to use HTTPS connection (Default: False)
    "SSL_ignore_hostname" - During certificate validation ignore the hostname check
    "SSL_trust_all_certs" (insecure) - During certificate validation trust any certificate - if True, 
        will "set SSL_ignore_hostname" to true

    Methods:

    "reinitialize()" - reinitialize the Kepware server
    "get_trans_log()" - retrieve the Configuration API transaction logs
    "get_event_log()" - retrieve the Kepware Event Log
    "get_project_properties()" - retrieve the Kepware Project Properties
    "modify_project_properties()" - modify the Kepware Project Properties
    "service_status()" - retrive service job status
    '''
    __root_url = '/config'
    __version_url = '/v1'
    __project_services_url = '/project/services'
    __event_log_url = '/event_log'
    __trans_log_url = '/log'



    def __init__(self,  host = None, port = None, user = None, pw = None, https = False):
        self.host = host
        self.port = port
        self.username = user
        self.password = pw
        self.__ssl_context = ssl.create_default_context()
        self.__SSL_on = https
    
    @property
    def url(self):
        if self.SSL_on:
            proto = 'https'
        else:
            proto = 'http'
        return  '{}://{}:{}{}{}'.format(proto, self.host, self.port, self.__root_url, self.__version_url)
    
    @property
    def SSL_on(self):
        return self.__SSL_on
    
    @SSL_on.setter
    def SSL_on(self, val):
        if isinstance(val, bool):
            self.__SSL_on = val

    @property
    def SSL_ignore_hostname(self):
        return not self.__ssl_context.check_hostname

    @SSL_ignore_hostname.setter
    def SSL_ignore_hostname(self, val):
        if isinstance(val, bool):
            if val == True:
                self.__ssl_context.check_hostname = False
            else:
                self.__ssl_context.check_hostname = True

    
    @property
    def SSL_trust_all_certs(self):
        if self.__ssl_context.verify_mode == ssl.CERT_NONE:
            return True
        else:
            return False

    @SSL_trust_all_certs.setter
    def SSL_trust_all_certs(self, val):
        if isinstance(val, bool):
            if val == True:
                if self.__ssl_context.check_hostname == True:
                    self.__ssl_context.check_hostname = False
                self.__ssl_context.verify_mode = ssl.CERT_NONE
            else:
                self.__ssl_context.verify_mode = ssl.CERT_REQUIRED




    def reinitialize(self, job_ttl = None) -> KepServiceResponse:
        '''Executes a Reinitialize call to the Kepware instance.

        INPUTS:

        "job_ttl" (optional) - Determines the number of seconds a job instance will exist following completion.

        RETURNS:
        KepServiceResponse instance with job information

        EXCEPTIONS (If not HTTP 200 or 429 returned):
        
        KepHTTPError - If urllib provides an HTTPError
        KepURLError - If urllib provides an URLError
        '''
        url = self.url + self.__project_services_url + '/ReinitializeRuntime' 
        try:
            job = self._kep_service_execute(url, None, job_ttl)
            return job
        except Exception as err:
            raise err
        
    def get_trans_log(self, start = None, end = None, limit = None) -> list:
        ''' Get the Transaction Log from the Kepware instance.

        "start" (optional) - datetime.datetime type and should be UTC

        "end" (optional) - datetime.datetime type and should be UTC

        "limit" (optional) -  number of event log entries to request
        '''
        query = self.__create_query(start, end, limit)
        url = self.url + self.__trans_log_url + '?' + parse.urlencode(query)
        r = self._config_get(url)
        return r.payload

    def get_event_log(self, limit = None, start = None, end = None) -> list:
        ''' Get the Event Log from the Kepware instance.

        "start" (optional) - datetime.datetime type and should be UTC

        "end" (optional) - datetime.datetime type and should be UTC

        "limit" (optional) - number of event log entries to request
        '''
        query = self.__create_query(start, end, limit)
        url = self.url + self.__event_log_url + '?' + parse.urlencode(query)
        r = self._config_get(url)
        return r.payload
    
    def get_project_properties(self) -> dict:
        ''' Get the Project Properties of the Kepware instance.
        
        RETURNS:
        dict - Dict of all the project properties

        EXCEPTIONS:
        KepHTTPError - If urllib provides an HTTPError
        KepURLError - If urllib provides an URLError
        '''

        r = self._config_get(self.url + '/project')
        return r.payload
    
    def modify_project_properties(self, DATA, force = False) -> bool:
        ''' Modify the Project Properties of the Kepware instance.

        INPUTS:

        "DATA" - properly JSON object (dict) of the project properties to be modified

        "force" (optional) - if True, will force the configuration update to the Kepware server
        
        RETURNS:
        True - If a "HTTP 200 - OK" is received from Kepware

        EXCEPTIONS:
        KepHTTPError - If urllib provides an HTTPError
        KepURLError - If urllib provides an URLError
        '''

        prop_data = self._force_update_check(force, DATA)
        r = self._config_update(self.url + '/project', prop_data)
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
    
    def save_project(self, filename: str, password: str = None, job_ttl: int = None) -> KepServiceResponse:
        '''Executes a ProjectSave Service call to the Kepware instance. This saves 
        a copy of the current project file to disk. The filename

        INPUTS:
        
        "filename" - Fully qualified relative file path and name of project file including the file extension.
        location of project file save defaults: 
                TKS or KEP (Windows): C:\\PROGRAMDATA\\PTC\\Thingworx Kepware Server\\V6 or 
                                C:\\PROGRAMDATA\\Kepware\\KEPServerEX\\V6
                TKE (Linux):    /opt/tkedge/v1/user_data


        "password" (optional) - Specify a password with which to load or save an encrypted project file.  
            This password will be required to load this project file.
        
        "job_ttl" (optional) - Determines the number of seconds a job instance will exist following completion.

        RETURNS:
        KepServiceResponse instance with job information

        EXCEPTIONS (If not HTTP 200 or 429 returned):
        
        KepHTTPError - If urllib provides an HTTPError
        KepURLError - If urllib provides an URLError
        '''
        url = self.url + self.__project_services_url + '/ProjectSave'
        prop_data = {'servermain.PROJECT_FILENAME': filename}
        if password != None: prop_data['servermain.PROJECT_PASSWORD'] = password
        try:
            job = self._kep_service_execute(url, prop_data, job_ttl)
            return job
        except Exception as err:
            raise err

    def load_project(self, filename: str, password: str = None, job_ttl: int = None) -> KepServiceResponse:
        '''Executes a ProjectLoad Service call to the Kepware instance. This loads 
        a project file to disk.

        INPUTS:
        
        "filename" - Fully qualified path and name of project file including the file extension. Absolute
        paths required for TKS and KEP while file path is relative for TKE
            ex: Windows - filename = C:\\filepath\\test.opf
                Linux - filename = /filepath/test.lpf - Location is /opt/tkedge/v1/user_data/filepath/test.lpf

        "password" (optional) - Specify a password with which to load or save an encrypted project file.
        
        "job_ttl" (optional) - Determines the number of seconds a job instance will exist following completion.

        RETURNS:
        KepServiceResponse instance with job information

        EXCEPTIONS (If not HTTP 200 or 429 returned):
        
        KepHTTPError - If urllib provides an HTTPError
        KepURLError - If urllib provides an URLError
        '''
        url = self.url + self.__project_services_url + '/ProjectLoad'
        prop_data = {'servermain.PROJECT_FILENAME': filename}
        if password != None: prop_data['servermain.PROJECT_PASSWORD'] = password
        try:
            job = self._kep_service_execute(url, prop_data, job_ttl)
            return job
        except Exception as err:
            raise err


    def service_status(self, resp: KepServiceResponse):
        '''Returns the status of a service job. Used to verify if a service call
        has completed or not.

        INPUT:
        "resp" - KepServiceResponse instance with job information

        RETURNS:
        KepServiceStatus instance with job status

        EXCEPTIONS:
        
        KepHTTPError - If urllib provides an HTTPError
        KepURLError - If urllib provides an URLError
        '''
        # need to remove part of job href
        loc = resp.href.find(self.__root_url + self.__version_url)
        job_url = resp.href[loc + len(self.__root_url + self.__version_url):]

        r = self._config_get(self.url + job_url)
        job = KepServiceStatus(r.payload['servermain.JOB_COMPLETE'],r.payload['servermain.JOB_STATUS'], r.payload['servermain.JOB_STATUS_MSG'])
        return job


    #Function used to Add an object to Kepware (HTTP POST)
    def _config_add(self, url, DATA):
        '''Conducts an POST method at *url* to add an object in the Kepware Configuration
        *DATA* is required to be a properly JSON object (dict) of the item to be posted to *url* 
        '''
        data = json.dumps(DATA).encode('utf-8')
        url_obj = self.__url_validate(url)
        q = request.Request(url_obj, data, method='POST')
        r = self.__connect(q)
        return r

    #Function used to del an object to Kepware (HTTP DELETE)
    def _config_del(self, url):
        '''Conducts an DELETE method at *url* to delete an object in the Kepware Configuration'''
        url_obj = self.__url_validate(url)
        q = request.Request(url_obj, method='DELETE')
        r = self.__connect(q)
        return r

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
        r = self.__connect(q)
        return r

    #Function used to Read an object from Kepware (HTTP GET) and return the JSON response
    def _config_get(self, url):
        '''Conducts an GET method at *url* to retrieve an objects properties in the Kepware Configuration.'''
        url_obj = self.__url_validate(url)
        q = request.Request(url_obj, method='GET')
        r = self.__connect(q)
        return r

    
    def _force_update_check(self, force, DATA):
        if force == True:
            DATA['FORCE_UPDATE'] = True
        else:
            # Get Project ID if it doesn't exist and if FORCE_UPDATE is existing and FALSE
            if 'PROJECT_ID' not in DATA:
                if 'FORCE_UPDATE' in DATA:
                    if 'FORCE_UPDATE' == False:
                        try:
                            project_data = self._config_get(self.url + '/project')
                            DATA['PROJECT_ID'] = project_data.payload['PROJECT_ID']
                        except:
                            #NEED TO COVER ERROR CONDITION
                            pass
                else:
                    try:
                        project_data = self._config_get(self.url + '/project')
                        DATA['PROJECT_ID'] = project_data.payload['PROJECT_ID']
                    except:
                        #NEED TO COVER ERROR CONDITION
                        pass
        return DATA
    # General service call handler
    def _kep_service_execute(self, url, DATA = None, TTL = None):
        try:
            if TTL != None:
                if DATA == None: DATA = {}
                DATA["servermain.JOB_TIME_TO_LIVE_SECONDS"]= TTL
            r = self._config_update(url, DATA)
            job = KepServiceResponse(r.payload['code'],r.payload['message'], r.payload['href'])
            return job
        except KepHTTPError as err:
            if err.code == 429:
                job = KepServiceResponse()
                job.code = err.code
                job.message = err.payload
                return job
            else:
                raise err

# 
# Supporting Functions
#

    # General connect call to manage HTTP responses for all methods
    # Returns the response object for the method to handle as appropriate
    # Raises Errors as found
    def __connect(self,request_obj):
        # Fill appropriate header information
        data = _HttpDataAbstract()
        request_obj.add_header("Authorization", "Basic %s" % self.__build_auth_str(self.username, self.password))
        request_obj.add_header("Content-Type", "application/json")
        request_obj.add_header("Accept", "application/json")
        try:
            # context is sent regardless of HTTP or HTTPS - seems to be ignored if HTTP URL
            with request.urlopen(request_obj, context=self.__ssl_context) as server:
                try:
                    payload = server.read()
                    data.payload = json.loads(codecs.decode(payload,'utf-8-sig'))
                except:
                    pass
                data.code = server.code
                data.reason = server.reason
                return data
        except error.HTTPError as err:
            payload = json.loads(codecs.decode(err.read(),'utf-8-sig'))
            # print('HTTP Code: {}\n{}'.format(err.code,payload), file=sys.stderr)
            raise KepHTTPError(err.url, err.code, err.msg, err.hdrs, payload)
        except error.URLError as err:
            # print('URLError: {} URL: {}'.format(err.reason, request_obj.get_full_url()), file=sys.stderr)
            raise KepURLError(err.reason, request_obj.get_full_url())

    # Fucntion used to ensure special characters are handled in the URL
    # Ex: Space will be turned to %20
    def __url_validate(self, url):
        parsed_url = parse.urlparse(url)
        # Added % for scenarios where special characters have already been escaped with %
        updated_path = parse.quote(parsed_url.path, safe = '/%')

        # If host is "localhost", force using the IPv4 loopback adapter IP address in all calls
        # This is done to remove retries that will happen when the host resolution uses IPv6 intially
        # Kepware currently doesn't support IPv6 and is not listening on this interface
        if parsed_url.hostname.lower() == 'localhost':
            ip = socket.gethostbyname(parsed_url.hostname)
            parsed_url = parsed_url._replace(netloc='{}:{}'.format(ip, parsed_url.port))
        
        return parsed_url._replace(path=updated_path).geturl()

    # Function used to build the basic authentication string
    def __build_auth_str(self, username, password):
        if isinstance(username, str):
            username = username.encode('latin1')
        if isinstance(password, str):
            password = password.encode('latin1')
        authstr = b64encode(b':'.join((username, password))).strip().decode('ascii')
        return authstr
    
    # Create parameters for log queries
    def __create_query(self, start = None, end = None, limit = None):
        query = {}
        if start != None and isinstance(start, datetime.datetime):
            query['start'] = start.isoformat()
        if end != None and isinstance(end, datetime.datetime):
            query['end'] = end.isoformat()
        if limit != None:
            query['limit'] = limit
        return query


