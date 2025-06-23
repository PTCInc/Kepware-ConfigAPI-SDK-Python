# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`maximum_tags` exposes an API to allow modifications (add, delete, modify) to 
maximum tag objects within the Kepware Configuration API
"""

from ..connection import server
from ..error import KepError, KepHTTPError
from ..utils import _url_parse_object
from typing import Union
from .. import adv_tags

MAXIMUM_TAGS_ROOT = '/maximum_tags'

def _get_maximum_tags_url(tag: str = None) -> str:
    '''Creates url object for the "maximum_tags" branch of Kepware's project tree.
    
    Returns the maximum tag specific url when a value is passed as the tag name.
    '''
    if tag is None:
        return MAXIMUM_TAGS_ROOT
    else:
        return f'{MAXIMUM_TAGS_ROOT}/{_url_parse_object(tag)}'

def add_maximum_tag(server: server, adv_tag_group_path: str, DATA: Union[dict, list]) -> Union[bool, list]:
    '''Add `"maximum_tag"` or multiple `"maximum_tag"` objects to a specific path in Kepware.
    Can be used to pass a list of maximum tags to be added at one path location.

    :param server: instance of the `server` class
    :param adv_tag_group_path: path identifying where to add maximum tag(s). Standard Kepware address decimal 
    notation string such as "_advancedtags.AdvTagGroup1" or "_advancedtags.AdvTagGroup1.AdvTagGroupChild"
    :param DATA: Dict or List of Dicts of the maximum tag(s) to add

    :return: True - If a "HTTP 201 - Created" is received from Kepware server
    :return: If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    maximum tags added that failed.

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    path_obj = adv_tags.adv_tag_path_split(adv_tag_group_path, isItem=False)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _get_maximum_tags_url()

    r = server._config_add(url, DATA)
    if r.code == 201:
        return True
    elif r.code == 207:
        errors = [item for item in r.payload if item['code'] != 201]
        return errors
    else:
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_maximum_tag(server: server, max_tag_path: str, DATA: dict, force: bool = False) -> bool:
    '''Modify a `"maximum_tag"` object and its properties in Kepware.

    :param server: instance of the `server` class
    :param max_tag_path: path identifying location and maximum tag to modify. Standard Kepware address decimal 
    notation string including the maximum tag such as "_advancedtags.AdvTagGroup1.MaxTag1"
    :param DATA: Dict of the `maximum_tag` properties to be modified
    :param force: *(optional)* if True, will force the configuration update to the Kepware server

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    max_tag_data = server._force_update_check(force, DATA)
    path_obj = adv_tags.adv_tag_path_split(max_tag_path, isItem=True)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _get_maximum_tags_url(path_obj['item'])

    r = server._config_update(url, max_tag_data)
    if r.code == 200:
        return True
    else:
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def del_maximum_tag(server: server, max_tag_path: str) -> bool:
    '''Delete `"maximum_tag"` object at a specific path in Kepware.

    :param server: instance of the `server` class
    :param max_tag_path: path identifying location and maximum tag to delete. Standard Kepware address decimal 
    notation string including the maximum tag such as "_advancedtags.AdvTagGroup1.MaxTag1"

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    path_obj = adv_tags.adv_tag_path_split(max_tag_path, isItem=True)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _get_maximum_tags_url(path_obj['item'])

    r = server._config_del(url)
    if r.code == 200:
        return True
    else:
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_maximum_tag(server: server, max_tag_path: str) -> dict:
    '''Returns the properties of the `"maximum_tag"` object at a specific path in Kepware.

    :param server: instance of the `server` class
    :param max_tag_path: path identifying location and maximum tag to retrieve. Standard Kepware address decimal 
    notation string including the maximum tag such as "_advancedtags.AdvTagGroup1.MaxTag1"

    :return: Dict of data for the maximum tag requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    path_obj = adv_tags.adv_tag_path_split(max_tag_path, isItem=True)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _get_maximum_tags_url(path_obj['item'])

    r = server._config_get(url)
    return r.payload

def get_all_maximum_tags(server: server, adv_tag_group_path: str, *, options: dict = None) -> list:
    '''Returns the properties of all `"maximum_tag"` objects at a specific path in Kepware.

    :param server: instance of the `server` class
    :param adv_tag_group_path: path identifying location to retrieve maximum tag list. Standard Kepware address decimal
    notation string such as "_advancedtags.AdvTagGroup1" or "_advancedtags.AdvTagGroup1.AdvTagGroupChild"
    :param options: *(optional)* Dict of parameters to filter, sort or paginate the list of maximum tags. Options are `filter`,
        `sortOrder`, `sortProperty`, `pageNumber`, and `pageSize`

    :return: List of data for all maximum tags

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    path_obj = adv_tags.adv_tag_path_split(adv_tag_group_path, isItem=False)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _get_maximum_tags_url()

    r = server._config_get(url, params=options)
    return r.payload