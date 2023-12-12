import os
from webdav3.client import Client
import os
from service.webdav_options import webDavOption

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

    webDavOption = webDavOption(dav=client)

    print(webDavOption.rename("/singstor-drive-vue-new/test_1", "/test_11"))
