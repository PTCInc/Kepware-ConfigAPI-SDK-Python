# Kepware Configuration API SDK for Python

This is a package SDK to create Python modules to conduct operations with the Kepware Configuration API.

## Prerequisites

The client libraries are supported on Python 3.6 or later.

## Features

- Supports both HTTP and HTTPS connections with certificate validation options

SDK allows for *GET*, *ADD*, *DELETE*, and *MODIFY* functions for the following Kepware configuration objects:

- **Project Properties** *(Get and Modify Only)*
- **Connectivity** *(Channel, Devices, Tags, Tag Groups)*
- **IoT Gateway** *(Agents, IoT Items)*

Methods to read the following logs:

- **Event Log**
- **API Transaction Log**

Additionally the following *Services* are implemented:

- **TagGeneration** *(not supported by all drivers)*
- **ReinitializeRuntime** *(Thingworx Kepware Edge and Kepware Server 6.8+)*

## Known Limitations

- Project Properties are not defined
- Other property configruation for more complex drivers are not explicitly defined
- Other supported plug-ins (Datalogger, Scheduler, etc) are not defined
- When using hostnames (not IP addresses) for connections, delays may occur under certain network configurations as the connection may attempt IPv6 connections first. IPv6 is not supported by Kepware servers at this time.

## Installation

> PIP packages can be found in the [dist](dist) folder to install. Installation can be done manually using the following:

```cmd
pip install kepconfig-<version>-py3-none-any.whl -f ./ --no-index
```

## Key Concepts

### Create server connection

```python
import kepconfig.connection

server = connection.server(host = '127.0.0.1', port = 57412, user = 'Administrator', pw = '')

# For HTTPS connections:
server = connection.server(host = '127.0.0.1', port = 57412, user = 'Administrator', pw = '', https=True)

```

For certificate validation, the SDK uses the OS/systems trusted CA certificate store. The connection leverages uses the "create_default_context()" function as part of urllib as described at the following links:

- [ssl.create_default_context](https://docs.python.org/3/library/ssl.html#ssl.create_default_context)
- [ssl.SSLContext.load_default_certs](https://docs.python.org/3/library/ssl.html#ssl.SSLContext.load_default_certs)
- [set_default_verify_paths](https://docs.python.org/3/library/ssl.html#ssl.SSLContext.set_default_verify_paths)

For Windows OSes, the Kepware server's instance certificate can be loaded into the hosts "Trusted Root Certificate Authorities" store.

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

## Need More Information

**Visit:**
[Kepware.com](https://www.kepware.com/)
