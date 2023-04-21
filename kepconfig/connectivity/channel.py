# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


r"""`channel` exposes an API to allow modifications (add, delete, modify) to 
channel objects within the Kepware Configuration API
"""

 
import inspect
from ..connection import server
from ..error import KepHTTPError, KepError
from typing import Union
from . import device

CHANNEL_ROOT = '/project/channels'

def _create_url(channel = None):
    '''Creates url object for the "channel" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the channel specific url when a value is passed as the channel name.
    '''
    
    if channel == None:
        return CHANNEL_ROOT
    else:
        return '{}/{}'.format(CHANNEL_ROOT,channel)

def add_channel(server: server, DATA: dict | list) -> Union[bool, list]:
    '''Add a `"channel"` or multiple `"channel"` objects to Kepware. Can be used to pass children of a channel object 
    such as devices and tags/tag groups. This allows you to create a channel, it's devices and tags 
    all in one function, if desired.

    Additionally it can be used to pass a list of channels and it's children to be added all at once.

    :param server: instance of the `server` class
    :param DATA: Dict of the channel and it's children
    expected by Kepware Configuration API

    :return: True - If a "HTTP 201 - Created" is received from Kepware server
    :return: If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    channels added that failed.

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_add(server.url + _create_url(), DATA)
    if r.code == 201: return True
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else: 
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def del_channel(server: server, channel: str) -> bool:
    '''Delete a `"channel"` object in Kepware. This will delete all children as well
    
    :param server: instance of the `server` class
    :param channel: name of channel
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_del(server.url + _create_url(channel))
    if r.code == 200: return True 
    else: 
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_channel(server: server, DATA: dict, *, channel: str = None, force: bool = False) -> bool:
    '''Modify a channel object and it's properties in Kepware. If a `"channel"` is not provided as an input,
    you need to identify the channel in the *'common.ALLTYPES_NAME'* property field in `"DATA"`. It will 
    assume that is the channel that is to be modified.

    :param server: instance of the `server` class
    :param DATA: Dict of the `channel` properties to be modified
    :param channel: *(optional)* - name of channel to modify. Only needed if not existing in `"DATA"`
    :param force: *(optional)* if True, will force the configuration update to the Kepware server
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    
    channel_data = server._force_update_check(force, DATA)
    if channel == None:
        try:
            r = server._config_update(server.url + _create_url(channel_data['common.ALLTYPES_NAME']), channel_data)
            if r.code == 200: return True 
            else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        except KeyError as err:
            err_msg = 'Error: No Channel identified in DATA | Key Error: {}'.format(err)
            raise KepError(err_msg)
        # except Exception as e:
        #     return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    else:
        r = server._config_update(server.url + _create_url(channel), channel_data)
        if r.code == 200: return True 
        else: 
            raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_channel(server: server, channel: str)  -> dict:
    '''Returns the properties of the channel object.
    
    :param server: instance of the `server` class
    :param channel: name of channel
    
    :return: Dict of data for the channel requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_get(server.url + _create_url(channel))
    return r.payload

def get_all_channels(server: server, *, options: dict = None) -> list:
    '''Returns list of all channel objects and their properties.
    
    :param server: instance of the `server` class
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of channels. Options are `filter`, 
        `sortOrder`, `sortProperty`, `pageNumber`, and `pageSize`
    
    :return: List of data for all channels in Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_get(server.url + _create_url(), params= options)
    return r.payload

def get_channel_structure(server: server, channel: str) -> dict:
    '''Returns the properties of `"channel"` and includes all `"devices"` and the `"tag"` and `"tag group"` objects for a 
    channel in Kepware. Returned object is a dict of channel properties including a device list with 
    tag lists and tag group lists.

    The returned object resembles the example below, nested based on how many 
    levels the tag_group namespace has tags or tag_groups:

    Example return:
    
        {
            channel_properties,
            'devices: [
                {
                    device1_properties,
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
                },...]
        }       

    :param server: instance of the `server` class
    :param channel: name of channel

    :return: Dict of data for the channel structure requested for `"channel"`

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    channel_properties = get_channel(server, channel)
    device_list = device.get_all_devices(server,channel)
    for dev in device_list:
        device_properties = []
        dev_struct = device.get_device_structure(server,channel + '.' + dev['common.ALLTYPES_NAME'])
        device_properties.append(dev_struct)
    return {**channel_properties,'device': device_properties}