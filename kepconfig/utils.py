# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`utils` provides general utilities to help manage 
various objects for Kepware's configuration
"""

def path_split(path: str):
    '''Used to split the standard Kepware address decimal notation into a dict that contains the 
    *channel*, *device* and *tag_path* keys.

    :param path: standard Kepware address in decimal notation ("ch1.dev1.tg1.tg2.tg3")
    :return: dict that contains the "channel", "device" and "tag_path"
    :rtype: dict

    Ex: path = "ch1.dev1.tg1.tg2.tg3"

    return = {'channel': 'ch1', 'device': 'dev1', 'tag_path': ['tg1','tg2','tg3']}

    Ex: path = "ch1.dev1"

    return = {'channel': 'ch1', 'device': 'dev1'}
    '''
    path_list = path.split('.', 2)
    path_obj = {}
    for x in range(0, len(path_list)):
        if x == 0:
            path_obj['channel'] = path_list[0]
        elif x == 1:
            path_obj['device'] = path_list[1]
        else:
            path_obj['tag_path'] = path_list[2].split('.')
    return path_obj

def _address_dedecimal(tag_address):
    if tag_address[0] == '_':
        tag_address = tag_address[1::]
    updated = tag_address.replace('.','_')
    return updated
