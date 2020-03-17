# -------------------------------------------------------------------------
# Copyright (c) 2020, PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


r""":mod:`tag` exposes an API to allow modifications (add, delete, modify) to 
tag and tag group objects within the Kepware Configuration API
"""

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

def add_all_tags(server, ch_dev_path, DATA):
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
    True - If a "HTTP 201 - Created" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    result = False
    if 'tags' in DATA:
        if (add_tag(server, ch_dev_path, DATA['tags'])):
            result = True
        else: 
            return False
    if 'tag_groups' in DATA:
        #Add all Tag Groups
        if (add_tag_group(server, ch_dev_path, DATA['tag_groups'])):
            result = True
        else:
            return False
    return result

def add_tag(server, tag_path, DATA):
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
        print('Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name))
        return False
    except Exception as e:
        print('Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e)))
        return False
    r = server._config_add(url, DATA)
    if r.code == 201: return True 
    else: return False

def add_tag_group(server, tag_group_path, DATA):
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
        print('Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name))
        return False
    except Exception as e:
        print('Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e)))
        return False
    r = server._config_add(url, DATA)
    if r.code == 201: return True 
    else: return False

def modify_tag(server, full_tag_path, DATA, force = False):
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
        print('Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name))
        return False
    except Exception as e:
        print('Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e)))
        return False
    r = server._config_update(url, tag_data)
    if r.code == 200: return True 
    else: return False

def modify_tag_group(server, tag_group_path, DATA, force = False):
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
        print('Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name))
        return False
    except Exception as e:
        print('Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e)))
        return False
    r = server._config_update(url, tag_group_data)
    if r.code == 200: return True 
    else: return False

def del_tag(server, full_tag_path):
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
        print('Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name))
        return False
    except Exception as e:
        print('Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e)))
        return False
    r = server._config_del(url)
    if r.code == 200: return True 
    else: return False

def del_tag_group(server, tag_group_path):
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
        print('Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name))
        return False
    except Exception as err:
        print('Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(err)))
        return False
    r = server._config_del(url)
    if r.code == 200: return True 
    else: return False

def get_tag(server, full_tag_path):
    '''Returns the properties of the "tag" object at a specific path in Kepware. 
    Returned object is JSON. 

    INPUTS:
    "server" - instance of the "server" class
    
    "full_tag_path" - path identifying tag. Standard Kepware address decimal 
    notation string including the tag such as "channel1.device1.tag_group1.tag1"

    RETURNS:
    JSON - data for the tag requested

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
        print('Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name))
        return False
    except Exception as e:
        print('Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e)))
        return False
    r = server._config_get(url)
    return r.payload

def get_all_tags(server, full_tag_path):
    '''Returns the properties of all "tag" object at a specific path in Kepware. 
    Returned object is JSON list.

    INPUTS:
    "server" - instance of the "server" class
    
    "full_tag_path" - path identifying location to retreive tag list. Standard Kepware address decimal 
    notation string including the tag such as "channel1.device1.tag_group1"
    
    RETURNS:
    JSON - data for the tags requested

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
        print('Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name))
        return False
    except Exception as e:
        print('Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e)))
        return False
    r = server._config_get(url)
    return r.payload

def get_tag_group(server, tag_group_path):
    '''Returns the properties of the "tag group" object at a specific 
    path in Kepware. Returned object is JSON.

    INPUTS:
    "server" - instance of the "server" class 
    
    "tag_group_path" - path identifying tag group. Standard Kepware address decimal 
    notation string such as "channel1.device1.tag_group1"

    RETURNS:
    JSON - data for the tag group requested

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
        print('Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name))
        return False
    except Exception as e:
        print('Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e)))
        return False
    r = server._config_get(url)
    return r.payload

def get_all_tag_groups(server, tag_group_path):
    '''Returns the properties of all "tag group" objects at a specific 
    path in Kepware. Returned object is JSON list. 

    INPUTS:
    "server" - instance of the "server" class
    
    "tag_group_path" - path identifying location to retreive tag group list. Standard Kepware address decimal 
    notation string such as "channel1.device1.tag_group1"

    RETURNS:
    JSON - data for the tag groups requested

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
        print('Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name))
        return False
    except Exception as e:
        print('Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e)))
        return False
    r = server._config_get(url)
    return r.payload