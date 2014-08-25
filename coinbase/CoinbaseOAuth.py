# ----- Author ----------------------------------------------------------------

__author__ = 'Michael Montero <mike@resy.com>'

# ----- Imports ---------------------------------------------------------------

from .error import CoinbaseAPIException

import json
import requests
import urllib.parse

# ----- Public Classes --------------------------------------------------------

class CoinbaseOAuth(object):
    '''
    Handles client OAuth functionality like authorizing a user's account to be
    accessed.
    '''

    def __init__(self, client_id, client_secret, redirect_uri):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__redirect_uri = redirect_uri


    def create_authorize_url(self, scope=tuple()):
        params = {
            'response_type': 'code',
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'redirect_uri': self.__redirect_uri,
        }

        for i in range(len(scope)):
            scope[i] = urllib.parse.quote_plus(scope[i])

        params = urllib.parse.urlencode(params) + 'scope=' + '+'.join(scope)

        return 'https://coinbase.com/oauth/authorize?' + params


    def get_tokens(self, code, grant_type='authorization_code'):
        params = {
            'grant_type': grant_type,
            'redirect_uri': self.__redirect_uri,
            'client_id': self.__client_id,
            'client_secret': self.__client_secret
        }

        if grant_type == 'refresh_token':
            params['refresh_token'] = code
        else:
            params['code'] = code

        request = \
            requests.post(
                'https://coinbase.com/oauth/token',
                data=params)

        if request.status_code != 200:
            raise CoinbaseAPIException(
                    'Could not get tokens - code',
                    request.status_code,
                    request.content.decode())

        return json.loads(request.content.decode())


    def refresh_tokens(self, refresh_token):
        return self.get_tokens(refresh_token, 'refresh_token')
