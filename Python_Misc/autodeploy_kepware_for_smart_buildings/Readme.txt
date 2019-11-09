* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
* 									*
* Written By: S. Elsner						        *
* Date: September 2019						        *
* Script Type: Example for demonstration purposes and proofs of concept *
* 									*
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

!! PLEASE REVIEW IMPORTANT NOTES AT THE END OF README !!

OVERVIEW
This script automatically creates a complete Kepware project file based on a list of BACnet data points within a CSV file. The created project file will contain one BACnet channel, up to 128 BACnet devices below that channel, an IoT Gateway MQTT agent, and any number of tags and MQTT agent IoT item references. The IoT Gateway MQTT agent serves as an integration point to a single IoT Device created within an Azure IoT Hub.

DEPENDENCIES
This script leverages Python 3.7.4 and above and the following non-native Python library: requests (after installing Python 3.7.4 or above via https://www.python.org/downloads/, run 'pip install requests' from the command line in order to install the python 'requests' library)

INSTRUCTIONS
After installing Python and the 'requests' library, navigate to the 'autodeploy_kepware_for_smart_buildings' folder and double-click the Python script "auto_deploy.py". To observe verbose script output in a command prompt, call the script via the command line via "python auto_deploy.py"

PROCEDURE
The script performs the following tasks:

1- Ingests a setup file (setup.json in root of 'autodeploy_for_smart_buildings' directory) to determine values for the following critical variables:
-- Kepware Config API username ('administrator' by default)
-- Kepware Config API password (blank by default)
-- Kepware channel name ('B121' by default)
-- source CSV file path ('/csvs/source.csv' by default)

2- Creates a single BACnet channel and a single IoT Gateway MQTT agent from JSON object templates located in the script's 'objs' local directory

3- Ingests a CSV file located in the script's 'csvs' local diretory of the following CSV format and syntax in order to automatically create devices, device tags, and MQTT agent IoT item references:

Device, Name, ObjectType, Instance
1210100, AV_0, 2, 0

This yields Device with name "1210100" and tag with name "AV_0" and address of "AnalogValue.0.PresentValue" and an IoT item reference to "<channelNameDefinedinSetupFile>.<DeviceInstanceNumber>.<TagName>", i.e. B121.1210100.AV_0.

!! IMPORTANT NOTES !!
-- In its current design, this script must be local to Kepware - i.e. run on KEPServerEX's host operating system. To request enhancements to permit the script to run remotely, please email 'selsner@ptc.com'. 

-- Currently only the following BACnet data point types (called "object types") are supported: Analog Inputs, Analog Outputs, Analog Values, Binary Inputs, Binary Outputs, and Binary Values

-- Azure connectivity (MQTT agent configuration) is controlled by / modified via the JSON object file at ./objs/agent.json. This JSON object file also includes a configuration of desired message format.

-- BACnet network number is assumed (and thus hard-coded) to be "1", which yields Device Instance addresses like "1.1210100".

-- BACnet device discovery is assumed (and thus hard-coded) to be "automatic via WhoIs/IAm", which means no IP address information is required, but that the devices need to support this BACnet service. Otherwise, the script should be run first and then the IP addresses / discovery type modified afterwards either manually via the Configuration Tool or in batch via the Configuration API and a custom script, or via the Configuration API and an off-the-shelf HTTP/REST request application like Postman (www.getpostman.com)

-- If more than 128 BACnet devices are identified in the source CSV file, only 128 will be created. The value of '128' is the "device" limit per single channel for Kepware KEPServerEX V6.7 and below.

-- To communicate to more than 128 BACnet devices, the simplest option is to use additional, seperate instances of Kepware server on separate operating systems (virtual machines or physical), modifying the source CSV, .

-- Whether for performance goals or for scaling goals, you may want to configure connections to more than 128 devices within a single Kepware project. To do this, you'll need more than one channel in your Kepware project. To configure more than one BACnet channel in a single Kepware project, you'll need to prepare your BACnet devices OR the PC / VM running Kepware in the following manner:

---- 1: You either need to use a new UDP port (47809, for example), configuring your BACnet devices to support this additional port and updating the source UDP port in the "channel" object file within /objs/channel.json, or 
---- 2: Add additional network adapters to the PC / VM running Kepware OR multi-home your single adapter to add virtual IPs. Multi-homing instructions are included in the Kepware BACnet/IP driver Help file. In either case, make sure to update the Network Adapter setting in the "channel" object file within /objs/channel.json.

   Once the PC / VM is prepared, change the name of the channel in "setup.json" and re-run the script, providing a new or modified source CSV file for unique BACnet data point references.