# ******************************************************************************
#  S. Elsner

#  Name:
#       auto_deploy
#
#  Procedure:
#       Read in setup file
#       Read in agent/chan/device/tag template
#       Read in CSV, convert to json
#       Push channel / iot gateway mqtt agent / devices found in CSV to Kepware
#       Create device tags and mqtt agent iot item references for each unique device and push to kepware
#
# ******************************************************************************/

import csv
import json
import requests


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
        print("-- Check succeeded, unique devices gathered")
        return unique_devices
    except Exception as e:
        print("-- Load failed - '{}'".format(e))
        return False


def make_devices(devices, tchan, tdev, tagent, dev_limit, user, passw):
    try:
        print ("Creating BACnet channel, unique gathered devices, and IoT Gateway MQTT agent")
        cname = tchan['common.ALLTYPES_NAME']
        tagent['common.ALLTYPES_NAME'] = cname
        agent_endpoint = 'http://{}:{}@127.0.0.1:57412/config/v1/project/_iot_gateway/mqtt_clients'.format (user, passw)
        channel_endpoint = 'http://{}:{}@127.0.0.1:57412/config/v1/project/channels/'.format(user, passw)
        device_endpoint = 'http://{}:{}@127.0.0.1:57412/config/v1/project/channels/{}/devices/.'.format(user, passw, cname)
        rpchan = requests.post(url=channel_endpoint, json=tchan)
        rpchan.raise_for_status()
        rpagent = requests.post (url=agent_endpoint, json=tagent)
        rpagent.raise_for_status ()

        def make_device_list():
            device_list = []
            add_dev = tdev
            x = 0
            for i in devices:
                d_name = i['Device']
                add_dev['common.ALLTYPES_NAME'] = d_name
                add_dev['servermain.DEVICE_ID_STRING'] = "1.{}".format(d_name)
                device_list.append(add_dev.copy())
                x += 1
                if x == dev_limit:
                    break
            return device_list

        out = make_device_list()

        rpdev = requests.post(url=device_endpoint, json=out)
        rpdev.raise_for_status()
        print ("-- Channel and devices and agent created")
        return

    except requests.exceptions.HTTPError as err:
        print("-- POSTs failed - '{}'".format(err))
        return False


def make_tags(master_list, devices, tchan, ttag, user, passw, limit, titem):
    try:
        print ("Creating devices tags and iot item references")
        x = 0
        # obtain and review each unique device ID found in converted CSV
        for i in devices:
            add_tag = ttag
            c_name = tchan['common.ALLTYPES_NAME']
            add_iot_item = titem
            d_name = i['Device']
            device_tag_list = []
            agent_tag_list = []

            # for each tag (item) present in converted CSV associated with the current device ID, build device tag and iot item tag reference ready for posting to Kepware
            for item in master_list:
                if item['Device'] == d_name:
                    t_name = item['Name']
                    instance = item['Instance']

                    # based on the name of the item in the converted CSV, make custom tag address per driver requirements and also make an iot item reference
                    def make_address():
                        if "AI" in t_name:
                            add_tag['servermain.TAG_ADDRESS'] = 'AnalogInput.' + instance + '.PresentValue'
                            add_tag['servermain.TAG_DATA_TYPE'] = 8
                            add_iot_item['iot_gateway.IOT_ITEM_SERVER_TAG'] = "{}.{}.{}".format(c_name, d_name, t_name)
                        else:
                            if "AV" in t_name:
                                add_tag['servermain.TAG_ADDRESS'] = 'AnalogValue.' + instance + '.PresentValue'
                                add_tag['servermain.TAG_DATA_TYPE'] = 8
                                add_iot_item['iot_gateway.IOT_ITEM_SERVER_TAG'] = "{}.{}.{}".format (c_name, d_name, t_name)
                            else:
                                if "BI" in t_name:
                                    add_tag['servermain.TAG_ADDRESS'] = 'BinaryInput.' + instance + '.PresentValue'
                                    add_tag['servermain.TAG_DATA_TYPE'] = 1
                                    add_iot_item['iot_gateway.IOT_ITEM_SERVER_TAG'] = "{}.{}.{}".format (c_name, d_name, t_name)
                                else:
                                    if "BO" in t_name:
                                        add_tag['servermain.TAG_ADDRESS'] = 'BinaryOutput.' + instance + '.PresentValue'
                                        add_tag['servermain.TAG_DATA_TYPE'] = 1
                                        add_iot_item['iot_gateway.IOT_ITEM_SERVER_TAG'] = "{}.{}.{}".format (c_name, d_name,t_name)
                                    else:
                                        if "BV" in t_name:
                                            add_tag['servermain.TAG_ADDRESS'] = 'BinaryValue.' + instance + '.PresentValue'
                                            add_tag['servermain.TAG_DATA_TYPE'] = 1
                                            add_iot_item['iot_gateway.IOT_ITEM_SERVER_TAG'] = "{}.{}.{}".format (c_name, d_name, t_name)
                                        else:
                                            pass
                        return

                    make_address()
                    add_tag['common.ALLTYPES_NAME'] = t_name

                    # add device tag and iot item tag references to lists
                    agent_tag_list.append(add_iot_item.copy())
                    device_tag_list.append(add_tag.copy())

                    # define the unique device's tag addition endpoint
                    tag_endpoint = 'http://{}:{}@127.0.0.1:57412/config/v1/project/channels/{}/devices/{}/tags/'.format(user, passw, c_name, d_name)
                else:
                    pass

            # post list of device tags to dynamic endpoints
            rptag = requests.post (url=tag_endpoint, json=device_tag_list)

            # as tag sets are built for each device, post the device's list of iot item references to agent
            posted_agent_endpoint = 'http://{}:{}@127.0.0.1:57412/config/v1/project/_iot_gateway/mqtt_clients/{}/iot_items/'.format (user, passw, c_name)
            rpagent_items = requests.post(url=posted_agent_endpoint, json = agent_tag_list)

            # since we're parsing through all unique devices, stop at a maximum based on number of devices allowed per channel
            x += 1
            if x == limit:
                break

        print ("-- Device tags and IoT item references created")
        return rptag, rpagent_items
    except Exception as e:
        print ("-- Device tag and iot item reference creation failed - '{}'".format (e))
        return False

        
# load setup parameters
setupFilePath = 'setup.json'
setupData = get_parameters(setupFilePath)

# assign global variables
user = setupData['configApiUsername']
passw = setupData['configApiPassword']

# set limit of devices based on device-per-channel limit in Kepware
device_limit = 128

# get json templates for channel, device, and tag
jChan, jDev, jTag, jAgent, jAgentItem = get_templates()

# convert CSV file to JSON
csv_file_path = setupData['path']
masterList = convert_csv_to_json(csv_file_path)

# obtain list of unique devices from converted csv
uniqueDevices = get_unique_devices(masterList)

# create devices and MQTT agent
make_devices(uniqueDevices, jChan, jDev, jAgent, device_limit, user, passw)

# add tags to devices and iot item references to agent
make_tags(masterList, uniqueDevices, jChan, jTag, user, passw, device_limit, jAgentItem)
