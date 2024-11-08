from ..utils import _url_parse_object
from ..connection import server
from ..error import KepHTTPError
from enum import Enum

r"""`common` contains common internal functions and constants used by the 
`ua_gateway` module.
"""

CERT_TRUST_KEY = 'ua_gateway.UA_CERTIFICATE_TRUST_STATUS'

# URL Constants for UA Gateway Module

UA_GATEWAY_ROOT = '/project/_ua_gateway'
CERT_ROOT = f'{UA_GATEWAY_ROOT}/certificates'
CLIENT_ROOT = f'{UA_GATEWAY_ROOT}/ua_client_interfaces/Client Interface'
CONN_ROOT = f'{CLIENT_ROOT}/ua_client_connections'
CLIENT_CERT_ROOT = f'{CLIENT_ROOT}/certificates'
SERVER_ROOT = f'{UA_GATEWAY_ROOT}/ua_server_interfaces/Server Interface'
ENDPOINT_ROOT = f'{SERVER_ROOT}/ua_server_endpoints'
SERVER_CERT_ROOT = f'{SERVER_ROOT}/certificates'


class _INTER_TYPE(Enum):
    SERVER = 0
    CLIENT = 1
    CERTS = 2


def _create_url_cert(interface, certificate = None):
    '''Creates url object for the "certificate" branch of Kepware's UA Gateway. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the UA Gateway client interfaces specific certificate url when a value is passed as the certificate name.
    '''
    if interface == _INTER_TYPE.SERVER:
        if certificate == None:
            return SERVER_CERT_ROOT
        else:
            return f'{SERVER_CERT_ROOT}/{_url_parse_object(certificate)}'
    elif interface == _INTER_TYPE.CLIENT:
        if certificate == None:
            return CLIENT_CERT_ROOT
        else:
            return f'{CLIENT_CERT_ROOT}/{_url_parse_object(certificate)}'
    else:
        if certificate == None:
            return CERT_ROOT
        else:
            return '{}/{}'.format(CERT_ROOT,_url_parse_object(certificate))

def _change_cert_trust(server: server, inter_type, certificate: str, trust: bool):
    DATA = {
        CERT_TRUST_KEY: int(trust)
    }

    cert_data = server._force_update_check(True, DATA)
    r = server._config_update(server.url + _create_url_cert(inter_type, certificate), cert_data)
    if r.code == 200: return True 
    else: 
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def _create_url_server(ua_server_endpoint = None):
    '''Creates url object for the "ua_server_endpoints" branch of Kepware's UA Gateway. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the UA Gateway client connections specific url when a value is passed as the ua client interface name.
    '''
    if ua_server_endpoint == None:
        return ENDPOINT_ROOT
    else:
        return f'{ENDPOINT_ROOT}/{_url_parse_object(ua_server_endpoint)}'
    
def _create_url_client(ua_client_connection = None):
    '''Creates url object for the "ua_client_connections" branch of Kepware's UA Gateway. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the UA Gateway client connections specific url when a value is passed as the ua client interface name.
    '''
    if ua_client_connection == None:
        return CONN_ROOT
    else:
        return f'{CONN_ROOT}/{_url_parse_object(ua_client_connection)}'