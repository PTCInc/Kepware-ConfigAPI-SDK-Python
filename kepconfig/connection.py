# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`connection` exposes an `server` class that manages the connection
information and RESTful requests for the Kepware Configuration API Library.
"""

import json
import codecs
import datetime
from urllib import request, parse, error
from base64 import b64encode
from .error import KepError, KepHTTPError, KepURLError
import socket
import ssl
from .structures import KepServiceResponse, KepServiceStatus, _HttpDataAbstract, Filter


class server:
    '''A class to represent a connection to an instance of Kepware. This object is used to 
    create the Authentication and server parameters to taget a Kepware instance. An instance of this is 
    used in all configuration calls done.

    :param host: host name or IP address
    :param port: port of Configuration API
    :param username: username to conduct "Basic Authentication"
    :param password: password to conduct "Basic Authentication"
    :param https: Sets `SSL_on` to use HTTPS connection (Default: False)
    :param SSL_on: Identify to use HTTPS connection (Default: False)
    :param SSL_ignore_hostname: During certificate validation ignore the hostname check
    :param SSL_trust_all_certs: (insecure) - During certificate validation trust any certificate - if True, 
        will "set SSL_ignore_hostname" to true
    :param url: base URL for the server connection

    **Methods**

    :meth:`reinitialize`: reinitialize the Kepware server

    :meth:`get_transaction_log`: retrieve the Configuration API transaction logs

    :meth:`get_event_log`: retrieve the Kepware Event Log

    :meth:`get_audit_log`: retrieve the Kepware Audit Log

    :meth:`get_info`: retrieve the Kepware product information
    
    :meth:`import_empty_project`: import an empty project to the Kepware server

    :meth:`get_project_properties`: retrieve the Kepware Project Properties

    :meth:`modify_project_properties` - modify the Kepware Project Properties

    :meth:`service_status` - retrive service job status

    :meth:`export_project_configuration` - export the current project configuration in JSON format

    :meth:`save_project` - save the current project to a file

    :meth:`load_project` - load a project from a file
    '''
    __root_url = '/config'
    __version_url = '/v1'
    __project_services_url = '/project/services'
    __event_log_url = '/event_log'
    __trans_log_url = '/log'
    __audit_log_url = '/audit_log'



    def __init__(self,  host: str, port: int, user: str, pw: str, https: bool = False):
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
        return  f'{proto}://{self.host}:{self.port}{self.__root_url}{self.__version_url}'
    
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


    def get_status(self) -> dict:
        '''Executes a health status request to the Kepware instance to report service statuses.

        :return: List of data for the health status request

        :raises KepHTTPError: If urllib provides an HTTPError
        :raises KepURLError: If urllib provides an URLError
        '''

        r = self._config_get(f'{self.url}/status')
        return r.payload
    def get_info(self) -> dict:
        '''Requests product information from the Kepware instance. Provides various information including
        product name and version information.

        :return: dict of data for the product information request
        
        :raises KepHTTPError: If urllib provides an HTTPError
        :raises KepURLError: If urllib provides an URLError
        '''
        
        r = self._config_get(f'{self.url}/about')
        return r.payload

    def reinitialize(self, job_ttl: int = None) -> KepServiceResponse:
        '''Executes a Reinitialize service call to the Kepware instance.

        :param job_ttl: *(optional)* Determines the number of seconds a job instance will exist following completion.

        :return: `KepServiceResponse` instance with job information

        :raises KepHTTPError: If urllib provides an HTTPError (If not HTTP code 202 [Accepted] or 429 [Too Busy] returned)
        :raises KepURLError: If urllib provides an URLError
        '''
        url = self.url + self.__project_services_url + '/ReinitializeRuntime' 
        try:
            job = self._kep_service_execute(url, None, job_ttl)
            return job
        except Exception as err:
            raise err
        
    def get_transaction_log(self, limit: int = None, start: datetime.datetime = None, end: datetime.datetime = None) -> list:
        ''' Get the Transaction Log from the Kepware instance.

        :param limit: *(optional)* number of transaction log entries to request
        :param start: *(optional)* start time of query as `datetime.datetime` type and should be UTC
        :param end: *(optional)* end time of query as `datetime.datetime` type and should be UTC

        :raises KepHTTPError: If urllib provides an HTTPError
        :raises KepURLError: If urllib provides an URLError
        '''
        query = self.__create_query(start, end, limit)
        url = f'{self.url}{self.__trans_log_url}'
        r = self._config_get(url, params= query)
        return r.payload

    def get_event_log(self, limit: int = None, start: datetime.datetime = None, end: datetime.datetime = None, *, options: dict = None) -> list:
        ''' Get the Event Log from the Kepware instance.

        :param limit: *(optional)* number of event log entries to request
        :param start: *(optional)* start time of query as `datetime.datetime` type and should be UTC
        :param end: *(optional)* end time of query as `datetime.datetime` type and should be UTC
        :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of transactions. Options are `event`, 
        `sortOrder`, `sortProperty`, `pageNumber`, and `pageSize`

        :raises KepHTTPError: If urllib provides an HTTPError
        :raises KepURLError: If urllib provides an URLError
        '''
        query = self.__create_query(start, end, limit)
        if options is not None:
            query = {**query, **options}
        url = f'{self.url}{self.__event_log_url}'
        r = self._config_get(url, params= query)
        return r.payload

    def get_audit_log(self, limit: int = None, *, filters: list[Filter] = None, options: dict = None) -> list:
        ''' Get the Audit Log from the Kepware instance.

        :param limit: *(optional)* number of event log entries to request
        :param filters: *(optional)* list of filters that are used to control results returned from the log
        :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of transactions. Options are `sortOrder`, 
        `sortProperty`, `pageNumber`, and `pageSize`

        :raises KepHTTPError: If urllib provides an HTTPError
        :raises KepURLError: If urllib provides an URLError
        '''
        query = self.__create_filter_query(filters)
        if limit is not None:
            query['limit'] = limit
        if options is not None:
            query = {**query, **options}
        url = f'{self.url}{self.__audit_log_url}'
        r = self._config_get(url, params= query)
        return r.payload
    
    def get_project_properties(self) -> dict:
        ''' Get the Project Properties of the Kepware instance.
        
        :return: Dict of all the project properties

        :raises KepHTTPError: If urllib provides an HTTPError
        :raises KepURLError: If urllib provides an URLError
        '''

        r = self._config_get(self.url + '/project')
        return r.payload
    
    def modify_project_properties(self, DATA: dict, force: bool = False) -> bool:
        ''' Modify the Project Properties of the Kepware instance.

        :param DATA: Dict of the project properties to be modified
        :param force: *(optional)* if True, will force the configuration update to the Kepware server
        
        :return: True - If a "HTTP 200 - OK" is received from Kepware server

        :raises KepHTTPError: If urllib provides an HTTPError
        :raises KepURLError: If urllib provides an URLError
        '''

        prop_data = self._force_update_check(force, DATA)
        r = self._config_update(self.url + '/project', prop_data)
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
    
    def import_empty_project(self) -> KepServiceResponse:
        '''Executes JsonProjectLoad Service call to the Kepware instance with an empty project. This service 
        imports an empty project configuration, acts like a FILE->NEW action and 
        stop communications while the new project replaces the current project in the Kepware runtime. 

        :return: `KepServiceResponse` instance with job information
        
        :raises KepHTTPError: If urllib provides an HTTPError (If not HTTP code 202 [Accepted] or 429 [Too Busy] returned)
        :raises KepURLError: If urllib provides an URLError
        '''
        return self.import_project_configuration({"project":{}})


    def import_project_configuration(self, DATA: dict) -> KepServiceResponse:
        '''Executes JsonProjectLoad Service call to the Kepware instance. This service imports project configuration 
        data, expecting a complete project file in JSON/dict format. This service acts like a FILE->OPEN action and 
        stop communications while the new project replaces the current project in the Kepware runtime. 
    
        :param DATA: Complete project configuration data in JSON/dict format. 

        :return: `KepServiceResponse` instance with job information
        
        :raises KepHTTPError: If urllib provides an HTTPError (If not HTTP code 202 [Accepted] or 429 [Too Busy] returned)
        :raises KepURLError: If urllib provides an URLError
        '''
        url = self.url + self.__project_services_url + '/JsonProjectLoad'
        try:
            job = self._kep_service_execute(url, DATA)
            return job
        except Exception as err:
            raise err
        
    def export_project_configuration(self) -> dict:
        '''Get a complete copy of the project configuration in JSON format. This will include the same 
        configuration that is stored when you save the project file manually.

        :return: Dict of the complete project configuration

        :raises KepHTTPError: If urllib provides an HTTPError
        :raises KepURLError: If urllib provides an URLError
        '''
        r = self._config_get(self.url + '/project', params= {"content": "serialize"})
        return r.payload
    
    def save_project(self, filename: str, password: str = None, job_ttl: int = None) -> KepServiceResponse:
        '''Executes a ProjectSave Service call to the Kepware instance. This saves 
        a copy of the current project file to disk. The filename

        :param filename: Relative file path and name of project file including the file extension to save.
        Location of relative project file paths:
         
                TKS or KEP (Windows): C:\\PROGRAMDATA\\PTC\\Thingworx Kepware Server\\V6 or 
                                C:\\PROGRAMDATA\\Kepware\\KEPServerEX\\V6
                TKE (Linux):    /opt/tkedge/v1/user_data


        :param password: *(optional)* Specify a password with which to  save an encrypted project file with.  
            This password will be required to load this project file.
        :param job_ttl: *(optional)* Determines the number of seconds a job instance will exist following completion.

        :return: `KepServiceResponse` instance with job information

        :raises KepHTTPError: If urllib provides an HTTPError (If not HTTP code 202 [Accepted] or 429 [Too Busy] returned)
        :raises KepURLError: If urllib provides an URLError
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
        
        :param filename: Fully qualified or relative path and name of project file including the file extension. Absolute
        paths required for TKS and KEP while file path is relative for TKE:

                Windows - filename = C:\\filepath\\test.opf
                Linux - filename = filepath/test.lpf - Location is /opt/tkedge/v1/user_data/filepath/test.lpf

        :param password: *(optional)* Specify a password with which to load an encrypted project file.          
        :param job_ttl: *(optional)* Determines the number of seconds a job instance will exist following completion.

        :return: `KepServiceResponse` instance with job information

        :raises KepHTTPError: If urllib provides an HTTPError (If not HTTP code 202 [Accepted] or 429 [Too Busy] returned)
        :raises KepURLError: If urllib provides an URLError
        '''
        url = self.url + self.__project_services_url + '/ProjectLoad'
        prop_data = {'servermain.PROJECT_FILENAME': filename}
        if password != None: prop_data['servermain.PROJECT_PASSWORD'] = password
        try:
            job = self._kep_service_execute(url, prop_data, job_ttl)
            return job
        except Exception as err:
            raise err

    def get_project_backup_info(self) -> dict:
        ''' Get the Project Backup Information of the Kepware instance.
        
        :return: List of all the backup projects and their properties.

        :raises KepHTTPError: If urllib provides an HTTPError
        :raises KepURLError: If urllib provides an URLError
        '''

        r = self._config_get(self.url + '/project/backups')
        return r.payload

    def backup_project(self, job_ttl: int = None) -> KepServiceResponse:
        '''Executes a CreateBackup Service call to the Kepware instance. This saves 
        a copy of the current project file to disk as a backup that can be retrieved.

        :param job_ttl: *(optional)* Determines the number of seconds a job instance will exist following completion.

        :return: `KepServiceResponse` instance with job information

        :raises KepHTTPError: If urllib provides an HTTPError (If not HTTP code 202 [Accepted] or 429 [Too Busy] returned)
        :raises KepURLError: If urllib provides an URLError
        '''
        url = self.url + self.__project_services_url + '/CreateBackup'
        try:
            job = self._kep_service_execute(url, TTL= job_ttl)
            return job
        except Exception as err:
            raise err
        
    def service_status(self, resp: KepServiceResponse):
        '''Returns the status of a service job. Used to verify if a service call
        has completed or not.

        :param resp: `KepServiceResponse` instance with job information

        :return: `KepServiceStatus` instance with job status

        :raises KepHTTPError: If urllib provides an HTTPError
        :raises KepURLError: If urllib provides an URLError
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
        if len(DATA) == 0:
            err_msg = f'Error: Empty List or Dict in DATA | DATA type: {type(DATA)}'
            raise KepError(err_msg) 
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
    def _config_get(self, url, *, params = None):
        '''
        Conducts an GET method at *url* to retrieve an objects properties with query parameters in 
        the Kepware Configuration.
        '''
        # Add parameters when necessary
        if params is not None and params != {}:
            qparams = parse.urlencode(params)
            url = f'{url}?{qparams}'
        url_obj = self.__url_validate(url)
        q = request.Request(url_obj, method='GET')
        r = self.__connect(q)
        return r

    
    def _force_update_check(self, force, DATA):
        '''
        This will validate if the modify call needs to be forced or not. If forced, the dict DATA needs
        to have the 'FORCE_UPDATE' property with a value of True. If forced is not requested, it is necessary
        to provide the current 'PROJECT_ID'. If 'PROJECT_ID' is not present in DATA, this will automatically 
        retreive it from the active server.
        '''
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
            raise KepHTTPError(url=err.url, code=err.code, msg=err.msg, hdrs=err.hdrs, payload=payload)
        except error.URLError as err:
            # print('URLError: {} URL: {}'.format(err.reason, request_obj.get_full_url()), file=sys.stderr)
            raise KepURLError(msg=err.reason, url=request_obj.get_full_url())

    # Fucntion used to ensure special characters are handled in the URL
    # Ex: Space will be turned to %20
    def __url_validate(self, url):
        # Configuration API does not use fragments in URL so ignore to allow # as a character
        # Objects in Kepware can include # as part of the object names
        parsed_url = parse.urlparse(url, allow_fragments= False)
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

    # Create filter query for log queries
    def __create_filter_query(self, filters: list[Filter] = None):
        query = {}
        if filters is None:
            return query
        for f in filters:
            # Ensure we use the value of the Enum, not the Enum object itself
            key = f"filter[{f.field.value}][{f.modifier.value}]"
            query[key] = f.value
        return query