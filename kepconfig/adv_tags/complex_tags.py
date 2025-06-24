# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Note: The code within this file was created in total or in part
#  with the use of AI tools.

r"""`complex_tags` exposes an API to allow modifications (add, delete, modify) to 
complex tag objects within the Kepware Configuration API
"""

from ..connection import server
from ..error import KepError, KepHTTPError
from ..utils import _url_parse_object
from typing import Union
from .. import adv_tags

COMPLEX_TAGS_ROOT = '/complex_tags'

def _get_complex_tags_url(tag: str = None) -> str:
    '''Creates url object for the "complex_tags" branch of Kepware's project tree.
    
    Returns the complex tag specific url when a value is passed as the tag name.
    '''
    if tag is None:
        return COMPLEX_TAGS_ROOT
    else:
        return f'{COMPLEX_TAGS_ROOT}/{_url_parse_object(tag)}'

def add_complex_tag(server: server, adv_tag_group_path: str, DATA: Union[dict, list]) -> Union[bool, list]:
    '''Add `"complex_tag"` or multiple `"complex_tag"` objects to a specific path in Kepware.
    Can be used to pass a list of complex tags to be added at one path location.

    :param server: instance of the `server` class
    :param adv_tag_group_path: path identifying where to add complex tag(s). Standard Kepware address decimal 
    notation string such as "_advancedtags.AdvTagGroup1" or "_advancedtags.AdvTagGroup1.AdvTagGroupChild"
    :param DATA: Dict or List of Dicts of the complex tag(s) to add

    :return: True - If a "HTTP 201 - Created" is received from Kepware server
    :return: If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    complex tags added that failed.

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    path_obj = adv_tags._adv_tag_path_split(adv_tag_group_path, isItem=False)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _get_complex_tags_url()

    r = server._config_add(url, DATA)
    if r.code == 201:
        return True
    elif r.code == 207:
        errors = [item for item in r.payload if item['code'] != 201]
        return errors
    else:
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_complex_tag(server: server, complex_tag_path: str, DATA: dict, force: bool = False) -> bool:
    '''Modify a `"complex_tag"` object and its properties in Kepware.

    :param server: instance of the `server` class
    :param complex_tag_path: path identifying location and complex tag to modify. Standard Kepware address decimal 
    notation string including the complex tag such as "_advancedtags.AdvTagGroup1.ComplexTag1"
    :param DATA: Dict of the `complex_tag` properties to be modified
    :param force: *(optional)* if True, will force the configuration update to the Kepware server

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    complex_tag_data = server._force_update_check(force, DATA)
    path_obj = adv_tags._adv_tag_path_split(complex_tag_path, isItem=True)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _get_complex_tags_url(path_obj['item'])

    r = server._config_update(url, complex_tag_data)
    if r.code == 200:
        return True
    else:
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def del_complex_tag(server: server, complex_tag_path: str) -> bool:
    '''Delete `"complex_tag"` object at a specific path in Kepware.

    :param server: instance of the `server` class
    :param complex_tag_path: path identifying location and complex tag to delete. Standard Kepware address decimal 
    notation string including the complex tag such as "_advancedtags.AdvTagGroup1.ComplexTag1"

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    path_obj = adv_tags._adv_tag_path_split(complex_tag_path, isItem=True)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _get_complex_tags_url(path_obj['item'])

    r = server._config_del(url)
    if r.code == 200:
        return True
    else:
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_complex_tag(server: server, complex_tag_path: str) -> dict:
    '''Returns the properties of the `"complex_tag"` object at a specific path in Kepware.

    :param server: instance of the `server` class
    :param complex_tag_path: path identifying location and complex tag to retrieve. Standard Kepware address decimal 
    notation string including the complex tag such as "_advancedtags.AdvTagGroup1.ComplexTag1"

    :return: Dict of data for the complex tag requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    path_obj = adv_tags._adv_tag_path_split(complex_tag_path, isItem=True)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _get_complex_tags_url(path_obj['item'])

    r = server._config_get(url)
    return r.payload

def get_all_complex_tags(server: server, adv_tag_group_path: str, *, options: dict = None) -> list:
    '''Returns the properties of all `"complex_tag"` objects at a specific path in Kepware.

    :param server: instance of the `server` class
    :param adv_tag_group_path: path identifying location to retrieve complex tag list. Standard Kepware address decimal
    notation string such as "_advancedtags.AdvTagGroup1" or "_advancedtags.AdvTagGroup1.AdvTagGroupChild"
    :param options: *(optional)* Dict of parameters to filter, sort or paginate the list of complex tags. Options are `filter`,
        `sortOrder`, `sortProperty`, `pageNumber`, and `pageSize`

    :return: List of data for all complex tags

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    path_obj = adv_tags._adv_tag_path_split(adv_tag_group_path, isItem=False)
    url = adv_tags._create_adv_tags_base_url(server.url, path_obj) + _get_complex_tags_url()

    r = server._config_get(url, params=options)
    return r.payload