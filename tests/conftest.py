# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Pytest config file

import pytest, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kepconfig

@pytest.fixture(scope="module")
def kepware_server():
    return [kepconfig.connection.server(host = 'localhost', port = 57412, user = 'Administrator', pw = '', https = False), 'TKS']
    
    # server = kepconfig.connection.server(host = '127.0.0.1', port = 57513, user = 'Administrator', pw = 'Kepware400400400', https = True)
    # server.SSL_trust_all_certs = True
    # return [server, 'TKE']
