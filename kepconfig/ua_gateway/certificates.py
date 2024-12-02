# -------------------------------------------------------------------------
# Copyright (c) 2023 PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`certificates` exposes an API to allow read access to 
UA Gateway plug-in instance certificate objects within the Kepware Configuration API
"""

from ..connection import server
from ..error import KepHTTPError
from ..ua_gateway.common import _INTER_TYPE, _create_url_cert, INSTANCE_CERTIFICATE

def get_instance_certificate(server: server) -> dict:
    '''Returns the properties of the UAG instance certificate object in the UAG certificate store. 
    These are UAG instance certificates that are used by UAG for trust purposes in the UA security model.
    
    :param server: instance of the `server` class
    
    :return: Dict of properties for the certificate requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url_cert(_INTER_TYPE.CERTS, INSTANCE_CERTIFICATE))
    return r.payload

# def get_all_certificates(server: server,  *, options: dict = None) -> list:
#     TODO: Implement if/when multiple instance certificates can be configured.
#     '''Returns list of all UAG instance certificate objects and their properties in the UAG certificate store. 
#     These are UAG instance certificates that are used by UAG for trust purposes in the UA security model.
    
#     :param server: instance of the `server` class
#     :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of certificates. Options are `filter`, 
#         `sortOrder`, `sortProperty`, `pageNumber`, and `pageSize`
    
#     :return: List of data for all certificates in Kepware server UAG server endpoint certificate store

#     :raises KepHTTPError: If urllib provides an HTTPError
#     :raises KepURLError: If urllib provides an URLError
#     '''
#     r = server._config_get(server.url + _create_url_cert(_INTER_TYPE.CERTS), params= options)
#     return r.payload

def reissue_self_signed_instance_certificate(server: server) -> bool:
    '''Deletes and reissues a self-signed UAG instance certificate object in the UAG certificate store. 
    This is the UAG instance certificate that are used by UAG for trust purposes in the UA security model.
    
    :param server: instance of the `server` class
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_del(server.url + _create_url_cert(_INTER_TYPE.CERTS, INSTANCE_CERTIFICATE))
    if r.code == 200: return True 
    else: 
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)