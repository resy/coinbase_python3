# ----- Author ----------------------------------------------------------------

__author__ = 'Michael Montero <mike@resy.com>'

# ----- Imports ---------------------------------------------------------------

from .CoinbaseAuthentication import CoinbaseAuthentication

# ----- Public Classes --------------------------------------------------------

class CoinbaseAPIKeyAuthentication(CoinbaseAuthentication):
    '''
    Implements the authentication mechanism that uses the API key and secret.
    '''

    def __init__(self, key, secret):
        self.api_key = key
        self.api_secret = secret


    def get_data(self):
        return {
            'api_key': self.api_key,
            'api_secret': self.api_secret
        }
