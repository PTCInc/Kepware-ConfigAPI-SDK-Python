# -------------------------------------------------------------------------
# Copyright (c) 2020, PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r""":mod:`device` exposes an API to allow modifications (add, delete, modify) to 
device objects within the Kepware Configuration API
"""

import kepconfig
from . import channel
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

def add_device(server, dev_channel, DATA):
    '''Add a "device" object to a channel in Kepware. Can be used to pass children of a device object 
    such as tags and tag groups. This allows you to create a device and tags 
    all in one function, if desired.

    Additionally it can be used to pass a list of channelsdevices and it's children to be added all at once.

    INPUTS:
    "server" - instance of the "server" class

    "dev_channel" - channel the device object exists

    "DATA" - properly JSON object (dict) of the device and it's children 
    expected by Kepware Configuration API
    
    RETURNS:
    True - If a "HTTP 201 - Created" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_add(server.url + channel._create_url(dev_channel) + _create_url(), DATA)
    if r.code == 201: return True 
    else: return False

def del_device(server, device_path):
    '''Delete a "device" object in Kepware. This will delete all children as well.

    INPUTS:
    "server" - instance of the "server" class

    "device_path" - path identifying device to delete. Standard Kepware address decimal notation string including the 
    device such as "channel1.device1"

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    path_obj = kepconfig.path_split(device_path)
    try:
        r = server._config_del(server.url + channel._create_url(path_obj['channel']) + _create_url(path_obj['device']))
        if r.code == 200: return True 
        else: return False
    except KeyError as err:
        print('Error: No {} identified in {} | Function: {}'.format(err,'device_path', inspect.currentframe().f_code.co_name))
        return False

def modify_device(server, device_path, DATA, force = False):
    '''Modify a device object and it's properties in Kepware.

    INPUTS:
    "server" - instance of the "server" class

    "device_path" -  path identifying device to modify. Standard Kepware address decimal notation string including the 
    device such as "channel1.device1"

    "DATA" - properly JSON object (dict) of the device properties to be modified.

    "force" (optional) - if True, will force the configuration update to the Kepware server
    
    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    device_data = server._force_update_check(force, DATA)

    path_obj = kepconfig.path_split(device_path)
    try:
        r = server._config_update(server.url + channel._create_url(path_obj['channel']) + _create_url(path_obj['device']), device_data)
        if r.code == 200: return True 
        else: return False
    except KeyError as err:
            print('Error: No {} identified in {} | Function: {}'.format(err,'device_path', inspect.currentframe().f_code.co_name))
            return False
    # except Exception as e:
    #     return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))

def get_device(server, device_path):
    '''Returns the properties of the device object. Returned object is JSON.

    INPUTS:
    "server" - instance of the "server" class
    
    "device_path" -  path identifying device. Standard Kepware address decimal notation string including the 
    device such as "channel1.device1"

    RETURNS:
    JSON - data for the device requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    path_obj = kepconfig.path_split(device_path)
    try:
        r = server._config_get(server.url + channel._create_url(path_obj['channel']) + _create_url(path_obj['device']))
        return r.payload
    except KeyError as err:
        print('Error: No {} identified in {} | Function: {}'.format(err,'device_path', inspect.currentframe().f_code.co_name))
        return False
    # except Exception as err:
    #     print('Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(err)))
    #     raise err

def get_all_devices(server, dev_channel):
    '''Returns list of all device objects and their properties within a channel. Returned object is JSON list.
    
    INPUTS:
    "dev_channel" - channel the device object exists

    RETURNS:
    JSON - data for the devices requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_get(server.url + channel._create_url(dev_channel) + _create_url())
    return r.payload

def auto_tag_gen(server, device_path):
    '''Executes Auto Tag Generation function on devices that support the feature in Kepware
    
    INPUTS:
    "server" - instance of the "server" class
    
    "device_path" -  path identifying device. Standard Kepware address decimal notation string including the 
    device such as "channel1.device1"

    RETURNS:
    KepServiceReturn with the result of the service either Code 202 (Accepted) or 429 (Too Busy)

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    
    path_obj = kepconfig.path_split(device_path)
    try:
        r = server._config_update(server.url +channel._create_url(path_obj['channel']) + _create_url(path_obj['device']) + ATG_URL)
        job = kepconfig.connection.KepServiceResponse(r.payload['code'],r.payload['message'], r.payload['href'])
        return job
    except KeyError as err:
        print('Error: No {} identified in {} | Function: {}'.format(err,'device_path', inspect.currentframe().f_code.co_name))
        return False
    except kepconfig.error.KepHTTPError as err:
        if err.code == 429:
            job.code = err.code
            job.message = err.payload
            return job
        else:
            raise err
    # except Exception as e:
    #     return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    