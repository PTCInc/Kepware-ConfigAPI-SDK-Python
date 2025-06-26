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

import warnings
from ..helpers.deprecation_utils import _deprecated


# Enable DeprecationWarnings to be visible
warnings.simplefilter('always', DeprecationWarning)

@_deprecated("This function is deprecated and will be removed in a future release. Use `get_instance_certificate()` in UAG client or server module instead.")
def get_instance_certificate(server: server) -> dict:
    '''
    DEPRECATED: This function is deprecated and will be removed in a future release. Use `get_instance_certificate()` 
    in UAG client or server module instead for Kepware 6.18+.

    Returns the properties of the UAG instance certificate object in the UAG certificate store. 
    These are UAG instance certificates that are used by UAG for trust purposes in the UA security model.
    
    :param server: instance of the `server` class
    
    :return: Dict of properties for the certificate requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url_cert(_INTER_TYPE.CERTS, INSTANCE_CERTIFICATE))
    return r.payload

@_deprecated("This function is deprecated and will be removed in a future release. Use `TBD` instead.")
def reissue_self_signed_instance_certificate(server: server) -> bool:
    '''
    DEPRECATED: This function is deprecated and will be removed in a future release. Use `get_instance_certificate()` 
    in UAG client or server module instead for Kepware 6.18+.
    
    Deletes and reissues a self-signed UAG instance certificate object in the UAG certificate store. 
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