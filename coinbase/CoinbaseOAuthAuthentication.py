# ----- Author ----------------------------------------------------------------

__author__ = 'Michael Montero <mike@resy.com>'

# ----- Imports ---------------------------------------------------------------

from .CoinbaseAuthentication import CoinbaseAuthentication

# ----- Public Classes --------------------------------------------------------

class CoinbaseOAuthAuthentication(CoinbaseAuthentication):
    '''
    Implements the authentication mechanism that uses an access token and a
    refresh token.
    '''

    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token


    def get_data(self):
        return {
            'access_token': self.api_key,
            'refresh_token': self.api_secret
        }
