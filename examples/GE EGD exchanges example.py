# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# GE EGD Exchanges Example - Example on how to manage exchanges, ranges within
# an exchange and name resolution components for the GE Ethernet Global Data 
# driver through the Kepware Configuration API


from kepconfig import connection, error
from kepconfig.connectivity import channel, egd

# Channel and Device name to be used
ch_name = 'EGD'
dev_name = 'Device1'

egd_device = {
    "common.ALLTYPES_NAME": ch_name,
    "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "GE Ethernet Global Data",
    "devices": [{
        "common.ALLTYPES_NAME": dev_name,
        "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "GE Ethernet Global Data"
    }]
}

def ErrorHandler(err):
    # Generic Handler for exception errors
    if isinstance(err,  error.KepHTTPError):
        print(err.code)
        print(err.msg)
        print(err.url)
        print(err.hdrs)
        print(err.payload)
    elif isinstance(err,  error.KepURLError):
        print(err.url)
        print(err.reason)
    elif isinstance(err, error.KepError):
        print(err.msg)
    else:
        print('Different Exception Received: {}'.format(err))


# This creates a server reference that is used to target all modifications of 
# the Kepware configuration
server = connection.server(host = '127.0.0.1', port = 57412, user = 'Administrator', pw = '')

# Add a EGD Channel and Device
try:
    print("{} - {}".format("Adding EGD Channel and Device:", channel.add_channel(server,egd_device)))
except Exception as err:
    ErrorHandler(err)

#####################################################################
# Examples of managing Exchanges and Ranges in the Exchanges
#####################################################################


# Adding Exchanges to the device - Multiple exchanges can be added by creating a list of exchanges
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

try:
    print("{} - {}".format("Adding Consumer Exchange:", egd.exchange.add_exchange(server, ch_name + '.' + dev_name, egd.CONSUMER_EXCHANGE, consumer_exchange)))
except Exception as err:
    ErrorHandler(err)

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

try:
    print("{} - {}".format("Adding Producer Exchange:", egd.exchange.add_exchange(server, ch_name + '.' + dev_name, egd.PRODUCER_EXCHANGE, producer_exchange)))
except Exception as err:
    ErrorHandler(err)

# Modify an Exchange
try:
    print("{} - {}".format("Modify Consumer Exchange:", egd.exchange.modify_exchange(server, ch_name + '.' + dev_name, egd.CONSUMER_EXCHANGE, 
        {"ge_ethernet_global_data.CONSUMER_EXCHANGE_NUMBER": 2},exchange_name= consumer_exchange['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)

# Get Exchange Properties
try:
    print("{} - {}".format("Read Consumer Exchange {}:".format(consumer_exchange['common.ALLTYPES_NAME']), 
        egd.exchange.get_exchange(server, ch_name + '.' + dev_name, egd.CONSUMER_EXCHANGE, consumer_exchange['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)

# Get all Consumer/Producer Exchanges
try:
    print("{} - {}".format("Read all Consumer Exchanges:", 
        egd.exchange.get_exchange(server, ch_name + '.' + dev_name, egd.CONSUMER_EXCHANGE)))
except Exception as err:
    ErrorHandler(err)

# Get all Exchanges
try:
    print("{} - {}".format("Read all Exchanges:", 
        egd.exchange.get_all_exchanges(server, ch_name + '.' + dev_name)))
except Exception as err:
    ErrorHandler(err)

# Delete Exchange
try:
    print("{} - {}".format("Deleting Producer Exchange {}:".format(producer_exchange['common.ALLTYPES_NAME']), 
        egd.exchange.del_exchange(server, ch_name + '.' + dev_name, egd.PRODUCER_EXCHANGE, producer_exchange['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)

# Adding a Range - Multiple ranges can be added by creating a list of ranges
range = {
    "common.ALLTYPES_NAME": "Range_0",
    "common.ALLTYPES_DESCRIPTION": "",
    "ge_ethernet_global_data.RANGE_INDEX": 1,
    "ge_ethernet_global_data.RANGE_OFFSET": 0,
    "ge_ethernet_global_data.RANGE_REFERENCE": 0,
    "ge_ethernet_global_data.RANGE_LOW_POINT": 0,
    "ge_ethernet_global_data.RANGE_HIGH_POINT": 8
}

try:
    print("{} - {}".format("Adding a Range to a Consumer Exchange:", egd.range.add_range(server, ch_name + '.' + dev_name, 
        egd.CONSUMER_EXCHANGE, consumer_exchange['common.ALLTYPES_NAME'], range)))
except Exception as err:
    ErrorHandler(err)

# Modify a Range
try:
    print("{} - {}".format("Modify a Range to a Consumer Exchange:", egd.range.modify_range(server, ch_name + '.' + dev_name, egd.CONSUMER_EXCHANGE, consumer_exchange['common.ALLTYPES_NAME'], 
        {"ge_ethernet_global_data.CONSUMER_EXCHANGE_NUMBER": 2}, range['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)

# Get a Range for an Exchange
try:
    print("{} - {}".format("Read a Range from a Consumer Exchange - {}:".format(range['common.ALLTYPES_NAME']), egd.range.get_range(server, ch_name + '.' + dev_name, 
        egd.CONSUMER_EXCHANGE, consumer_exchange['common.ALLTYPES_NAME'], range['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)

# Get all Ranges for an Exchange
try:
    print("{} - {}".format("Read all Ranges from a Consumer Exchange:", egd.range.get_range(server, ch_name + '.' + dev_name, 
        egd.CONSUMER_EXCHANGE, consumer_exchange['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)

# Delete a Range for an Exchange
try:
    print("{} - {}".format("Delete a Range from a Consumer Exchange:", egd.range.del_range(server, ch_name + '.' + dev_name, 
        egd.CONSUMER_EXCHANGE, consumer_exchange['common.ALLTYPES_NAME'], range['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)

#####################################################################
# Examples of managing Name Resolutions
#####################################################################

#  Add a Name Resolution - Multiple name resolutions can be added by creating a list of them
name = {
        "common.ALLTYPES_NAME": "PLC1",
        "common.ALLTYPES_DESCRIPTION": "",
        "ge_ethernet_global_data.NAME_RESOLUTION_ALIAS": "PLC1",
        "ge_ethernet_global_data.NAME_RESOLUTION_IP_ADDRESS": "192.168.1.200"
    }

try:
    print("{} - {}".format("Adding Name Resolution:", egd.name.add_name_resolution(server, ch_name + '.' + dev_name, name)))
except Exception as err:
    ErrorHandler(err)

# Modify a Name Resolution
try:
    print("{} - {}".format("Modify Name Resolution {}:".format(name['common.ALLTYPES_NAME']), egd.name.modify_name_resolution(server, ch_name + '.' + dev_name,
        {"ge_ethernet_global_data.NAME_RESOLUTION_IP_ADDRESS": '192.168.1.50'}, name['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)

# Get Name Resolution Properties
try:
    print("{} - {}".format("Read Name Resolution {}:".format(name['common.ALLTYPES_NAME']), 
        egd.name.get_name_resolution(server, ch_name + '.' + dev_name, name['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)

# Get all Name Resolutions
try:
    print("{} - {}".format("Read All Name Resolutions:".format(name['common.ALLTYPES_NAME']), 
        egd.name.get_name_resolution(server, ch_name + '.' + dev_name, name['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)

# Delete a Name Resolution
try:
    print("{} - {}".format("Delete Name Resolution {}:".format(name['common.ALLTYPES_NAME']), 
        egd.name.del_name_resolution(server, ch_name + '.' + dev_name, name['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)