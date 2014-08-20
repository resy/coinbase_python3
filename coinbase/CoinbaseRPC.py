# ----- Author ----------------------------------------------------------------

__author__ = 'Michael Montero <mike@resy.com>'

# ----- Imports ---------------------------------------------------------------

from .CoinbaseAPIKeyAuthentication import CoinbaseAPIKeyAuthentication
from .CoinbaseOAuthAuthentication import CoinbaseOAuthAuthentication
from .error import CoinbaseAPIException

import hashlib
import hmac
import json
import requests
import time
import urllib.parse

# ----- Public Classes --------------------------------------------------------

class CoinbaseRPC(object):
    '''
    Abstracts functionality for executing remote procedure calls.
    '''

    COINBASE_API = 'https://coinbase.com/api/v1'

    def __init__(self, authentication):
        self.__authentication = authentication


    def request(self, method, url, params=None):
        url = self.COINBASE_API + url

        query_string = ''
        if params is not None and len(params) > 0:
            query_string = urllib.parse.urlencode(params)

        method = method.lower()
        if (method == 'get' or method == 'delete') and \
           len(query_string) > 0:
            url += '?' + query_string

        headers = {
            'User-Agent': 'CoinbasePython3/v1'
        }

        auth = self.__authentication.get_data()

        if isinstance(self.__authentication, CoinbaseOAuthAuthentication):
            headers['Authorization'] = 'Bearer ' + auth['access_token']
        elif isinstance(self.__authentication, CoinbaseAPIKeyAuthentication):
            nonce = int(time.time() * 1e6)

            data_to_hash = str(nonce) + url
            if (method == 'post' or method == 'put') and \
               len(query_string) > 0:
                data_to_hash += query_string

            signature = \
                hmac.new(
                    auth['api_secret'].encode(),
                    data_to_hash.encode(),
                    hashlib.sha256) \
                .hexdigest()

            headers['ACCESS_KEY'] = auth['api_key']
            headers['ACCESS_SIGNATURE'] = signature
            headers['ACCESS_NONCE'] = nonce
        else:
            raise CoinbaseAPIException('Invalid authentication mechanism')

        if method == 'get':
            request = requests.get(url, headers=headers)
        elif method == 'delete':
            request = requests.delete(url, params=params, headers=headers)
        elif method == 'post':
            request = requests.post(url, data=params, headers=headers)
        elif method == 'put':
            request = requests.put(url, data=params, headers=headers)

        if request.status_code != 200:
            raise CoinbaseAPIException(
                    'Status Code ' + str(request.status_code),
                    request.status_code,
                    request.content.decode())

        content = json.loads(request.content.decode())
        if content is None or len(content) == 0:
            raise CoinbaseAPIException(
                    'Invalid response body',
                    request.status_code,
                    request.content.decode())

        if 'error' in content:
            raise CoinbaseAPIException(
                    content['error'],
                    request.status_code,
                    request.content.decode())

        if 'errors' in content:
            raise CoinbaseAPIException(
                    ', '.join(content['errors']),
                    request.status_code,
                    request.content.decode())

        return content
