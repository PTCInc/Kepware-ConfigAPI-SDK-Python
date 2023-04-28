# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`mapping` exposes an API to allow modifications (add, delete, modify) to 
column mapping objects in a Datalogger log group within the Kepware Configuration API
"""

from . import log_group as Log_Group
from ..error import KepError, KepHTTPError
from ..connection import server
from ..utils import _url_parse_object

MAPPING_ROOT = '/column_mappings'

def _create_url(mapping = None):
    '''Creates url object for the "column_mappings" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the mapping specific url when a value is passed as the column_mapping name.
    '''

    if mapping == None:
        return '{}'.format(MAPPING_ROOT)
    else:
        return '{}/{}'.format(MAPPING_ROOT, _url_parse_object(mapping))

def modify_mapping(server: server, log_group: str, DATA: dict, *, mapping: str = None, force: bool = False) -> bool:
    '''Modify a column `"mapping"` object and it's properties in Kepware. If a `"mapping"` is not provided as an input,
    you need to identify the column mapping in the *'common.ALLTYPES_NAME'* property field in the `"DATA"`. It will 
    assume that is the column mapping that is to be modified.

    :param server: instance of the `server` class
    :param log_group: name of log group for the mapping
    :param DATA: Dict of the mapping properties to be modified.
    :param mapping: *(optional)* column mapping to modify in the log group. Only needed if not existing in `"DATA"`
    :param force: *(optional)* if True, will force the configuration update to the Kepware server

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    
    mapping_data = server._force_update_check(force, DATA)
    
    if mapping == None:
        try:
            r = server._config_update(server.url + Log_Group._create_url(log_group) + _create_url(mapping_data['common.ALLTYPES_NAME']), mapping_data)
            if r.code == 200: return True 
            else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        except KeyError as err:
            err_msg = 'Error: No column mapping identified in DATA | Key Error: {}'.format(err)
            raise KepError(err_msg)
    else:
        r = server._config_update(server.url + Log_Group._create_url(log_group) + _create_url(mapping), mapping_data)
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_mapping(server: server, log_group: str, mapping: str) -> dict:
    '''Returns the properties of the `"mapping"` object.
    
    :param server: instance of the `server` class
    :param log_group: name of log group for the mapping
    :param mapping: name of column mapping to retrieve properties
    
    :return: Dict of properties for the mapping object requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + Log_Group._create_url(log_group) + _create_url(mapping))
    return r.payload

def get_all_mappings(server: server, log_group: str, *, options: dict = None) -> list:
    '''Returns the properties of all column `"mapping"` objects for a log group.
    
    :param server: instance of the `server` class
    :param log_group: name of log group for the mapping
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of mapping items. Options are 'filter', 
    'sortOrder', 'sortProperty', 'pageNumber', and 'pageSize'. Only used when exchange_name is not defined.

    :return: list of properties for all mapping items in the log group requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(f'{server.url}{Log_Group._create_url(log_group)}{_create_url()}', params= options)
    return r.payload
