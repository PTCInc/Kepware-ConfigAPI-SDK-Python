# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


r"""`channel` exposes an API to allow modifications (add, delete, modify) to 
channel objects within the Kepware Configuration API
"""

 
import inspect
from typing import Union
from. import device

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

def add_channel(server, DATA) -> Union[bool, list]:
    '''Add a "channel" or multiple "channel" objects to Kepware. Can be used to pass children of a channel object 
    such as devices and tags/tag groups. This allows you to create a channel, it's devices and tags 
    all in one function, if desired.

    Additionally it can be used to pass a list of channels and it's children to be added all at once.

    INPUTS:
    "server" - instance of the "server" class

    "DATA" - properly JSON object (dict) of the channel and it's children
    expected by Kepware Configuration API

    RETURNS:
    True - If a "HTTP 201 - Created" is received from Kepware
    
    List - If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    channels added that failed.

    False - If a non-expected "2xx successful" code is returned
        

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_add(server.url + _create_url(), DATA)
    if r.code == 201: return True
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else: return False

def del_channel(server, channel):
    '''Delete a "channel" object in Kepware. This will delete all children as well
    
    INPUTS:
    "server" - instance of the "server" class

    "channel" - name of channel
    
    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_del(server.url + _create_url(channel))
    if r.code == 200: return True 
    else: return False

def modify_channel(server, DATA, channel = None, force = False):
    '''Modify a channel object and it's properties in Kepware. If a "channel" is not provided as an input,
    you need to identify the channel in the 'common.ALLTYPES_NAME' property field in the "DATA". It will 
    assume that is the channel that is to be modified.

    INPUTS:
    "server" - instance of the "server" class

    "DATA" - properly JSON object (dict) of the channel properties to be modified.

    "channel" (optional) - name of channel to modify. Only needed if not existing in  "DATA"

    "force" (optional) - if True, will force the configuration update to the Kepware server
    
    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    
    channel_data = server._force_update_check(force, DATA)
    if channel == None:
        try:
            r = server._config_update(server.url + _create_url(channel_data['common.ALLTYPES_NAME']), channel_data)
            if r.code == 200: return True 
            else: return False
        except KeyError as err:
            print('Error: No Channel identified in DATA | Key Error: {}'.format(err))
            return False
        # except Exception as e:
        #     return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    else:
        r = server._config_update(server.url + _create_url(channel), channel_data)
        if r.code == 200: return True 
        else: return False

def get_channel(server, channel):
    '''Returns the properties of the channel object. Returned object is JSON.
    
    INPUTS:
    "server" - instance of the "server" class

    "channel" - name of channel
    
    RETURNS:
    JSON - data for the channel requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_get(server.url + _create_url(channel))
    return r.payload

def get_all_channels(server):
    '''Returns list of all channel objects and their properties. Returned object is JSON list.
    
    INPUTS:
    "server" - instance of the "server" class
    
    RETURNS:
    JSON - data for the channel requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_get(server.url + _create_url())
    return r.payload

def get_channel_structure(server, channel):
    '''Returns the properties of "channel" and includes all "devices" and the "tag" and "tag group" objects for a 
    channel in Kepware. Returned object is a dict of channel properties including a device list with 
    tag lists and tag group lists.

    The returned object resembles below, nested based on how many 
    levels the tag_group namespace has tags or tag_groups:

    Ex.
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

    INPUTS:
    "server" - instance of the "server" class
    
    "channel" - name of channel

    RETURNS:
    dict - data for the device structure requested for "channel"
    FALSE - If the call fails

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    try:
        channel_properties = get_channel(server, channel)
        device_list = device.get_all_devices(server,channel)
        if type(device_list) is not list or type(channel_properties) is not dict:
            return False
        else:
            for dev in device_list:
                device_properties = []
                dev_struct = device.get_device_structure(server,channel + '.' + dev['common.ALLTYPES_NAME'])
                if type(dev_struct) is dict:
                    device_properties.append(dev_struct)
                else:
                    return False
            return {**channel_properties,'device': device_properties}
    except Exception as err:
        # pass on exceptions
        raise err