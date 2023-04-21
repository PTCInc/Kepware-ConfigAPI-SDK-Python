# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`connectivity` module provides functionality to manage Kepware driver configuration 
available through the Kepware Configuration API. This includes channels, devices, 
tags, tag groups and driver specific objects. 

Driver specific object support, if available, through their own modules. Currently
the GE Ethernet Global Data and Universal Device Drivers have driver specific API
support in the SDK.
"""
from . import channel, device, tag, egd, udd