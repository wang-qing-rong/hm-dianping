from webdav3.client import Client
import os



if __name__ == '__main__':
    options = {
        'webdav_hostname': "http://localhost/webDav",
        'webdav_digest_auth': ('wqr', '111111'),
        'webdav_override_methods': {
            'check': 'GET'
        },
        'webdav_auth': 'digest'
    }
    client = Client(options)
    client_list = client.list('/')
    for item in client_list:
        print(item)
