# -------------------------------------------------------------------------
# Copyright (c) 2023 PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`certificates` exposes an API to allow read access to 
UA Gateway plug-in instance certificate objects within the Kepware Configuration API
"""

from ..connection import server
from ..ua_gateway.common import _INTER_TYPE, _create_url_cert

def get_certificate(server: server, certificate: str) -> dict:
    '''Returns the properties of the UAG instance certificate object in the UAG certificate store. 
    These are UAG instance certificates that are used by UAG for trust purposes in the UA security model.
    
    :param server: instance of the `server` class
    :param certificate: name of certificate
    
    :return: Dict of data for the certificate requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url_cert(_INTER_TYPE.CERTS, certificate))
    return r.payload

def get_all_certificates(server: server,  *, options: dict = None) -> list:
    '''Returns list of all UAG instance certificate objects and their properties in the UAG certificate store. 
    These are UAG instance certificates that are used by UAG for trust purposes in the UA security model.
    
    :param server: instance of the `server` class
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of certificates. Options are `filter`, 
        `sortOrder`, `sortProperty`, `pageNumber`, and `pageSize`
    
    :return: List of data for all certificates in Kepware server UAG server endpoint certificate store

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url_cert(_INTER_TYPE.CERTS), params= options)
    return r.payload