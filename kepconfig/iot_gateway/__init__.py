# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`iot_gateway` module provides support for Kepware's IoT Gateway plug-in 
specific objects within the Kepware Configuration API
"""

from . import agent, iot_items

#IoT Gateway Agent Types
MQTT_CLIENT_AGENT = 'MQTT Client'
REST_CLIENT_AGENT = 'REST Client'
REST_SERVER_AGENT = 'REST Server'
THINGWORX_AGENT = 'ThingWorx'
