# -------------------------------------------------------------------------
# Copyright (c) 2023 PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`client` exposes an API to allow modifications (add, delete, modify) to 
UA Gateway plug-in client connection objects within the Kepware Configuration API. 
Certificate store read, remove and trust functionality is also available for the 
client connections.
"""

from typing import Union
from ..connection import server
from ..error import KepError, KepHTTPError
from ..ua_gateway.common import _INTER_TYPE, _change_cert_trust,  _create_url_cert, _create_url_client, _delete_cert_truststore

def get_certificate(server: server, certificate: str) -> dict:
    '''Returns the properties of the UAG client connection certificate object in the UAG client connection 
    certificate store. These are UA server instance certificates that are used by UAG client connections for
    trust purposes in the UA security model.
    
    :param server: instance of the `server` class
    :param certificate: name of certificate
    
    :return: Dict of data for the certificate requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url_cert(_INTER_TYPE.CLIENT, certificate))
    return r.payload

def get_all_certificates(server: server,  *, options: dict = None) -> list:
    '''Returns list of all UAG client connection certificate objects and their properties. These are UA server instance 
    certificates that are used by UAG client connections for trust purposes in the UA security model.
    
    :param server: instance of the `server` class
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of certificates. Options are `filter`, 
        `sortOrder`, `sortProperty`, `pageNumber`, and `pageSize`
    
    :return: List of data for all certificates in Kepware server UAG client connection certificate store

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url_cert(_INTER_TYPE.CLIENT), params= options)
    return r.payload

def trust_certificate(server: server, certificate: str) -> bool:
    '''Trusts the certificate in the UAG client connection certifcate store. This is updating the trust state of UA server instance 
    certificates that are used by UAG client connections for trust purposes in the UA security model.

    :param server: instance of the `server` class
    :param certificate: name of certificate
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    return _change_cert_trust(server, _INTER_TYPE.CLIENT, certificate, True)
    
def reject_certificate(server: server, certificate: str) -> bool:
    '''Rejects the certificate in the UAG client connection certifcate store. This is updating the trust state of UA server instance 
    certificates that are used by UAG client connections for trust purposes in the UA security model.

    :param server: instance of the `server` class
    :param certificate: name of certificate
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    return _change_cert_trust(server, _INTER_TYPE.CLIENT, certificate, False)

def delete_certificate(server: server, certificate: str) -> bool:
    '''Deletes the certificate in the UAG client endpoint certificate store.

    :param server: instance of the `server` class
    :param certificate: name of certificate
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    return _delete_cert_truststore(server, _INTER_TYPE.CLIENT, certificate)

def get_ua_client_connection(server: server, ua_client_connection: str) -> dict:
    '''Returns the properties of the UAG client connection object.
    
    :param server: instance of the `server` class
    :param ua_client_connection: name of ua_client_connection
    
    :return: Dict of data for the client connection requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url_client(ua_client_connection))
    return r.payload

def get_all_ua_client_connections(server: server,  *, options: dict = None) -> dict:
    '''Returns list of all UAG client connection objects and their properties.
    
    :param server: instance of the `server` class
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of client connections. Options are `filter`, 
        `sortOrder`, `sortProperty`, `pageNumber`, and `pageSize`
    
    :return: List of data for all client connections in Kepware server UAG

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url_client())
    return r.payload

def add_ua_client_connection(server: server, DATA: Union[dict, list]) -> Union[bool, list]:
    '''Add a `"UAG client connection"` or multiple `"UAG client connection"` objects to Kepware. This allows you 
    to create a client connection with all needed properties.

    Additionally it can be used to pass a list of UAG client connections to be added all at once.

    :param server: instance of the `server` class
    :param DATA: Dict of the connection or a list of connections
    expected by Kepware Configuration API

    :return: True - If a "HTTP 201 - Created" is received from Kepware server
    :return: If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    connections added that failed.

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_add(server.url + _create_url_client(), DATA)
    if r.code == 201: return True
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else: 
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
    
def modify_ua_client_connection(server: server, DATA: dict, *, ua_client_connection: str = None, force: bool = False) -> bool:
    '''Modify a UAG client connection object and it's properties in Kepware. If a `"ua_client_connection"` is not provided as an input,
    you need to identify the client connection in the *'common.ALLTYPES_NAME'* property field in `"DATA"`. It will 
    assume that is the client connection that is to be modified.

    :param server: instance of the `server` class
    :param DATA: Dict of the `ua_client_connection` properties to be modified
    :param ua_client_connection: *(optional)* name of client connection to modify. Only needed if not existing in `"DATA"`
    :param force: *(optional)* if True, will force the configuration update to the Kepware server
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    client_data = server._force_update_check(force, DATA)
    if ua_client_connection == None:
        try:
            r = server._config_update(server.url + _create_url_client(client_data['common.ALLTYPES_NAME']), client_data)
            if r.code == 200: return True 
            else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        except KeyError as err:
            err_msg = 'Error: No Channel identified in DATA | Key Error: {}'.format(err)
            raise KepError(err_msg)
        # except Exception as e:
        #     return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    else:
        r = server._config_update(server.url + _create_url_client(ua_client_connection), client_data)
        if r.code == 200: return True 
        else: 
            raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        
def del_ua_client_connection(server: server, ua_client_connection: str) -> bool:
    '''Delete a `"UAG client connection"` object in Kepware.
    
    :param server: instance of the `server` class
    :param ua_client_connection: name of client connection
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_del(server.url + _create_url_client(ua_client_connection))
    if r.code == 200: return True 
    else: 
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)