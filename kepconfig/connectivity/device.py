# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


r"""`device` exposes an API to allow modifications (add, delete, modify) to 
device objects within the Kepware Configuration API
"""

from ..connection import KepServiceResponse, server
from ..error import KepHTTPError, KepError
from typing import Union
import kepconfig
from . import channel, tag
import inspect

DEVICE_ROOT = '/devices'
ATG_URL = '/services/TagGeneration'

def _create_url(device = None):
    '''Creates url object for the "device" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure
    
    Returns the device specific url when a value is passed as the device name.
    '''
    if device == None:
        return DEVICE_ROOT
    else:
        return '{}/{}'.format(DEVICE_ROOT,device)

def add_device(server: server, channel_name: str, DATA: dict | list) -> Union[bool, list]:
    '''Add a `"device"` or multiple `"device"` objects to a channel in Kepware. Can be used to pass children of a device object 
    such as tags and tag groups. This allows you to create a device and tags 
    all in one function, if desired.

    Additionally it can be used to pass a list of devices and it's children to be added all at once.

    :param server: instance of the `server` class
    :param channel_name: channel to add the device object(s)
    :param DATA: Dict or List of Dicts of the device(s) and it's children
    expected by Kepware Configuration API
    
    :return: True - If a "HTTP 201 - Created" is received from Kepware server
    :return: If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    devices added that failed.

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_add(server.url + channel._create_url(channel_name) + _create_url(), DATA)
    if r.code == 201: return True
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else: 
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def del_device(server: server, device_path: str) -> bool:
    '''Delete a `"device"` object in Kepware. This will delete all children as well.

    :param server: instance of the `server` class
    :param device_path: path identifying device to delete. Standard Kepware address decimal notation string including the 
    device such as `"channel1.device1"`

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    path_obj = kepconfig.path_split(device_path)
    try:
        r = server._config_del(server.url + channel._create_url(path_obj['channel']) + _create_url(path_obj['device']))
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
    except KeyError as err:
        err_msg = 'Error: No {} identified in {} | Function: {}'.format(err,'device_path', inspect.currentframe().f_code.co_name)
        raise KepError(err_msg)

def modify_device(server: server, device_path: str, DATA: dict, *, force: bool = False) -> bool:
    '''Modify a device object and it's properties in Kepware.

    :param server: instance of the `server` class
    :param device_path: path identifying device to modffy. Standard Kepware address decimal notation string including the 
    device such as `"channel1.device1"`
    :param DATA: Dict of the `device` properties to be modified
    :param force: *(optional)* if True, will force the configuration update to the Kepware server
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    device_data = server._force_update_check(force, DATA)

    path_obj = kepconfig.path_split(device_path)
    try:
        r = server._config_update(server.url + channel._create_url(path_obj['channel']) + _create_url(path_obj['device']), device_data)
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
    except KeyError as err:
            err_msg = 'Error: No {} identified in {} | Function: {}'.format(err,'device_path', inspect.currentframe().f_code.co_name)
            raise KepError(err_msg)

def get_device(server: server, device_path: str) -> dict:
    '''Returns the properties of the device object.

    :param server: instance of the `server` class
    :param device_path: path identifying device to retrieve properties. Standard Kepware address decimal notation string including the 
    device such as `"channel1.device1"`

    :return: Dict of data for the device requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    path_obj = kepconfig.path_split(device_path)
    try:
        r = server._config_get(server.url + channel._create_url(path_obj['channel']) + _create_url(path_obj['device']))
        return r.payload
    except KeyError as err:
        err_msg = 'Error: No {} identified in {} | Function: {}'.format(err,'device_path', inspect.currentframe().f_code.co_name)
        raise KepError(err_msg)
    # except Exception as err:
    #     print('Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(err)))
    #     raise err

def get_all_devices(server: server, channel_name: str, *, options: dict = None) -> list:
    '''Returns list of all device objects and their properties within a channel. Returned object is JSON list.
    
    :param server: instance of the `server` class
    :param channel: name of channel
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of devices. Options are `filter`, 
        `sortOrder`, `sortProperty`, `pageNumber`, and `pageSize`

    :return: List of data for all devices within the channel

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(f'{server.url}{channel._create_url(channel_name)}{_create_url()}', params= options)
    return r.payload

def auto_tag_gen(server: server, device_path: str, job_ttl: int = None) -> KepServiceResponse:
    '''Executes Auto Tag Generation function on devices that support the feature in Kepware
    
    :param server: instance of the `server` class
    :param device_path: path identifying device to modffy. Standard Kepware address decimal notation string including the 
    device such as `"channel1.device1"`

    :param job_ttl: *(optional)* Determines the number of seconds a job instance will exist following completion.

    :return: `KepServiceResponse` instance with job information
    
    :raises KepHTTPError: If urllib provides an HTTPError (If not HTTP code 202 [Accepted] or 429 [Too Busy] returned)
    :raises KepURLError: If urllib provides an URLError
    '''
    
    path_obj = kepconfig.path_split(device_path)
    try:
        url = server.url +channel._create_url(path_obj['channel']) + _create_url(path_obj['device']) + ATG_URL
        job = server._kep_service_execute(url, None, job_ttl)
        return job
    except KeyError as err:
        err_msg = 'Error: No {} identified in {} | Function: {}'.format(err,'device_path', inspect.currentframe().f_code.co_name)
        raise KepError(err_msg)

def get_all_tags_tag_groups(server: server, device_path: str) -> dict:
    '''Returns the properties of all `"tag"` and `"tag group"` objects for as specific
    device in Kepware. Returned object is a dict of tag list and tag group list.

    The returned object resembles the example below, nested based on how many 
    levels the tag_group namespace has tags or tag_groups:

    Example return:

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

    :param server: instance of the `server` class
    :param device_path: path identifying device to modffy. Standard Kepware address decimal notation string including the 
    device such as `"channel1.device1"`

    :return: Dict of data for the tag structure for device requested at `"device_path"` location

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = tag.get_full_tag_structure(server, device_path,recursive=True)
    return r

def get_device_structure(server, device_path) -> dict:
    '''Returns the properties of `"device"` and includes all `"tag"` and `"tag group"` objects for as specific
    device in Kepware. Returned object is a dict of device properties including a tag list and tag group list.

    The returned object resembles example below, nested based on how many 
    levels the tag_group namespace has tags or tag_groups:

    Example return:
    
        {
            device_properties,
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

    :param server: instance of the `server` class
    :param device_path: path identifying device to modffy. Standard Kepware address decimal notation string including the 
    device such as `"channel1.device1"`

    :return: Dict of data for the device structure at `"device_path"` location

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    tags = tag.get_full_tag_structure(server, device_path,recursive=True)
    device_properties = get_device(server,device_path)
    return {**device_properties, **tags}
