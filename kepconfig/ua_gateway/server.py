# -------------------------------------------------------------------------
# Copyright (c) 2023 PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`server` exposes an API to allow modifications (add, delete, modify) to 
UA Gateway plug-in server endpoint objects within the Kepware Configuration API. 
Certificate read and trust functionality is also available for the server endpoints.
"""

from typing import Union
from ..connection import server
from ..error import KepError, KepHTTPError
from ..ua_gateway.common import _INTER_TYPE, _change_cert_trust, _create_url_cert, _create_url_server


def get_certificate(server: server, certificate: str) -> dict:
    '''Returns the properties of the UAG server endpoint certificate object in the UAG client connection 
    certificate store. These are UA client instance certificates that are used by UAG server endpoints for
    trust purposes in the UA security model.
    
    :param server: instance of the `server` class
    :param certificate: name of certificate
    
    :return: Dict of data for the certificate requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url_cert(_INTER_TYPE.SERVER, certificate))
    return r.payload

def get_all_certificates(server: server, *, options: dict = None) -> list:
    '''Returns list of all UAG server endpoint certificate objects and their properties.This is updating the trust state of UA client instance 
    certificates that are used by UAG server endpoints for trust purposes in the UA security model. These are UA client instance certificates 
    that are used by UAG server endpoints for trust purposes in the UA security model.
    
    :param server: instance of the `server` class
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of certificates. Options are `filter`, 
        `sortOrder`, `sortProperty`, `pageNumber`, and `pageSize`
    
    :return: List of data for all certificates in Kepware server UAG server endpoint certificate store

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url_cert(_INTER_TYPE.SERVER), params= options)
    return r.payload

def trust_certificate(server: server, certificate: str) -> bool:
    '''Trusts the certificate in the UAG server endpoint certifcate store. This is updating the trust state of UA client instance 
    certificates that are used by UAG server endpoints for trust purposes in the UA security model.

    :param server: instance of the `server` class
    :param certificate: name of certificate
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    return _change_cert_trust(server, _INTER_TYPE.SERVER, certificate, True)

def reject_certificate(server: server, certificate: str) -> bool:
    '''Rejects the certificate in the UAG server endpoint certifcate store.

    :param server: instance of the `server` class
    :param certificate: name of certificate
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    return _change_cert_trust(server, _INTER_TYPE.SERVER, certificate, False)

def get_ua_server_endpoint(server: server, ua_server_endpoint: str) -> dict:
    '''Returns the properties of the UAG server endpoint object.
    
    :param server: instance of the `server` class
    :param ua_server_endpoint: name of ua_server_endpoint
    
    :return: Dict of data for the server endpoint requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url_server(ua_server_endpoint))
    return r.payload

def get_all_ua_server_endpoints(server: server,  *, options: dict = None) -> dict:
    '''Returns list of all UAG server endpoint objects and their properties.
    
    :param server: instance of the `server` class
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of server endpoints. Options are `filter`, 
        `sortOrder`, `sortProperty`, `pageNumber`, and `pageSize`
    
    :return: List of data for all server endpoints in Kepware server UAG

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url_server())
    return r.payload

def add_ua_server_endpoint(server: server, DATA: Union[dict, list]) -> Union[bool, list]:
    '''Add a `"UAG server endpoint"` or multiple `"UAG server endpoint"` objects to Kepware. This allows you 
    to create a server endpoint with all needed properties.

    Additionally it can be used to pass a list of UAG server endpoint to be added all at once.

    :param server: instance of the `server` class
    :param DATA: Dict of the endpoint or a list of endpoints
    expected by Kepware Configuration API

    :return: True - If a "HTTP 201 - Created" is received from Kepware server
    :return: If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    endpoints added that failed.

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_add(server.url + _create_url_server(), DATA)
    if r.code == 201: return True
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else: 
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
    
def modify_ua_server_endpoint(server: server, DATA: dict, *, ua_server_endpoint: str = None, force: bool = False) -> bool:
    '''Modify a UAG server endpoint object and it's properties in Kepware. If a `"ua_server_endpoint"` is not provided as an input,
    you need to identify the client connection in the *'common.ALLTYPES_NAME'* property field in `"DATA"`. It will 
    assume that is the client connection that is to be modified.

    :param server: instance of the `server` class
    :param DATA: Dict of the `ua_server_endpoint` properties to be modified
    :param ua_server_endpoint: *(optional)* name of server endpoint to modify. Only needed if not existing in `"DATA"`
    :param force: *(optional)* if True, will force the configuration update to the Kepware server
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    server_data = server._force_update_check(force, DATA)
    if ua_server_endpoint == None:
        try:
            r = server._config_update(server.url + _create_url_server(server_data['common.ALLTYPES_NAME']), server_data)
            if r.code == 200: return True 
            else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        except KeyError as err:
            err_msg = 'Error: No Channel identified in DATA | Key Error: {}'.format(err)
            raise KepError(err_msg)
        # except Exception as e:
        #     return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    else:
        r = server._config_update(server.url + _create_url_server(ua_server_endpoint), server_data)
        if r.code == 200: return True 
        else: 
            raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        
def del_ua_server_endpoint(server: server, ua_server_endpoint: str) -> bool:
    '''Delete a `"UAG server endpoint"` object in Kepware.
    
    :param server: instance of the `server` class
    :param ua_server_endpoint: name of server endpoint
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_del(server.url + _create_url_server(ua_server_endpoint))
    if r.code == 200: return True 
    else: 
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)