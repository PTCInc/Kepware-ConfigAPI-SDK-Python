# -------------------------------------------------------------------------
# Copyright (c) 2020, PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


__path__ = __import__("pkgutil").extend_path(__path__, __name__)
from . import agent, iot_items

#IoT Gateway Agent Types
MQTT_CLIENT_AGENT = 'MQTT Client'
REST_CLIENT_AGENT = 'REST Client'
REST_SERVER_AGENT = 'REST Server'
THINGWORX_AGENT = 'ThingWorx'
