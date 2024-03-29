# -------------------------------------------------------------------------
# Copyright (c), PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`lls` exposes an API to allow modifications to Local License Server parameters in 
the Kepware Administration through the Kepware Configuration API
"""
from .. import connection
from typing import Union
from ..error import KepHTTPError, KepError



LLS_ROOT = '/admin'
FORCE_CHECK_URL = '/project/services/ForceLicenseCheck'
LICENSING_SERVER_PORT = "libadminsettings.LICENSING_SERVER_PORT"
LICENSING_SERVER_NAME = "libadminsettings.LICENSING_SERVER_NAME"
LICENSING_SERVER_ENABLE = "libadminsettings.LICENSING_SERVER_ENABLE"
LICENSING_CHECK_PERIOD_MINS = "libadminsettings.LICENSING_CHECK_PERIOD_MINS"
LICENSING_SERVER_SSL_PORT = "libadminsettings.LICENSING_SERVER_SSL_PORT"
LICENSING_SERVER_ALLOW_INSECURE_COMMS = "libadminsettings.LICENSING_SERVER_ALLOW_INSECURE_COMMS"
LICENSING_SERVER_ALLOW_SELF_SIGNED_CERTS = "libadminsettings.LICENSING_SERVER_ALLOW_SELF_SIGNED_CERTS"
LICENSING_CLIENT_ALIAS = "libadminsettings.LICENSING_CLIENT_ALIAS"

class lls_config:
    '''A class to represent a admin properties for the Local License Server connection from an instance of Kepware. 
    This object is used to easily manage the LLS parameters for a Kepware instance. 

    :param server_name: Host name or IP address of the LLS server
    :param server_port: HTTP/non-SSL port to target for the LLS server
    :param check_period: Period that Kepware checks licensing status
    :param server_port_SSL: HTTPS/SSL port to target for the LLS server
    :param allow_insecure_comms: When True, use HTTP/non-SSL connection to LLS
    :param allow_self_signed_certs: Allow for self signed certificates to be used during HTTPS/SSL connections to the LLS
    :param instance_alias_name: Alias name for LLS to use as reference to this Kepware instance
    '''

    def __init__(self, config = {}):
        self.server_name = config[LICENSING_SERVER_NAME] if LICENSING_SERVER_NAME in config else ''
        self.server_port = config[LICENSING_SERVER_PORT] if LICENSING_SERVER_PORT in config else 7070
        self.check_period = config[LICENSING_CHECK_PERIOD_MINS] if LICENSING_CHECK_PERIOD_MINS in config else 5
        self.server_port_SSL = config[LICENSING_SERVER_SSL_PORT] if LICENSING_SERVER_SSL_PORT in config else 1883
        self.allow_insecure_comms = config[LICENSING_SERVER_ALLOW_INSECURE_COMMS] if LICENSING_SERVER_ALLOW_INSECURE_COMMS in config else False
        self.allow_self_signed_certs = config[LICENSING_SERVER_ALLOW_SELF_SIGNED_CERTS] if LICENSING_SERVER_ALLOW_SELF_SIGNED_CERTS in config else False
        self.instance_alias_name = config[LICENSING_CLIENT_ALIAS] if LICENSING_CLIENT_ALIAS in config else ''
    
    def _get_dict(self):
        return {
            LICENSING_SERVER_PORT: self.server_port,
            LICENSING_SERVER_NAME: self.server_name,
            LICENSING_CHECK_PERIOD_MINS: self.check_period,
            LICENSING_SERVER_SSL_PORT: self.server_port_SSL,
            LICENSING_SERVER_ALLOW_INSECURE_COMMS: self.allow_insecure_comms,
            LICENSING_SERVER_ALLOW_SELF_SIGNED_CERTS: self.allow_self_signed_certs,
            LICENSING_CLIENT_ALIAS: self.instance_alias_name
        }
    
    def __str__(self) -> str:
        return "{}".format(self._get_dict())

def get_lls_config(server: connection.server) -> lls_config:
    '''Returns the properties of the Local License server connection properties. Returned object is `lls_config` class object.
    
    :param server: instance of the `server` class
    
    :return: `lls_config` class object with lls connection configuration

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_get(server.url + LLS_ROOT)
    return lls_config(r.payload)

def update_lls_config(server: connection.server, config: lls_config) -> bool:
    '''Updates the Local License Server connection properties for Kepware.
    
    :param server: instance of the `server` class
    :param config: `lls_config` class object with lls connection configuration
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    DATA = config._get_dict()
    r = server._config_update(server.url + LLS_ROOT, DATA)
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def enable_lls(server: connection.server) -> bool:
    '''Enables the Local License Server connection for Kepware.
    
    :param server: instance of the `server` class
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_update(server.url + LLS_ROOT, {LICENSING_SERVER_ENABLE: True})
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def disable_lls(server: connection.server) -> bool:
    '''Disables the Local License Server connection for Kepware.
    
    :param server: instance of the `server` class
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_update(server.url + LLS_ROOT, {LICENSING_SERVER_ENABLE: False})
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def force_license_check(server: connection.server, job_ttl: int = None):
    '''Executes a ForceLicenseCheck service call to the Kepware instance. This triggers the server to verify the 
    license state of the license received from the Local License Server.

    :param server: instance of the `server` class
    :param job_ttl: *(optional)* Determines the number of seconds a job instance will exist following completion.

    :return: `KepServiceResponse` instance with job information

    :raises KepHTTPError: If urllib provides an HTTPError (If not HTTP code 202 [Accepted] or 429 [Too Busy] returned)
    :raises KepURLError: If urllib provides an URLError
    '''

    url = f'{server.url}{FORCE_CHECK_URL}'
    job = server._kep_service_execute(url, None, job_ttl)
    return job