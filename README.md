# Kepware Configuration API SDK for Python

This is a package SDK to create Python modules to conduct operations with the Kepware Configuration API.

## Prerequisites

The client libraries are supported on Python 3.6 or later.

## Features

SDK allows for *GET*, *ADD*, *DELETE*, and *MODIFY* functions for the following Kepware  configuration objects:

- **Connectivity** *(Channel, Devices, Tags, Tag Groups)*
- **IoT Gateway** *(Agents, IoT Items)*

Methods to read the following logs:

- **Event Log**
- **API Transaction Log**

Additionally the following *Services* are implemented:

- **TagGeneration** *(not supported by all drivers)*
- **ReinitializeRuntime** *(Thingworx Kepware Edge only)*

## Limitations

- Supports HTTP connections only

## Installation

> TBD

## Key Concepts

### Create server connection

```python
import kepconfig.connection

server = connection.server(host = '127.0.0.1', port = 57412, user = 'Administrator', pw = '')
```

### Create an object

Objects such as channels or devices can be created either sigularly or with children included.

### Ex: Add Single channel

```python
from kepconfig.connectivity import channel

channel_data = {"common.ALLTYPES_NAME": "Channel1","servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"}
result = channel.add_channel(server,channel_data)
```

### Ex: Add Multiple tags

```python
from kepconfig.connectivity import tag

tag_info = [
    {
            "common.ALLTYPES_NAME": "Temp",
            "servermain.TAG_ADDRESS": "R0"
    },
    {
            "common.ALLTYPES_NAME": "Temp2",
            "servermain.TAG_ADDRESS": "R1"
    }
]
tag_path = '{}.{}.{}'.format(ch_name, dev_name, tag_group_path)
result = tag.add_tag(server, tag_path, tag_info))

```

## Need help?

**Visit:**
[Kepware.com](https://www.kepware.com/)