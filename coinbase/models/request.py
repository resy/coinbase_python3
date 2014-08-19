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

class CoinbaseOAuth2Request(object):
    '''
    Simplify API requests being made with OAuth2 credentials.
    '''

    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token


    def get(self, url, params=None):
        session = requests.session()
        session.headers.update({'Content-Type': 'application/json'})

        if params is None:
            params = {}

        params['access_token'] = self.access_token

        return self.__handle_coinbase_error(
                session.get(url, params=params)
                    .json())


    def __handle_coinbase_error(self, response):
        if 'error' in response:
            raise CoinbaseError(response['error'])
        elif 'success' in response and response['success'] == False:
            raise CoinbaseError(response['errors'])

        return response


    def post(self, url, params=None):
        session = requests.session()
        session.headers.update({'Content-Type': 'application/json'})

        if params is None:
            params = {}

        params['access_token'] = self.access_token

        return self.__handle_coinbase_error(
                session.post(url, data=json.dumps(params))
                    .json())


class CoinbaseRESTRequest(object):
    '''
    Simplify API requests being made with an API key and secret.
    '''

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret


    def get(self, url, params=None):
        session = requests.session()
        session.headers.update({'Content-Type': 'application/json'})

        query_string = ''
        if params is not None:
            query_string = '?' + urllib.parse.urlencode(params)

        nonce, signature = self.__get_nonce_and_signature(url + query_string)

        session.headers.update({
            'ACCESS_KEY': self.api_key,
            'ACCESS_SIGNATURE': signature,
            'ACCESS_NONCE': nonce,
            'Accept': 'application/json'
        })

        return self.__handle_coinbase_error(
                session.get(url, params=params)
                    .json())


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


    def __handle_coinbase_error(self, response):
        if 'error' in response:
            raise CoinbaseError(response['error'])
        elif 'success' in response and response['success'] == False:
            raise CoinbaseError(response['errors'])

        return response


    def post(self, url, params=None):
        session = requests.session()
        session.headers.update({'Content-Type': 'application/json'})

        body = ''
        if params is not None:
            body = json.dumps(params)

        nonce, signature = self.__get_nonce_and_signature(url + body)

        session.headers.update({
            'ACCESS_KEY': self.api_key,
            'ACCESS_SIGNATURE': signature,
            'ACCESS_NONCE': nonce,
            'Accept': 'application/json'
        })

        return self.__handle_coinbase_error(
                session.post(url, data=json.dumps(params))
                    .json())
