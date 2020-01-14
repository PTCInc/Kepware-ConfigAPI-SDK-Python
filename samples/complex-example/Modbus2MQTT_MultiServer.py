# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Complex Example (Modbus2MQTT_MultiServer) - Complex example of pulling device and tag information
# from a csv file and building out the Connectivity for each MODBUS PLC and modeling an MQTT Agent 
# each device to publish to a broker
# 
#  Name:
#       Modbus2MQTT_MultiDeployment.py
# 
#
#  Procedure:
#       Read in setup file
#       Read in agent/chan/device/tag template
#       Read in CSV, convert to json
#       Create JSON for channel, devices tags found in CSV
#       Create JSON for iot gateway mqtt agent for each device found in CSV
#       Create the connectivity and MQTT Agents in each kepware IP Addresses within the setup.json file
#
# ******************************************************************************/

import csv
import json
import kepconfig
from kepconfig.connectivity import channel, device, tag
import kepconfig.iot_gateway as IoT

def HTTPErrorHandler(err):
    # Generic Handler for exception errors
    if err.__class__ is kepconfig.error.KepHTTPError:
        print(err.code)
        print(err.msg)
        print(err.url)
        print(err.hdrs)
        print(err.payload)
    else:
        print('Different Exception Received')

def get_parameters(setup_file):
    try:
        print("Loading 'setup.json' from local directory")
        with open(setup_file) as j:
            setup_data = json.load(j)
            print("-- Load succeeded")
        return setup_data
    except Exception as e:
        print("-- Load setup failed - '{}'".format(e))
        return False


def convert_csv_to_json(path):
    try:
        print("Converting CSV at '{}' into JSON".format(path))
        csv_file = open(path, 'r')
        reader = csv.DictReader(csv_file)
        out = json.dumps([row for row in reader])
        json_from_csv = json.loads(out)
        print("-- Conversion succeeded")
        return json_from_csv
    except Exception as e:
        print("-- Conversion failed - '{}'".format (e))
        return False


def get_templates():
    try:
        print("Loading channel, device, and tag JSON template from local directory")
        c_template = open('./objs/channel.json')
        d_template = open('./objs/device.json')
        t_template = open('./objs/tag.json')
        a_template = open('./objs/agent.json')
        a_item_template = open('./objs/agent_item.json')
        chan = json.load(c_template)
        dev = json.load(d_template)
        tag = json.load(t_template)
        agent = json.load(a_template)
        a_item_template = json.load(a_item_template)
        print("-- Load succeeded")
        return chan, dev, tag, agent, a_item_template
    except Exception as e:
        print("-- Load failed - '{}'".format(e))
        return False


def get_unique_devices(master_list):
    try:
        print("Checking for unique devices in JSON from converted CSV")
        key = 'Device'
        seen = set()
        seen_add = seen.add
        unique_devices = [x for x in master_list if x[key] not in seen and not seen_add(x[key])]
        print("-- Check succeeded, unique devices gathered: {}".format(len(unique_devices)))
        return unique_devices
    except Exception as e:
        print("-- Load failed - '{}'".format(e))
        return False


def make_device(device, tchan, tdev, dev_limit):
    try:
        # Create channel JSON and add to the list
        name = device['Device']
        ip = device['Device_IP']
        ch_json = tchan.copy()
        dev_json = tdev.copy()
        ch_json['common.ALLTYPES_NAME'] = name

        #create the device JSON and add to the channel
        dev_json['common.ALLTYPES_NAME'] = name
        dev_json['servermain.DEVICE_ID_STRING'] = "<{}>.0".format(ip)
        ch_json['devices'] = []
        ch_json['devices'].append(dev_json)
        return ch_json

    except KeyError as err:
        print('Key Error: {}'.format(err))
        return False

def make_MQTT_agent(device, tagent, broker):
    try:
        name = device['Device']
        agent_json = tagent.copy()
        agent_json['common.ALLTYPES_NAME'] = name
        agent_json['iot_gateway.MQTT_CLIENT_URL'] = broker
        return agent_json
    except KeyError as err:
        print('Key Error: {}'.format(err))
        return False

def make_tags(master_list, device, ttag, limit, titem):
    try:
        add_tag = ttag.copy()
        add_iot_item = titem.copy()
        device_tag_list = []
        agent_tag_list = []
        
        # for each tag (item) present in converted CSV associated with the current device ID, build device tag and iot item tag reference ready for posting to Kepware
        for item in master_list:
            if item['Device'] == device['Device']:
                t_name = item['TagName']
                t_Address = item['Address']
                #5 = Word // 8 = float
                t_Type = item['DataType']
                add_tag['servermain.TAG_ADDRESS'] = t_Address
                add_tag['servermain.TAG_DATA_TYPE'] = int(t_Type)
                add_tag['common.ALLTYPES_NAME'] = t_name
                add_iot_item['iot_gateway.IOT_ITEM_SERVER_TAG'] = "{}.{}.{}".format(device['Device'], device['Device'], t_name)
                # add device tag and iot item tag references to lists
                agent_tag_list.append(add_iot_item.copy())
                device_tag_list.append(add_tag.copy())
            else:
                pass
        return device_tag_list, agent_tag_list
    except Exception as e:
        print ("-- Device tag and iot item reference creation failed - '{}'".format (e))
        return False

if __name__ == "__main__":
      
    # load setup parameters
    setupFilePath = 'setup.json'
    setupData = get_parameters(setupFilePath)

    # assign global variables
    user = setupData['configApiUsername']
    passw = setupData['configApiPassword']
    Kepware_IP_Array = setupData['Kepware_IP_Array']
    Kepware_Port = setupData['Kepware_Port']
    MQTT_broker = setupData['Broker_URL']

    # list to hold all channel, device and tag JSON to add to config
    all_devices_JSON = []
    all_agents_JSON = []

    # set limit of devices based on device-per-channel limit in Kepware
    device_limit = 128

    # get json templates for channel, device, and tag
    jChan, jDev, jTag, jAgent, jAgentItem = get_templates()

    # convert CSV file to JSON
    csv_file_path = setupData['path']
    masterList = convert_csv_to_json(csv_file_path)

    # obtain list of unique devices from converted csv
    uniqueDevices = get_unique_devices(masterList)

    print ("Creating Modbus channel, device, and tag structure")
    for device in uniqueDevices:
        # create device configuration JSON
        dev_JSON = make_device(device, jChan, jDev, device_limit)
        all_devices_JSON.append(dev_JSON)

        # create MQTT Agent JSON
        agent_JSON = make_MQTT_agent(device, jAgent, MQTT_broker)
        all_agents_JSON.append(agent_JSON)

        # add tags to devices and iot item references to agent
        dev_tags_JSON, agent_tags_JSON = make_tags(masterList, device, jTag, device_limit, jAgentItem)
        all_devices_JSON[-1]['devices'][-1]['tags'] = dev_tags_JSON
        all_agents_JSON[-1]['iot_items'] = agent_tags_JSON
    print ("-- Devices, tags IoT Agents and IoT item references created")
    
    print ("-- Channel and devices and agent creation attempt")
    for Kepware_IP in Kepware_IP_Array:
        server = kepconfig.connection.server(Kepware_IP, Kepware_Port, user, passw)
        try:
            print("{} - {}".format("Adding all devices", channel.add_channel(server,all_devices_JSON)))
        except Exception as err:
            HTTPErrorHandler(err)
        try:
            print("{} - {}".format("Adding all Agents", IoT.agent.add_iot_agent(server,all_agents_JSON,IoT.MQTT_CLIENT_AGENT)))
        except Exception as err:
            HTTPErrorHandler(err)
    print ("-- Channel and devices and agent creation completed")
