
from kepconfig import connection, error, connectivity
import ssl


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




# Channel and Device name to be used /?#
# ch_name = 'Chann:/?#[]@!$&\'()*+,;=el1'
ch_name = 'Channel1'
dev_name = 'Device1'

# For tls versions, use the various PROTOCOL constants from the SSL module: https://docs.python.org/3.9/library/ssl.html#ssl.PROTOCOL_TLSv1
# 
# Typically will be ssl.PROTOCOL_TLSv1, ssl.PROTOCOL_TLSv1_1 or ssl.PROTOCOL_TLSv1_2

server = connection.server(host = '127.0.0.1', port = 57512, user = 'Administrator', pw = '', https=True, tls= ssl.PROTOCOL_TLSv1_1)
server.SSL_trust_all_certs = True


try:
    channel_data = {"common.ALLTYPES_NAME": ch_name,"servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"}
    r = connectivity.channel.add_channel(server,channel_data)
    print(r)

    r = connectivity.channel.get_channel(server, ch_name)
    print(r)

except Exception as err:
    ErrorHandler(err)

