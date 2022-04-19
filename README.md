# Kepware Configuration API SDK for Python

[![PyPI version](https://badge.fury.io/py/kepconfig.svg)](https://badge.fury.io/py/kepconfig)

This is a package SDK to create Python modules to conduct operations with the Kepware Configuration API. This package is designed to work with all versions of Kepware that support the Configuration API including Thingworx Kepware Server (TKS), Thingworx Kepware Edge (TKE) and KEPServerEX (KEP).

## Prerequisites

The client libraries are supported on Python 3.6 or later. All HTTP communication is handled by the [urllib](https://docs.python.org/3.6/library/urllib.html#module-urllib) Python standard library.

## Features

- Supports both HTTP and HTTPS connections with certificate validation options

SDK allows for *GET*, *ADD*, *DELETE*, and *MODIFY* functions for the following Kepware configuration objects:

| Features      | TKS/KEP       | TKE           |
| :----------:  | :----------:  | :----------:  |
| **Project Properties** <br /> *(Get and Modify Only)* | Y | Y |
| **Connectivity** <br /> *(Channel, Devices, Tags, Tag Groups)* | Y | Y |
| **IoT Gateway** <br /> *(Agents, IoT Items)* | Y | Y |
| **Datalogger** <br /> *(Log Groups, Items, Mapping, Triggers, Reset Mapping Service)* | Y | Y |
| **Administration** <br /> *(User Groups, Users, UA Endpoints)* | Y* | Y |

Note (*) - UA Endpoints supported for Kepware Edge only

Driver specific features:

| Driver          | Features       |
| :----------:  | :----------:  |
|GE Ethernet Global Data|Exchanges, Ranges and Name Resolutions|

Methods to read the following logs:

| Logs          | TKS/KEP       | TKE           |
| :----------:  | :----------:  | :----------:  |
| **Event Log** | Y | Y |
| **API Transaction Log** | Y | Y |

Configuration API *Services* implemented:

| Services      | TKS/KEP       | TKE           |
| :----------:  | :----------:  | :----------:  |
| **TagGeneration** <br /> *(for supported drivers)* | Y | Y |
| **ReinitializeRuntime** | Y* | Y |

Note (*) - Reinitialize service was implemented for Kepware Server v6.8+

Generic REST methods are provided to use for functions not developed in SDK package. These are found in the Server Class in [connection.py](/kepconfig/connection.py)

## Known Limitations

- Other property configuration for more complex drivers with objects besides channels, devices, tags and tag groups are not explicitly defined
- Other supported plug-ins (EFM Exporter, Scheduler, etc) are not defined
- When using hostnames (not IP addresses) for connections, delays may occur under certain network configurations as the connection may attempt IPv6 connections first. IPv6 is not supported by Kepware servers at this time.

## Installation

Package can be installed with `pip` using the following:

```cmd
    pip install kepconfig
```

## Key Concepts

NOTE: Samples can also be found in the [samples](samples) folder.

### Create server connection

```python
import kepconfig.connection

server = connection.server(host = '127.0.0.1', port = 57412, user = 'Administrator', pw = '')

# For HTTPS connections:
server = connection.server(host = '127.0.0.1', port = 57412, user = 'Administrator', pw = '', https=True)

```

For certificate validation, the SDK uses the OS/systems trusted CA certificate store. The connection uses the "create_default_context()" function as part of urllib as described at the following links:

- [ssl.create_default_context](https://docs.python.org/3/library/ssl.html#ssl.create_default_context)
- [ssl.SSLContext.load_default_certs](https://docs.python.org/3/library/ssl.html#ssl.SSLContext.load_default_certs)
- [set_default_verify_paths](https://docs.python.org/3/library/ssl.html#ssl.SSLContext.set_default_verify_paths)

For Windows OSes, the Kepware server's instance certificate can be loaded into the hosts "Trusted Root Certificate Authorities" store.

### Create an object

Objects such as channels or devices can be created either singularly or with children included.

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

- [Kepware.com](https://www.kepware.com/)
- [Configuration API Info](https://www.kepware.com/en-us/products/kepserverex/features/configuration-api/)
- [PTC.com](https://www.ptc.com/)
