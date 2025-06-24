# filepath: c:\Users\rlabbe\OneDrive - PTC\Documents\GitHub\Kepware-ConfigAPI-SDK-Python\kepconfig\connectivity\adv_tag_group.py
# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Note: The code within this file was created in total or in part
#  with the use of AI tools.


r"""`adv_tag_group` exposes an API to allow modifications (add, delete, modify) to 
tag group objects within the Kepware Configuration API
"""

from ..connection import KepServiceResponse, server
from ..error import KepHTTPError, KepError
from ..utils import _url_parse_object, path_split
from typing import Union
from .. import adv_tags
import inspect

TAG_GROUP_ROOT = '/advanced_tag_groups'

def _create_url(tag_group=None):
    '''Creates url object for the "tag group" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure
    
    Returns the tag group specific url when a value is passed as the tag group name.
    '''
    if tag_group is None:
        return TAG_GROUP_ROOT
    else:
        return '{}/{}'.format(TAG_GROUP_ROOT, _url_parse_object(tag_group))

def _create_adv_tags_group_url(path_obj):
    '''Creates url object for the "path_obj" which provides the adv tags tag group structure of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure
    
    Returns the advanced tag group specific url when a value is passed as the tag group name.
    '''

    try:
        url = ''
        if 'tag_path' in path_obj:
            for obj in path_obj['tag_path']:
                url += _create_url(obj)
    except KeyError as err:
        err_msg = 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
        raise KepError(err_msg)
    except Exception as e:
        err_msg = f'Error: Error with {inspect.currentframe().f_code.co_name}: {str(e)}'
        raise KepError(err_msg)
    return url

def add_tag_group(server: server, adv_tag_group_path: str, DATA: Union[dict, list]) -> Union[bool, list]:
    # TODO: confirm adding tag types in this folder
    # TODO: Do we need to require the tag group path if we are adding a tag group at the root? (i.e. _advancedtags)
    '''Add a `"tag group"` or multiple `"tag group"` objects to a device in Kepware. Can be used to pass children of a tag group object 
    such as tags. This allows you to create a tag group and tags 
    all in one function, if desired.

    Additionally it can be used to pass a list of tag groups and its children to be added all at once.

    :param server: instance of the `server` class
    :param adv_tag_group_path: path identifying tag group to add the tag group object(s). Standard Kepware address decimal 
    notation string such as "_advancedtags.AdvTagGroup1" or "_advancedtags.AdvTagGroup1.AdvTagGroupChild"
    :param DATA: Dict or List of Dicts of the tag group(s) and its children
    expected by Kepware Configuration API
    
    :return: True - If a "HTTP 201 - Created" is received from Kepware server
    :return: If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    tag groups added that failed.

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    path_obj = adv_tags._adv_tag_path_split(adv_tag_group_path, isItem=False)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _create_url()
    
    r = server._config_add(url, DATA)
    if r.code == 201: return True
    elif r.code == 207:
        errors = []
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else:
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def del_tag_group(server: server, adv_tag_group_path: str) -> bool:
    '''Delete a `"tag group"` object in Kepware. This will delete all children as well.

    :param server: instance of the `server` class
    :param adv_tag_group_path: path identifying tag group to delete. Standard Kepware address decimal 
    notation string such as "_advancedtags.AdvTagGroup1" or "_advancedtags.AdvTagGroup1.AdvTagGroupChild"

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    # url = _create_url(server.url, adv_tag_group_path, isItem=True)
    path_obj = adv_tags._adv_tag_path_split(adv_tag_group_path, isItem=True)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _create_url(path_obj['item'])
    r = server._config_del(url)
    if r.code == 200: return True
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_tag_group(server: server, adv_tag_group_path: str, DATA: dict, force: bool = False) -> bool:
    '''Modify a tag group object and its properties in Kepware.

    :param server: instance of the `server` class
    :param adv_tag_group_path: path identifying the advanced tag group to modify. Standard Kepware address decimal 
    notation string such as "_advancedtags.AdvTagGroup1" or "_advancedtags.AdvTagGroup1.AdvTagGroupChild"
    :param DATA: Dict of the advanced tag group properties to be modified
    :param force: *(optional)* if True, will force the configuration update to the Kepware server
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    tag_group_data = server._force_update_check(force, DATA)
    path_obj = adv_tags._adv_tag_path_split(adv_tag_group_path, isItem=True)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _create_url(path_obj['item'])

    r = server._config_update(url, tag_group_data)
    if r.code == 200: return True
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_tag_group(server: server, adv_tag_group_path: str) -> dict:
    '''Returns the properties of the tag group object.

    :param server: instance of the `server` class
    :param adv_tag_group_path: path identifying the advanced tag group to retrieve. Standard Kepware address decimal
    notation string such as "_advancedtags.AdvTagGroup1" or "_advancedtags.AdvTagGroup1.AdvTagGroupChild"

    :return: Dict of data for the tag group requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    path_obj = adv_tags._adv_tag_path_split(adv_tag_group_path, isItem=True)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _create_url(path_obj['item'])
    r = server._config_get(url)
    return r.payload

def get_all_tag_groups(server: server, adv_tag_group_path: str, *, options: dict = None) -> list:
    '''Returns list of all tag group objects and their properties within a tag group. Returned object is JSON list.
    
    :param server: instance of the `server` class
    :param adv_tag_group_path: path identifying the advanced tag group collection to retrieve. Standard Kepware address decimal
    notation string such as "_advancedtags.AdvTagGroup1" or "_advancedtags.AdvTagGroup1.AdvTagGroupChild"

    :return: List of data for all tag groups within the tag group

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    path_obj = adv_tags._adv_tag_path_split(adv_tag_group_path, isItem=True)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _create_url()
    r = server._config_get(url, params=options)
    return r.payload
