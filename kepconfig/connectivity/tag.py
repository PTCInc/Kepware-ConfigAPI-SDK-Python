# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


r"""`tag` exposes an API to allow modifications (add, delete, modify) to 
tag and tag group objects within the Kepware Configuration API
"""

from ..error import KepError, KepHTTPError
from typing import Union
import kepconfig
from . import channel, device
import inspect

TAGS_ROOT = '/tags'
TAG_GRP_ROOT = '/tag_groups'

def _create_tags_url(tag = None):
    '''Creates url object for the "tags" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure
    
    Returns the tag specific url when a value is passed as the tag name.
    '''
    if tag == None:
        return TAGS_ROOT
    else: 
        return '{}/{}'.format(TAGS_ROOT,tag)

def _create_tag_groups_url(tag_group = None):
    '''Creates url object for the "tag_group" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure
    
    Returns the tag group specific url when a value is passed as the tag group name.
    '''
    if tag_group == None:
        return TAG_GRP_ROOT
    else: 
        return '{}/{}'.format(TAG_GRP_ROOT,tag_group)

def add_tag(server, tag_path, DATA) -> Union[bool, list]:
    '''Add "tag" objects to a specific path in Kepware. To be used to 
    pass a list of tags to be added at one path location.

    INPUTS:
    "server" - instance of the "server" class
    
    "tag_path" -  path identifying location to add tags. Standard Kepware address decimal 
    notation string such as "channel1.device1.tag_group1"
    
    "DATA" - properly JSON object (dict) of the tags 
    expected by Kepware Configuration API at the "tags" url

    RETURNS:
    True - If a "HTTP 201 - Created" is received from Kepware

    List  - If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    tags added that failed.

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    path_obj = kepconfig.path_split(tag_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        if 'tag_path' in path_obj:
            for tg in path_obj['tag_path']:
                url += _create_tag_groups_url(tag_group=tg)
        url += _create_tags_url()
    except KeyError as err:
        err_msg = 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
        raise KepError(err_msg)
    except Exception as e:
        err_msg = 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
        raise KepError(err_msg)
    r = server._config_add(url, DATA)
    if r.code == 201: return True 
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def add_tag_group(server, tag_group_path, DATA) -> Union[bool, list]:
    '''Add "tag_group" objects to a specific path in Kepware. To be used to 
    pass a list of tag_groups and children (tags or tag groups) to be added at one 
    path location.

    INPUTS:
    "server" - instance of the "server" class
    
    "tag_group_path" - path identifying location to add tag groups. Standard Kepware address decimal 
    notation string such as "channel1.device1.tag_group1"
    
    "DATA" - properly JSON object (dict) of the tag groups
    and it's children expected by Kepware Configuration API at the "tag_groups" url

    RETURNS:
    True - If a "HTTP 201 - Created" is received from Kepware

    List  - If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    tag groups added that failed.

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    path_obj = kepconfig.path_split(tag_group_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        if 'tag_path' in path_obj:
            for tg in path_obj['tag_path']:
                url += _create_tag_groups_url(tag_group=tg)
        url += _create_tag_groups_url()
    except KeyError as err:
        err_msg = 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
        raise KepError(err_msg)
    except Exception as e:
        err_msg = 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
        raise KepError(err_msg)
    r = server._config_add(url, DATA)
    if r.code == 201: return True 
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def add_all_tags(server, ch_dev_path, DATA) -> Union[bool, list]:
    '''Add "tag" and "tag group" objects to a device in Kepware. To be used to 
    pass a list of tags, tag groups and/or children of tag groups (tags and tag 
    groups) to be added at once.
    
    INPUTS:
    "server" - instance of the "server" class

    "ch_dev_path" - path to add tags and tag groups. Standard Kepware address decimal 
    notation string such as "channel1.device1"
    
    "DATA" - properly JSON object (dict) of the tags, 
    tag groups and it's children expected by Kepware Configuration API.
    
    RETURNS:
    True - If a "HTTP 201 - Created" is received from Kepware for all items

    List  - [tag failure list, tag group failure list] -   If a "HTTP 207 - Multi-Status" is received from 
    Kepware for either tags or tag groups, a list of dict error responses for all tags and/or tag groups added that failed. 

    False - If tags or tag groups are not found in DATA

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
######################################################
# Need to Handle HTTP 207 from the tag/tag group calls
######################################################
    
    tags_result = False
    tag_groups_result = False

    # check to see if there are dict entries for tags or tag groups
    if ('tag_groups' not in DATA) and ('tags' not in DATA):
        return False

    if 'tags' in DATA:
        tags_result = add_tag(server, ch_dev_path, DATA['tags'])
    if 'tag_groups' in DATA:
        #Add all Tag Groups
        tag_groups_result = add_tag_group(server, ch_dev_path, DATA['tag_groups'])
    
    # build results return from both calls
    if tags_result == True and tag_groups_result == True:
        return True
    elif tags_result == True:
        return [[], tag_groups_result]
    elif tag_groups_result == True:
        return [tags_result, []]
    else:
        # mixed results from both tags and tag groups
        return [tags_result, tag_groups_result]

def modify_tag(server, full_tag_path, DATA, force = False) -> bool:
    '''Modify a "tag" object and it's properties in Kepware.

    INPUTS:
    "server" - instance of the "server" class
    
    "full_tag_path" - path identifying location and tag to modify. Standard Kepware address decimal 
    notation string including the tag such as "channel1.device1.tag_group1.tag1"

    "DATA" - properly JSON object (dict) of the tag properties to be modified.

    "force" (optional) - if True, will force the configuration update to the Kepware server

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    tag_data = server._force_update_check(force, DATA)

    path_obj = kepconfig.path_split(full_tag_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        for x in range(0, len(path_obj['tag_path'])-1):
            url += _create_tag_groups_url(tag_group=path_obj['tag_path'][x])
        url += _create_tags_url(tag=path_obj['tag_path'][len(path_obj['tag_path'])-1])
    except KeyError as err:
        err_msg = 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
        raise KepError(err_msg)
    except Exception as e:
        err_msg = 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
        raise KepError(err_msg)
    r = server._config_update(url, tag_data)
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_tag_group(server, tag_group_path, DATA, force = False) -> bool:
    '''Modify a "tag group" object and it's properties in Kepware.

    INPUTS:
    "server" - instance of the "server" class
    
    "tag_group_path" - path identifying location and tag group to modify. Standard Kepware address decimal 
    notation string including the tag such as "channel1.device1.tag_group1"

    "DATA" is required to be a properly JSON object (dict) of the tag properties to be modified.

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    tag_group_data = server._force_update_check(force, DATA)

    path_obj = kepconfig.path_split(tag_group_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        for tg in path_obj['tag_path']:
            url += _create_tag_groups_url(tag_group=tg)
    except KeyError as err:
        err_msg = 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
        raise KepError(err_msg)
    except Exception as e:
        err_msg = 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
        raise KepError(err_msg)
    r = server._config_update(url, tag_group_data)
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def del_tag(server, full_tag_path) -> bool:
    '''Delete "tag" object at a specific path in Kepware.

    INPUTS:
    "server" - instance of the "server" class
    
    "full_tag_path" - path identifying location and tag to delete. Standard Kepware address decimal 
    notation string including the tag such as "channel1.device1.tag_group1.tag1"

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    path_obj = kepconfig.path_split(full_tag_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        for x in range(0, len(path_obj['tag_path'])-1):
            url += _create_tag_groups_url(tag_group=path_obj['tag_path'][x])
        url += _create_tags_url(tag=path_obj['tag_path'][len(path_obj['tag_path'])-1])
    except KeyError as err:
        err_msg = 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
        raise KepError(err_msg)
    except Exception as e:
        err_msg = 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
        raise KepError(err_msg)
    r = server._config_del(url)
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def del_tag_group(server, tag_group_path) -> bool:
    '''Delete "tag group" object at a specific path in Kepware.

    INPUTS:
    "server" - instance of the "server" class
    
    "tag_group_path" - path identifying location and tag group to delete. Standard Kepware address decimal 
    notation string such as "channel1.device1.tag_group1"

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    path_obj = kepconfig.path_split(tag_group_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        for tg in path_obj['tag_path']:
            url += _create_tag_groups_url(tag_group=tg)
    except KeyError as err:
        err_msg = 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
        raise KepError(err_msg)
    except Exception as err:
        err_msg = 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(err))
        raise KepError(err_msg)
    r = server._config_del(url)
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_tag(server, full_tag_path) -> dict:
    '''Returns the properties of the "tag" object at a specific path in Kepware. 
    Returned object is JSON. 

    INPUTS:
    "server" - instance of the "server" class
    
    "full_tag_path" - path identifying tag. Standard Kepware address decimal 
    notation string including the tag such as "channel1.device1.tag_group1.tag1"

    RETURNS:
    dict - data for the tag requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    path_obj = kepconfig.path_split(full_tag_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        for x in range(0, len(path_obj['tag_path'])-1):
            url += _create_tag_groups_url(tag_group=path_obj['tag_path'][x])
        url += _create_tags_url(tag=path_obj['tag_path'][len(path_obj['tag_path'])-1])
    except KeyError as err:
        err_msg = 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
        raise KepError(err_msg)
    except Exception as e:
        err_msg = 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
        raise KepError(err_msg)
    r = server._config_get(url)
    return r.payload

def get_all_tags(server, full_tag_path) -> list:
    '''Returns the properties of all "tag" object at a specific path in Kepware. 
    Returned object is JSON list.

    INPUTS:
    "server" - instance of the "server" class
    
    "full_tag_path" - path identifying location to retreive tag list. Standard Kepware address decimal 
    notation string including the tag such as "channel1.device1.tag_group1"
    
    RETURNS:
    list - data for the tags requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    path_obj = kepconfig.path_split(full_tag_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        if 'tag_path' in path_obj:
            for tg in path_obj['tag_path']:
                url += _create_tag_groups_url(tag_group=tg)
        url += _create_tags_url()
    except KeyError as err:
        err_msg = 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
        raise KepError(err_msg)
    except Exception as e:
        err_msg = 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
        raise KepError(err_msg)
    r = server._config_get(url)
    return r.payload

def get_tag_group(server, tag_group_path) -> dict:
    '''Returns the properties of the "tag group" object at a specific 
    path in Kepware. Returned object is JSON.

    INPUTS:
    "server" - instance of the "server" class 
    
    "tag_group_path" - path identifying tag group. Standard Kepware address decimal 
    notation string such as "channel1.device1.tag_group1"

    RETURNS:
    dict - data for the tag group requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    path_obj = kepconfig.path_split(tag_group_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        for tg in path_obj['tag_path']:
            url += _create_tag_groups_url(tag_group=tg)
    except KeyError as err:
        err_msg = 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
        raise KepError(err_msg)
    except Exception as e:
        err_msg = 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
        raise KepError(err_msg)
    r = server._config_get(url)
    return r.payload

def get_all_tag_groups(server, tag_group_path) -> list:
    '''Returns the properties of all "tag group" objects at a specific 
    path in Kepware. Returned object is JSON list. 

    INPUTS:
    "server" - instance of the "server" class
    
    "tag_group_path" - path identifying location to retreive tag group list. Standard Kepware address decimal 
    notation string such as "channel1.device1.tag_group1"

    RETURNS:
    list - data for the tag groups requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    path_obj = kepconfig.path_split(tag_group_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        if 'tag_path' in path_obj:
            for tg in path_obj['tag_path']:
                url += _create_tag_groups_url(tag_group=tg)
        url += _create_tag_groups_url()
    except KeyError as err:
        err_msg = 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
        raise KepError(err_msg)
    except Exception as e:
        err_msg = 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
        raise KepError(err_msg)
    r = server._config_get(url)
    return r.payload

def get_full_tag_structure(server, path, recursive = False) -> dict:
    '''Returns the properties of all "tag" and "tag group" objects at a specific 
    path in Kepware. Returned object is a dict of tag list and tag group list.

    Ex.
    {
        'tags': [tag1_dict, tag2_dict,...],
        'tag_groups':[tag_group1_dict, tag_group2_dict,...]
    } 

    If recursive is TRUE, then the call will iterate through all tag groups and get the tags and 
    tag groups of all tag group children.This would be the equivilant of asking for all tags and tag groups
    that exist below the "path" location. The returned object would look like below, nested based on how many 
    levels the tag_group namespace has tags or tag_groups:

    Ex.
    {
        'tags': [tag1_dict, tag2_dict,...],
        'tag_groups':[
            {
                tag_group1_properties,
                'tags': [tag1_dict, tag2_dict,...]
                'tag_groups':[sub_group1, subgroup2,...]
            }, 
            {
                tag_group2_properties,
                'tags': [tag1_dict, tag2_dict,...]
                'tag_groups':[sub_group1, subgroup2,...]
            },...]
    } 

    INPUTS:
    "server" - instance of the "server" class
    
    "path" - path identifying location to retreive the tag structure. Standard Kepware address decimal 
    notation string such as "channel1.device1.tag_group1" and must container at least the channel and device.

    RETURNS:
    dict - data for the tag structure requested at "path" location

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = {}
        
    r['tags'] = get_all_tags(server, path)
    r['tag_groups'] = get_all_tag_groups(server, path)
    if recursive:
        for group in r['tag_groups']:
            res = get_full_tag_structure(server, path + '.' + group['common.ALLTYPES_NAME'], recursive=recursive)
            group.update(res)
    return r
