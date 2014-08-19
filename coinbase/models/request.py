# ----- Credits ---------------------------------------------------------------

__author__ = 'Michael Montero <mike@resy.com>'

# ----- Imports ---------------------------------------------------------------

from coinbase.models import CoinbaseError

import hashlib
import hmac
import json
import requests
import time
import urllib.parse

# ----- Public Classes --------------------------------------------------------

class CoinbaseBaseRequest(object):
    '''
    Base class for request handlers.
    '''

    def _handle_coinbase_errors(self, request):
        if request.status_code != 200 and request.status_code != 201:
            content = request.content.decode()

            raise CoinbaseError(
                '(' + str(request.status_code) + '): '
                + ('N/A' if len(content) == 0 or content == ' ' else content))

        response = json.loads(request.content.decode())

        if 'error' in response:
            raise CoinbaseError(response['error'])
        elif 'success' in response and response['success'] == False:
            raise CoinbaseError(response['errors'][0])

        return response


class CoinbaseOAuth2Request(CoinbaseBaseRequest):
    '''
    Simplify API requests being made with OAuth2 credentials.
    '''

    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_was_refreshed = False


    def get(self, url, params=None):
        if params is None:
            params = {}

        params['access_token'] = self.access_token

        return self._handle_coinbase_errors(requests.get(url, params=params))


    def post(self, url, params=None):
        if params is None:
            params = {}

        params['access_token'] = self.access_token

        return self._handle_coinbase_errors(requests.post(url, data=params))


class CoinbaseRESTRequest(CoinbaseBaseRequest):
    '''
    Simplify API requests being made with an API key and secret.
    '''

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret


    def get(self, url, params=None):
        query_string = ''
        if params is not None:
            query_string = '?' + urllib.parse.urlencode(params)

        nonce, signature = self.__get_nonce_and_signature(url + query_string)

        headers = {
            'ACCESS_KEY': self.api_key,
            'ACCESS_SIGNATURE': signature,
            'ACCESS_NONCE': nonce,
            'Accept': 'application/json'
        }

        return self._handle_coinbase_errors(
                requests.get(url, params=params, headers=headers))


    def __get_nonce_and_signature(self, message):
        nonce = \
            int(time.time() * 1e6)
        message = \
            str(nonce) + message
        signature = \
            hmac.new(
                self.api_secret.encode(),
                message.encode(),
                hashlib.sha256) \
            .hexdigest()

        return nonce, signature


    def post(self, url, params=None):
        body = ''
        if params is not None:
            body = urllib.parse.urlencode(params)

        nonce, signature = self.__get_nonce_and_signature(url + body)

        headers = {
            'ACCESS_KEY': self.api_key,
            'ACCESS_SIGNATURE': signature,
            'ACCESS_NONCE': nonce,
            'Accept': 'application/json'
        }

        return self._handle_coinbase_errors(
                requests.post(url, data=params, headers=headers))
