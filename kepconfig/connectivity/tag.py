# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r""":mod:`tag` exposes an API to allow modifications (add, delete, modify) to 
tag and tag group objects within the Kepware Configuration API
"""

import kepconfig as helper
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
    
    "server" - instance of the "server" class

    "ch_dev_path" - path to add tags and tag groups. Standard Kepware address decimal 
    notation string such as "channel1.device1"
    
    "DATA" - properly JSON object (dict) of the tags, 
    tag groups and it's children expected by Kepware Configuration API.
    '''
    path_obj = helper.path_split(ch_dev_path)
    result = []
    if 'tags' in DATA:
        try:
            result.append(server._config_add(server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device']) +
                _create_tags_url(), DATA['tags']))
        except KeyError as err:
            return 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
        except Exception as e:
            return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    if 'tag_groups' in DATA:
        #Add all Tag Groups
        try:
            result.append(server._config_add(server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device']) +
                _create_tag_groups_url(), DATA['tag_groups']))
        except KeyError as err:
            return 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
        except Exception as e:
            return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    return result

def add_tag(server, tag_path, DATA):
    '''Add "tag" objects to a specific path in Kepware. To be used to 
    pass a list of tags to be added at one path location.

    "server" - instance of the "server" class
    
    "tag_path" -  path identifying location to add tags. Standard Kepware address decimal 
    notation string such as "channel1.device1.tag_group1"
    
    "DATA" - properly JSON object (dict) of the tags 
    expected by Kepware Configuration API at the "tags" url
    '''
    path_obj = helper.path_split(tag_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        if 'tag_path' in path_obj:
            for tg in path_obj['tag_path']:
                url += _create_tag_groups_url(tag_group=tg)
        url += _create_tags_url()
    except KeyError as err:
        return 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
    except Exception as e:
        return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    return server._config_add(url, DATA)

def add_tag_group(server, tag_group_path, DATA):
    '''Add "tag_group" objects to a specific path in Kepware. To be used to 
    pass a list of tag_groups and children (tags or tag groups) to be added at one 
    path location.

    "server" - instance of the "server" class
    
    "tag_group_path" - path identifying location to add tag groups. Standard Kepware address decimal 
    notation string such as "channel1.device1.tag_group1"
    
    "DATA" - properly JSON object (dict) of the tag groups
    and it's children expected by Kepware Configuration API at the "tag_groups" url
    '''
    path_obj = helper.path_split(tag_group_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        if 'tag_path' in path_obj:
            for tg in path_obj['tag_path']:
                url += _create_tag_groups_url(tag_group=tg)
        url += _create_tag_groups_url()
    except KeyError as err:
        return 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
    except Exception as e:
        return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    return server._config_add(url, DATA)

def modify_tag(server, full_tag_path, DATA, force = False):
    '''Modify a "tag" object and it's properties in Kepware.

    "server" - instance of the "server" class
    
    "full_tag_path" - path identifying location and tag to modify. Standard Kepware address decimal 
    notation string including the tag such as "channel1.device1.tag_group1.tag1"

    "DATA" - properly JSON object (dict) of the tag properties to be modified.

    "force" (optional) - if True, will force the configuration update to the Kepware server
    '''
    tag_data = server._force_update_check(force, DATA)

    path_obj = helper.path_split(full_tag_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        for x in range(0, len(path_obj['tag_path'])-1):
            url += _create_tag_groups_url(tag_group=path_obj['tag_path'][x])
        url += _create_tags_url(tag=path_obj['tag_path'][len(path_obj['tag_path'])-1])
    except KeyError as err:
        return 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
    except Exception as e:
        return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    return server._config_update(url, tag_data)

def modify_tag_group(server, tag_group_path, DATA, force = False):
    '''Modify a "tag group" object and it's properties in Kepware.

    "server" - instance of the "server" class
    
    "tag_group_path" - path identifying location and tag group to modify. Standard Kepware address decimal 
    notation string including the tag such as "channel1.device1.tag_group1"

    "DATA" is required to be a properly JSON object (dict) of the tag properties to be modified.
    '''

    tag_group_data = server._force_update_check(force, DATA)

    path_obj = helper.path_split(tag_group_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        for tg in path_obj['tag_path']:
            url += _create_tag_groups_url(tag_group=tg)
    except KeyError as err:
        return 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
    except Exception as e:
        return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    return server._config_update(url, tag_group_data)

def del_tag(server, full_tag_path):
    '''Delete "tag" object at a specific path in Kepware.

    "server" - instance of the "server" class
    
    "full_tag_path" - path identifying location and tag to delete. Standard Kepware address decimal 
    notation string including the tag such as "channel1.device1.tag_group1.tag1"
    '''
    path_obj = helper.path_split(full_tag_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        for x in range(0, len(path_obj['tag_path'])-1):
            url += _create_tag_groups_url(tag_group=path_obj['tag_path'][x])
        url += _create_tags_url(tag=path_obj['tag_path'][len(path_obj['tag_path'])-1])
    except KeyError as err:
        return 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
    except Exception as e:
        return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    return server._config_del(url)

def del_tag_group(server, tag_group_path):
    '''Delete "tag group" object at a specific path in Kepware.

    "server" - instance of the "server" class
    
    "tag_group_path" - path identifying location and tag group to delete. Standard Kepware address decimal 
    notation string such as "channel1.device1.tag_group1"
    '''
    path_obj = helper.path_split(tag_group_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        for tg in path_obj['tag_path']:
            url += _create_tag_groups_url(tag_group=tg)
    except KeyError as err:
        return 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
    except Exception as e:
        return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    return server._config_del(url)

def get_tag(server, full_tag_path):
    '''Returns the properties of the "tag" object at a specific path in Kepware. 
    Returned object is JSON. 

    "server" - instance of the "server" class
    
    "full_tag_path" - path identifying tag. Standard Kepware address decimal 
    notation string including the tag such as "channel1.device1.tag_group1.tag1"
    '''
    path_obj = helper.path_split(full_tag_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        for x in range(0, len(path_obj['tag_path'])-1):
            url += _create_tag_groups_url(tag_group=path_obj['tag_path'][x])
        url += _create_tags_url(tag=path_obj['tag_path'][len(path_obj['tag_path'])-1])
    except KeyError as err:
        return 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
    except Exception as e:
        return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    return server._config_get(url)

def get_all_tags(server, full_tag_path):
    '''Returns the properties of all "tag" object at a specific path in Kepware. 
    Returned object is JSON list.

    "server" - instance of the "server" class
    
    "full_tag_path" - path identifying location to retreive tag list. Standard Kepware address decimal 
    notation string including the tag such as "channel1.device1.tag_group1"
    '''
    path_obj = helper.path_split(full_tag_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        if 'tag_path' in path_obj:
            for tg in path_obj['tag_path']:
                url += _create_tag_groups_url(tag_group=tg)
        url += _create_tags_url()
    except KeyError as err:
        return 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
    except Exception as e:
        return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    return server._config_get(url)

def get_tag_group(server, tag_group_path):
    '''Returns the properties of the "tag group" object at a specific 
    path in Kepware. Returned object is JSON.

    "server" - instance of the "server" class 
    
    "tag_group_path" - path identifying tag group. Standard Kepware address decimal 
    notation string such as "channel1.device1.tag_group1"
    '''
    path_obj = helper.path_split(tag_group_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        for tg in path_obj['tag_path']:
            url += _create_tag_groups_url(tag_group=tg)
    except KeyError as err:
        return 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
    except Exception as e:
        return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    return server._config_get(url)

def get_all_tag_groups(server, tag_group_path):
    '''Returns the properties of all "tag group" objects at a specific 
    path in Kepware. Returned object is JSON list. 

    "server" - instance of the "server" class
    
    "tag_group_path" - path identifying location to retreive tag group list. Standard Kepware address decimal 
    notation string such as "channel1.device1.tag_group1"
    '''
    path_obj = helper.path_split(tag_group_path)
    try:
        url = server.url+channel._create_url(path_obj['channel'])+device._create_url(path_obj['device'])
        if 'tag_path' in path_obj:
            for tg in path_obj['tag_path']:
                url += _create_tag_groups_url(tag_group=tg)
        url += _create_tag_groups_url()
    except KeyError as err:
        return 'Error: No key {} identified | Function: {}'.format(err, inspect.currentframe().f_code.co_name)
    except Exception as e:
        return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    return server._config_get(url)