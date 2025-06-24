# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Note: The code within this file was created in total or in part
#  with the use of AI tools.

r"""`derived_tags` exposes an API to allow modifications (add, delete, modify) to 
derived tag objects within the Kepware Configuration API
"""

from ..connection import server
from ..error import KepError, KepHTTPError
from ..utils import _url_parse_object
from typing import Union
from .. import adv_tags

DERIVED_TAGS_ROOT = '/derived_tags'

def _get_derived_tags_url(tag: str = None) -> str:
    '''Creates url object for the "derived_tags" branch of Kepware's project tree.
    
    Returns the derived tag specific url when a value is passed as the tag name.
    '''
    if tag is None:
        return DERIVED_TAGS_ROOT
    else:
        return f'{DERIVED_TAGS_ROOT}/{_url_parse_object(tag)}'

def add_derived_tag(server: server, adv_tag_group_path: str, DATA: Union[dict, list]) -> Union[bool, list]:
    '''Add `"derived_tag"` or multiple `"derived_tag"` objects to a specific path in Kepware.
    Can be used to pass a list of derived tags to be added at one path location.

    :param server: instance of the `server` class
    :param adv_tag_group_path: path identifying where to add derived tag(s). Standard Kepware address decimal 
    notation string such as "_advancedtags.AdvTagGroup1" or "_advancedtags.AdvTagGroup1.AdvTagGroupChild"
    :param DATA: Dict or List of Dicts of the derived tag(s) to add

    :return: True - If a "HTTP 201 - Created" is received from Kepware server
    :return: If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    derived tags added that failed.

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    path_obj = adv_tags._adv_tag_path_split(adv_tag_group_path, isItem=False)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _get_derived_tags_url()

    r = server._config_add(url, DATA)
    if r.code == 201:
        return True
    elif r.code == 207:
        errors = [item for item in r.payload if item['code'] != 201]
        return errors
    else:
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_derived_tag(server: server, derived_tag_path: str, DATA: dict, force: bool = False) -> bool:
    '''Modify a `"derived_tag"` object and its properties in Kepware.

    :param server: instance of the `server` class
    :param derived_tag_path: path identifying location and derived tag to modify. Standard Kepware address decimal 
    notation string including the derived tag such as "_advancedtags.AdvTagGroup1.DerivedTag1"
    :param DATA: Dict of the `derived_tag` properties to be modified
    :param force: *(optional)* if True, will force the configuration update to the Kepware server

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    derived_tag_data = server._force_update_check(force, DATA)
    path_obj = adv_tags._adv_tag_path_split(derived_tag_path, isItem=True)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _get_derived_tags_url(path_obj['item'])

    r = server._config_update(url, derived_tag_data)
    if r.code == 200:
        return True
    else:
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def del_derived_tag(server: server, derived_tag_path: str) -> bool:
    '''Delete `"derived_tag"` object at a specific path in Kepware.

    :param server: instance of the `server` class
    :param derived_tag_path: path identifying location and derived tag to delete. Standard Kepware address decimal 
    notation string including the derived tag such as "_advancedtags.AdvTagGroup1.DerivedTag1"

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    path_obj = adv_tags._adv_tag_path_split(derived_tag_path, isItem=True)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _get_derived_tags_url(path_obj['item'])

    r = server._config_del(url)
    if r.code == 200:
        return True
    else:
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_derived_tag(server: server, derived_tag_path: str) -> dict:
    '''Returns the properties of the `"derived_tag"` object at a specific path in Kepware.

    :param server: instance of the `server` class
    :param derived_tag_path: path identifying location and derived tag to retrieve. Standard Kepware address decimal 
    notation string including the derived tag such as "_advancedtags.AdvTagGroup1.DerivedTag1"

    :return: Dict of data for the derived tag requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    path_obj = adv_tags._adv_tag_path_split(derived_tag_path, isItem=True)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _get_derived_tags_url(path_obj['item'])

    r = server._config_get(url)
    return r.payload

def get_all_derived_tags(server: server, adv_tag_group_path: str, *, options: dict = None) -> list:
    '''Returns the properties of all `"derived_tag"` objects at a specific path in Kepware.

    :param server: instance of the `server` class
    :param adv_tag_group_path: path identifying location to retrieve derived tag list. Standard Kepware address decimal
    notation string such as "_advancedtags.AdvTagGroup1" or "_advancedtags.AdvTagGroup1.AdvTagGroupChild"
    :param options: *(optional)* Dict of parameters to filter, sort or paginate the list of derived tags. Options are `filter`,
        `sortOrder`, `sortProperty`, `pageNumber`, and `pageSize`

    :return: List of data for all derived tags

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    path_obj = adv_tags._adv_tag_path_split(adv_tag_group_path, isItem=False)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _get_derived_tags_url()

    r = server._config_get(url, params=options)
    return r.payload