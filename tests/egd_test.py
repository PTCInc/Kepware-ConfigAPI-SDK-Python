# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# EGD Test - Test to exersice all GE EGD driver exchange related features 
# including, exchanges, ranges and name resolutions

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kepconfig
import kepconfig.connectivity
import time
import datetime
import pytest
# import connectivity, admin, iot_gateway, datalogger


# Channel and Device name to be used
ch_name = 'EGD'
dev_name = 'Device1'

consumer_exchange = {
    "common.ALLTYPES_NAME": "0",
    "common.ALLTYPES_DESCRIPTION": "",
    "ge_ethernet_global_data.CONSUMER_EXCHANGE_ID": 0,
    "ge_ethernet_global_data.CONSUMER_EXCHANGE_NUMBER": 1,
    "ge_ethernet_global_data.CONSUMER_EXCHANGE_PRODUCER_ID": "192.168.1.130",
    "ge_ethernet_global_data.CONSUMER_EXCHANGE_GROUP_ID": 1,
    "ge_ethernet_global_data.CONSUMER_EXCHANGE_CONSUMED_PERIOD_MS": 1000,
    "ge_ethernet_global_data.CONSUMER_EXCHANGE_UPDATE_TIMEOUT_MS": 10000
}
consumer_exchange10 = {
    "common.ALLTYPES_NAME": "10",
    "common.ALLTYPES_DESCRIPTION": "",
    "ge_ethernet_global_data.CONSUMER_EXCHANGE_ID": 10,
    "ge_ethernet_global_data.CONSUMER_EXCHANGE_NUMBER": 10,
    "ge_ethernet_global_data.CONSUMER_EXCHANGE_PRODUCER_ID": "192.168.1.130",
    "ge_ethernet_global_data.CONSUMER_EXCHANGE_GROUP_ID": 1,
    "ge_ethernet_global_data.CONSUMER_EXCHANGE_CONSUMED_PERIOD_MS": 1000,
    "ge_ethernet_global_data.CONSUMER_EXCHANGE_UPDATE_TIMEOUT_MS": 10000
}
producer_exchange = {
    "common.ALLTYPES_NAME": "0",
    "common.ALLTYPES_DESCRIPTION": "",
    "ge_ethernet_global_data.PRODUCER_EXCHANGE_ID": 0,
    "ge_ethernet_global_data.PRODUCER_EXCHANGE_NUMBER": 0,
    "ge_ethernet_global_data.PRODUCER_EXCHANGE_CONSUMED_TYPE": 1,
    'ge_ethernet_global_data.PRODUCER_EXCHANGE_CONSUMED_ADDRESS_GROUP_ID':0,
    "ge_ethernet_global_data.PRODUCER_EXCHANGE_CONSUMED_ADDRESS_IP": "10.10.10.10",
    'ge_ethernet_global_data.PRODUCER_EXCHANGE_CONSUMED_ADDRESS_NAME': '',
    "ge_ethernet_global_data.PRODUCER_EXCHANGE_PRODUCER_INTERVAL_MS": 10
}
producer_exchange10 = {
    "common.ALLTYPES_NAME": "10",
    "common.ALLTYPES_DESCRIPTION": "",
    "ge_ethernet_global_data.PRODUCER_EXCHANGE_ID": 10,
    "ge_ethernet_global_data.PRODUCER_EXCHANGE_NUMBER": 10,
    "ge_ethernet_global_data.PRODUCER_EXCHANGE_CONSUMED_TYPE": 1,
    'ge_ethernet_global_data.PRODUCER_EXCHANGE_CONSUMED_ADDRESS_GROUP_ID':0,
    "ge_ethernet_global_data.PRODUCER_EXCHANGE_CONSUMED_ADDRESS_IP": "10.10.10.10",
    'ge_ethernet_global_data.PRODUCER_EXCHANGE_CONSUMED_ADDRESS_NAME': '',
    "ge_ethernet_global_data.PRODUCER_EXCHANGE_PRODUCER_INTERVAL_MS": 10
}

range1 = {
    "common.ALLTYPES_NAME": "Range_0",
    "common.ALLTYPES_DESCRIPTION": "",
    "ge_ethernet_global_data.RANGE_INDEX": 1,
    "ge_ethernet_global_data.RANGE_OFFSET": 0,
    "ge_ethernet_global_data.RANGE_REFERENCE": 0,
    "ge_ethernet_global_data.RANGE_LOW_POINT": 0,
    "ge_ethernet_global_data.RANGE_HIGH_POINT": 8
}

range2 = {
    "common.ALLTYPES_NAME": "Range_1",
    "common.ALLTYPES_DESCRIPTION": "",
    "ge_ethernet_global_data.RANGE_INDEX": 2,
    "ge_ethernet_global_data.RANGE_OFFSET": 18,
    "ge_ethernet_global_data.RANGE_REFERENCE": 6,
    "ge_ethernet_global_data.RANGE_LOW_POINT": 0,
    "ge_ethernet_global_data.RANGE_HIGH_POINT": 10
}

name1 = {
        "common.ALLTYPES_NAME": "PLC1",
        "common.ALLTYPES_DESCRIPTION": "",
        "ge_ethernet_global_data.NAME_RESOLUTION_ALIAS": "PLC1",
        "ge_ethernet_global_data.NAME_RESOLUTION_IP_ADDRESS": "192.168.1.200"
    }

name2 = {
        "common.ALLTYPES_NAME": "PLC2",
        "common.ALLTYPES_DESCRIPTION": "",
        "ge_ethernet_global_data.NAME_RESOLUTION_ALIAS": "PLC2",
        "ge_ethernet_global_data.NAME_RESOLUTION_IP_ADDRESS": "192.168.1.201"
    }

def HTTPErrorHandler(err):
    if err.__class__ is kepconfig.error.KepHTTPError:
        print(err.code)
        print(err.msg)
        print(err.url)
        print(err.hdrs)
        print(err.payload)
    else:
        print('Different Exception Received: {}'.format(err))

egd_device = {
    "common.ALLTYPES_NAME": ch_name,
    "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "GE Ethernet Global Data",
    "devices": [{
        "common.ALLTYPES_NAME": dev_name,
        "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "GE Ethernet Global Data"
    }]
}

def initialize(server: kepconfig.connection.server):
    try:
        server._config_get(server.url +"/doc/drivers/GE Ethernet Global Data/channels")
    except Exception as err:
        pytest.skip("EGD Driver is not installed", allow_module_level=True)
    
    try:
        kepconfig.connectivity.channel.add_channel(server,egd_device) == True
    except Exception as err:
        pytest.skip("Device Configuration couldn't be added", allow_module_level=True)

def complete(server):
    try:
        kepconfig.connectivity.channel.del_channel(server,egd_device['common.ALLTYPES_NAME'])
    except Exception as err:
            HTTPErrorHandler(err)

@pytest.fixture(scope="module")
def server(kepware_server):
    server = kepware_server
    
    # Initialize any configuration before testing in module
    initialize(server)

    # Everything below yield is run after module tests are completed
    yield server
    complete(server)


def remove_projectid(DATA):
    if type(DATA) is dict:
        DATA.pop('PROJECT_ID', None)
    elif type(DATA) is list:
        for item in DATA:
            if type(item) is list:
                for x in item:
                    x.pop('PROJECT_ID', None)
            else:
                item.pop('PROJECT_ID', None)
    return DATA

# Exchange Tests
def create_exchange(server, exchange_type, exchanges):
    assert kepconfig.connectivity.egd.exchange.add_exchange(server, ch_name + '.' + dev_name, exchange_type, exchanges[0])

    # Delete
    assert kepconfig.connectivity.egd.exchange.del_exchange(server, ch_name + '.' + dev_name, exchange_type, exchanges[0]['common.ALLTYPES_NAME'])
    # Add multiple Exchanges
    assert kepconfig.connectivity.egd.exchange.add_exchange(server, ch_name + '.' + dev_name, exchange_type, exchanges)

def get_exchange(server, exchange_type, exchanges):

    # Get a specific Exchange
    ret = kepconfig.connectivity.egd.exchange.get_exchange(server, ch_name + '.' + dev_name, exchange_type, exchanges[0]['common.ALLTYPES_NAME'])
    assert type(ret) == dict, 'Unexpected data type return. {}'.format(type(ret))
    assert remove_projectid(ret) == exchanges[0]

    # Get All exchanges for exchange type
    ret = kepconfig.connectivity.egd.exchange.get_exchange(server, ch_name + '.' + dev_name, exchange_type)
    assert type(ret) == list, 'Unexpected data type return. {}'.format(type(ret))
    assert remove_projectid(ret) == exchanges

    # Get All exchanges for device
    ret = kepconfig.connectivity.egd.exchange.get_all_exchanges(server, ch_name + '.' + dev_name)
    assert type(ret) == list
    if exchange_type == kepconfig.connectivity.egd.PRODUCER_EXCHANGE:
        assert remove_projectid(ret) == [[],exchanges]
    else:
        assert remove_projectid(ret) == [exchanges,[]]

def modify_exchange(server, exchange_type, exchange_name):

    assert kepconfig.connectivity.egd.exchange.modify_exchange(server, ch_name + '.' + dev_name, exchange_type, 
        {"ge_ethernet_global_data.CONSUMER_EXCHANGE_NUMBER": 2}, exchange_name)
    assert kepconfig.connectivity.egd.exchange.modify_exchange(server, ch_name + '.' + dev_name, exchange_type, 
        {"common.ALLTYPES_NAME": exchange_name,"ge_ethernet_global_data.CONSUMER_EXCHANGE_NUMBER": 3})
    assert kepconfig.connectivity.egd.exchange.modify_exchange(server, ch_name + '.' + dev_name, exchange_type, 
        {"common.ALLTYPES_NAME": exchange_name,"ge_ethernet_global_data.CONSUMER_EXCHANGE_NUMBER": 4}, force=True)

def delete_exchange(server, exchange_type, exchange_name):

    assert kepconfig.connectivity.egd.exchange.del_exchange(server, ch_name + '.' + dev_name, exchange_type, exchange_name)

# Exchange Range tests
def create_range(server, exchange_type, exchange_name, ranges):
    assert kepconfig.connectivity.egd.range.add_range(server, ch_name + '.' + dev_name, exchange_type, exchange_name, ranges[0])

    # Delete
    assert kepconfig.connectivity.egd.range.del_range(server, ch_name + '.' + dev_name, exchange_type, exchange_name, ranges[0]['common.ALLTYPES_NAME'])
    # Add multiple ranges
    assert kepconfig.connectivity.egd.range.add_range(server, ch_name + '.' + dev_name, exchange_type, exchange_name, ranges)

def get_range(server, exchange_type, exchange_name, ranges):

    # Get a specific range
    ret = kepconfig.connectivity.egd.range.get_range(server, ch_name + '.' + dev_name, exchange_type, exchange_name, ranges[0]['common.ALLTYPES_NAME'])
    assert type(ret) == dict, 'Unexpected data type return. {}'.format(type(ret))
    assert remove_projectid(ret) == ranges[0]

    # Get All ranges for Exchange
    ret = kepconfig.connectivity.egd.range.get_range(server, ch_name + '.' + dev_name, exchange_type, exchange_name)
    assert type(ret) == list, 'Unexpected data type return. {}'.format(type(ret))
    assert remove_projectid(ret) == ranges

def modify_range(server, exchange_type, exchange_name, range_name):

    assert kepconfig.connectivity.egd.range.modify_range(server, ch_name + '.' + dev_name, exchange_type, exchange_name,
        {"ge_ethernet_global_data.RANGE_HIGH_POINT": 10}, range_name)
    assert kepconfig.connectivity.egd.range.modify_range(server, ch_name + '.' + dev_name, exchange_type, exchange_name,
        {"common.ALLTYPES_NAME": range_name,"ge_ethernet_global_data.RANGE_HIGH_POINT": 11})
    assert kepconfig.connectivity.egd.range.modify_range(server, ch_name + '.' + dev_name, exchange_type, exchange_name,
        {"common.ALLTYPES_NAME": range_name,"ge_ethernet_global_data.RANGE_HIGH_POINT": 8}, force=True)

def delete_range(server, exchange_type, exchange_name, range_name):

    assert kepconfig.connectivity.egd.range.del_range(server, ch_name + '.' + dev_name, exchange_type, exchange_name, range_name)

# Name Resolution Tests
def create_name(server, names):
    assert kepconfig.connectivity.egd.name.add_name_resolution(server, ch_name + '.' + dev_name, names[0])

    # Delete
    assert kepconfig.connectivity.egd.name.del_name_resolution(server, ch_name + '.' + dev_name, names[0]['common.ALLTYPES_NAME'])
    # Add multiple ranges
    assert kepconfig.connectivity.egd.name.add_name_resolution(server, ch_name + '.' + dev_name, names)

def get_name(server, names):

    # Get a specific range
    ret = kepconfig.connectivity.egd.name.get_name_resolution(server, ch_name + '.' + dev_name, names[0]['common.ALLTYPES_NAME'])
    assert type(ret) == dict, 'Unexpected data type return. {}'.format(type(ret))
    assert remove_projectid(ret) == names[0]

    # Get All ranges for Exchange
    ret = kepconfig.connectivity.egd.name.get_name_resolution(server, ch_name + '.' + dev_name)
    assert type(ret) == list, 'Unexpected data type return. {}'.format(type(ret))
    assert remove_projectid(ret) == names

def modify_name(server, name):

    assert kepconfig.connectivity.egd.name.modify_name_resolution(server, ch_name + '.' + dev_name,
        {"ge_ethernet_global_data.NAME_RESOLUTION_IP_ADDRESS": '192.168.1.50'}, name)
    assert kepconfig.connectivity.egd.name.modify_name_resolution(server, ch_name + '.' + dev_name,
        {"common.ALLTYPES_NAME": name,"ge_ethernet_global_data.NAME_RESOLUTION_IP_ADDRESS": '192.168.1.100'})
    assert kepconfig.connectivity.egd.name.modify_name_resolution(server, ch_name + '.' + dev_name,
        {"common.ALLTYPES_NAME": name,"ge_ethernet_global_data.NAME_RESOLUTION_IP_ADDRESS": '192.168.1.202'}, force=True)

def delete_name(server, name):

    assert kepconfig.connectivity.egd.name.del_name_resolution(server, ch_name + '.' + dev_name, name)


# 
# MAIN TEST SET
# 


def test_consumer_exchange(server):
    # initialize(server)
    create_exchange(server, kepconfig.connectivity.egd.CONSUMER_EXCHANGE,[consumer_exchange, consumer_exchange10])
    get_exchange(server, kepconfig.connectivity.egd.CONSUMER_EXCHANGE, [consumer_exchange, consumer_exchange10])

    # Range Tests
    create_range(server, kepconfig.connectivity.egd.CONSUMER_EXCHANGE, consumer_exchange['common.ALLTYPES_NAME'], [range1, range2])
    get_range(server, kepconfig.connectivity.egd.CONSUMER_EXCHANGE, consumer_exchange['common.ALLTYPES_NAME'], [range1, range2])
    modify_range(server, kepconfig.connectivity.egd.CONSUMER_EXCHANGE, consumer_exchange['common.ALLTYPES_NAME'], range1['common.ALLTYPES_NAME'])
    delete_range(server, kepconfig.connectivity.egd.CONSUMER_EXCHANGE, consumer_exchange['common.ALLTYPES_NAME'], range1['common.ALLTYPES_NAME'])

    modify_exchange(server, kepconfig.connectivity.egd.CONSUMER_EXCHANGE, consumer_exchange['common.ALLTYPES_NAME'])
    delete_exchange(server, kepconfig.connectivity.egd.CONSUMER_EXCHANGE, consumer_exchange['common.ALLTYPES_NAME'])
    delete_exchange(server, kepconfig.connectivity.egd.CONSUMER_EXCHANGE, consumer_exchange10['common.ALLTYPES_NAME'])
    # complete(server)

def test_producer_exchange(server):
    # initialize(server)
    create_exchange(server, kepconfig.connectivity.egd.PRODUCER_EXCHANGE,[producer_exchange, producer_exchange10])
    get_exchange(server, kepconfig.connectivity.egd.PRODUCER_EXCHANGE, [producer_exchange, producer_exchange10])
    
    # Range Tests
    create_range(server, kepconfig.connectivity.egd.PRODUCER_EXCHANGE, producer_exchange['common.ALLTYPES_NAME'], [range1, range2])
    get_range(server, kepconfig.connectivity.egd.PRODUCER_EXCHANGE, producer_exchange['common.ALLTYPES_NAME'], [range1, range2])
    modify_range(server, kepconfig.connectivity.egd.PRODUCER_EXCHANGE, producer_exchange['common.ALLTYPES_NAME'], range1['common.ALLTYPES_NAME'])
    delete_range(server, kepconfig.connectivity.egd.PRODUCER_EXCHANGE, producer_exchange['common.ALLTYPES_NAME'], range1['common.ALLTYPES_NAME'])

    modify_exchange(server, kepconfig.connectivity.egd.PRODUCER_EXCHANGE, producer_exchange['common.ALLTYPES_NAME'])
    delete_exchange(server, kepconfig.connectivity.egd.PRODUCER_EXCHANGE, producer_exchange['common.ALLTYPES_NAME'])
    delete_exchange(server, kepconfig.connectivity.egd.PRODUCER_EXCHANGE, producer_exchange10['common.ALLTYPES_NAME'])
    # complete(server)

def test_name_resolutions(server):
    # initialize(server)
    create_name(server, [name1, name2])
    get_name(server, [name1, name2])
    modify_name(server, name1['common.ALLTYPES_NAME'])
    delete_name(server, name1['common.ALLTYPES_NAME'])
    # complete(server)