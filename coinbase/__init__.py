# ----- License --------------------------------------------------------------

"""
Coinbase Python3 Client Library

AUTHOR

Michael Montero <mike@resy.com>
Github: resy / mcmontero

LICENSE (The MIT License)

Copyright (c) 2013 Michael Montero "mike@resy.com"

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# ----- Author ---------------------------------------------------------------

__author__ = 'Michael Montero <mike@resy.com>'

# ----- Imports --------------------------------------------------------------

from coinbase.config import COINBASE_ENDPOINT
from coinbase.models import CoinbaseAmount
from coinbase.models import CoinbaseError
from coinbase.models import CoinbaseOAuth2Request
from coinbase.models import CoinbasePaymentButton
from coinbase.models import CoinbaseRESTRequest
from coinbase.models import CoinbaseTransaction
from coinbase.models import CoinbaseTransfer
from coinbase.models import CoinbaseUser
from oauth2client.client import AccessTokenCredentialsError
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2Credentials

# ----- Public Classes --------------------------------------------------------

class CoinbaseAccount(object):
    '''
    Manages data and interactions for a Coinbase account.
    '''

    def __init__(self,
                 access_token = None,
                 refresh_token = None,
                 api_key=None,
                 api_secret=None):
        '''
        You must provide either access_token and refresh_token or api_key and
        api_secret.
        '''

        self.use_oauth2 = False
        if access_token and refresh_token:
            if type(access_token) is str:
                self.access_token = access_token
            else:
                raise RuntimeError('access_token must be a string.')

            if type(refresh_token) is str:
                self.refresh_token = refresh_token
            else:
                raise RuntimeError('refresh_token must be a string.')

            self.use_oauth2 = True
        elif api_key and api_secret:
            if type(api_key) is str:
                self.api_key = api_key
            else:
                raise RuntimeError('api_key must be a string.')

            if type(api_secret) is str:
                self.api_secret = api_secret
            else:
                raise RuntimeError('api_secret must be a string.')
        else:
            raise RuntimeError('Either provide access_token and refresh_token '
                               + 'or api_key and api_secret.')


    @property
    def balance(self):
        '''
        Retrieve the account's balance.
        '''

        results = \
            self.__execute_get_request(
                COINBASE_ENDPOINT + '/account/balance')

        return CoinbaseAmount(results['amount'], results['currency'])


    def buy_btc(self, qty, pricevaries=False):
        '''
        Purchases BitCoin from Coinbase in USD.
        '''

        results = \
            self.__execute_post_request(
                COINBASE_ENDPOINT + '/buys',
                {'qty': qty,
                 'agree_btc_amount_varies': pricevaries})

        return CoinbaseTransfer(results['transfer'])


    def buy_price(self, qty=1):
        '''
        Retrieves the buy price for BitCoin in USD.
        '''

        results = \
            self.__execute_get_request(
                COINBASE_ENDPOINT + '/prices/buy',
                {'qty': qty})

        return CoinbaseAmount(results['amount'], results['currency'])


    @property
    def contacts(self):
        '''
        Retrieves the account's contacts.
        '''

        results = \
            self.__execute_get_request(
                COINBASE_ENDPOINT + '/contacts')

        return [contact['contact'] for contact in results['contacts']]


    def create_button(self,
                      name,
                      price,
                      price_currency='BTC',
                      button_type='buy_now',
                      callback_url=None,
                      **kwargs):
        '''
        Creates a new payment button, page, or iframe.
        '''

        params = {
            "button": {
                "name": name,
                "price_string": str(price),
                "price_currency_iso": price_currency,
                "button_type": button_type
            }
        }

        if callback_url is not None:
            params['button']['callback_url'] = callback_url

        params['button'].update(kwargs)

        results = \
            self.__execute_post_request(
                COINBASE_ENDPOINT + '/buttons',
                params)

        return CoinbasePaymentButton(results['button'])


    def __execute_get_request(self, url, params=None):
        if self.use_oauth2:
            return \
                CoinbaseOAuth2Request(
                    self.access_token, self.refresh_token) \
                        .get(url, params)
        else:
            return \
                CoinbaseRESTRequest(
                    self.api_key, self.api_secret) \
                        .get(url, params)


    def __execute_post_request(self, url, params=None):
        if self.use_oauth2:
            return \
                CoinbaseOAuth2Request(
                    self.access_token, self.refresh_token) \
                        .post(url, params)
        else:
            return \
                CoinbaseRESTRequest(
                    self.api_key, self.api_secret) \
                        .post(url, params)


    def generate_receive_address(self, callback_url=None):
        '''
        Generates a new receive address.
        '''

        results = \
            self.__execute_post_request(
                COINBASE_ENDPOINT + '/account/generate_receive_address',
                {'address': {'callback_url': callback_url}})

        return results['address']


    def get_transaction(self, transaction_id):
        '''
        Retrieves details about a specific transaction.
        '''

        results = \
            self.__execute_get_request(
                COINBASE_ENDPOINT + '/transactions/' + str(transaction_id))

        return CoinbaseTransaction(results['transaction'])


    def get_user_details(self):
        '''
        Retrieves user details for this account.
        '''

        results = \
            self.__execute_get_request(
                COINBASE_ENDPOINT + '/users')

        user_details = results['users'][0]['user']

        balance = \
            CoinbaseAmount(
                user_details['balance']['amount'],
                user_details['balance']['currency'])
        buy_limit = \
            CoinbaseAmount(
                user_details['buy_limit']['amount'],
                user_details['buy_limit']['currency'])
        sell_limit = \
            CoinbaseAmount(
                user_details['sell_limit']['amount'],
                user_details['sell_limit']['currency'])

        user = \
            CoinbaseUser(
                user_id=user_details['id'],
                name=user_details['name'],
                email=user_details['email'],
                time_zone=user_details['time_zone'],
                native_currency=user_details['native_currency'],
                balance=balance,
                buy_level=user_details['buy_level'],
                sell_level=user_details['sell_level'],
                buy_limit=buy_limit,
                sell_limit=sell_limit)

        return user


    @property
    def receive_address(self):
        '''
        Retrieves the accounts's current receive address.
        '''

        results = \
            self.__execute_get_request(
                COINBASE_ENDPOINT + '/account/receive_address')

        return results['address']


    def request(self, from_email, amount, notes='', currency='BTC'):
        '''
        Requests that BitCoin be delivered to this account from an email
        address.
        '''

        if currency == 'BTC':
            params = {
                "transaction": {
                    "from": from_email,
                    "amount": amount,
                    "notes": notes
                }
            }
        else:
            params = {
                "transaction": {
                    "from": from_email,
                    "amount_string": str(amount),
                    "amount_currency_iso": currency,
                    "notes": notes
                }
            }

        results = \
            self.__execute_post_request(
                COINBASE_ENDPOINT + '/transactions/request_money',
                params)

        return CoinbaseTransaction(results['transaction'])


    def sell_btc(self, qty):
        '''
        Sells BitCoin to Coinbase for USD.
        '''

        results = \
            self.__execute_post_request(
                COINBASE_ENDPOINT + '/sells',
                {'qty': qty})

        return CoinbaseTransfer(results['transfer'])


    def sell_price(self, qty=1):
        '''
        Retrieves the sell price of BitCoin in USD.
        '''

        results = \
            self.__execute_get_request(
                COINBASE_ENDPOINT + '/prices/sell',
                {'qty': qty})

        return CoinbaseAmount(results['amount'], results['currency'])


    def send(self, to_address, amount, notes='', currency='BTC'):
        '''
        Sends BitCoin from this account to an email address or a BTC address.
        '''

        if currency == 'BTC':
            params = {
                "transaction": {
                    "to": to_address,
                    "amount": amount,
                    "notes": notes
                }
            }
        else:
            params = {
                "transaction": {
                    "to": to_address,
                    "amount_string": str(amount),
                    "amount_currency_iso": currency,
                    "notes": notes
                }
            }

        results = \
            self.__execute_post_request(
                COINBASE_ENDPOINT + '/transactions/send_money',
                params)

        return CoinbaseTransaction(results['transaction'])


    def transactions(self, count=30):
        '''
        Retrieves the list of transactions for this account.
        '''

        transactions = []
        for page in range(1, int(count / 30 + 1) + 1):
            results = \
                self.__execute_get_request(
                    COINBASE_ENDPOINT + '/transactions',
                    {'page': page})

            for transaction in results['transactions']:
                transactions.append(
                    CoinbaseTransaction(transaction['transaction']))

            if results['num_pages'] == page:
                break

        return transactions


    def transfers(self, count=30):
        '''
        Retrieves the list of transfers for this account.
        '''

        transfers = []
        for page in range(1, int(count / 30 + 1) + 1):
            results = \
                self.__execute_get_request(
                    COINBASE_ENDPOINT + '/transfers',
                    {'page': page})

            for transfer in results['transfers']:
                transfers.append(CoinbaseTransfer(transfer['transfer']))

            if results['num_pages'] == page:
                break

        return transfers
