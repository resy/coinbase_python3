# ----- Author ----------------------------------------------------------------

__author__ = 'Michael Montero <mike@resy.com>'

# ----- Imports ---------------------------------------------------------------

from .CoinbaseAPIKeyAuthentication import CoinbaseAPIKeyAuthentication
from .CoinbaseOAuth import CoinbaseOAuth
from .CoinbaseOAuthAuthentication import CoinbaseOAuthAuthentication
from .CoinbaseRPC import CoinbaseRPC
from .error import CoinbaseAPIException
from .error import CoinbaseException

# ----- Public Classes --------------------------------------------------------

class Coinbase(object):
    '''
    Manages all data and interactions with the Coinbase API.
    '''

    @staticmethod
    def with_api_key(key, secret):
        return Coinbase(
                CoinbaseAPIKeyAuthentication(
                    key, secret))


    @staticmethod
    def with_oauth(access_token, refresh_token):
        return Coinbase(
                CoinbaseOAuthAuthentication(
                    access_token, refresh_token))


    def __init__(self, authentication):
        self.__authentication = authentication
        self.__rpc = CoinbaseRPC(self.__authentication)


    def buy(self, amount, agree_btc_amount_varies=False):
        params = {
            'qty': amount,
            'agree_btc_amount_varies': agree_btc_amount_varies
        }

        return self.post('/buys', params)


    def cancel_request(self, id):
        return self.delete('/transactions/' + id + '/cancel_request')


    def complete_request(self, id):
        return self.put('/transactions/' + id + '/complete_request')


    def create_button(self, name, price, currency, custom=None, options=None):
        params = {
            'name': name,
            'price_string': str(price),
            'price_currency_iso': currency
        }

        if custom is not None:
            params['custom'] = custom

        if options is not None:
            for key, value in operation.items():
                params[key] = value

        return self.create_button_with_options(params)


    def create_button_with_options(self, options=None):
        response = self.post('/buttons', {'button': options})

        if response['success'] == False:
            return response

        return {
            'button': response['button'],
            'embed_html': '<div class="coinbase-button" data-code="'
                          + response['button']['code']
                          + '></div><script src="https://coinbase.com/assets/'
                          + 'button.js" type="text/javascript"></script>',
            'success': True
        }


    def create_order_from_button(self, button_code):
        return self.post('/buttons/' + button_code + '/create_order')


    def create_user(self, email, password):
        params = {
            'user': {
                'email': email,
                'password': password
            }
        }

        return self.post('/users', params)


    def delete(self, path, params=None):
        return self.__rpc.request('DELETE', path, params)


    def generate_receive_address(self, callback=None, label=None):
        params = {}
        if callback is not None:
            params['callback'] = callback

        if label is not None:
            params['label'] = label

        return self.post('/account/generate_receive_address', params)['address']


    def get(self, path, params=None):
        return self.__rpc.request('GET', path, params)


    def get_all_addresses(self, query=None, page=0, limit=None):
        params = {}
        if query is not None:
            params['query'] = query

        if limit is not None:
            params['limit'] = limit

        return self.__get_paginated_resource(
                '/addresses', 'addresses', 'address', page, params)


    def get_balance(self):
        return self.get('/account/balance')['amount']


    def get_buy_price(self, qty=1):
        return self.get('/prices/buy', {'qty': qty})['amount']


    def get_contacts(self, query=None, page=0, limit=None):
        params = {
            'page': page
        }

        if query is not None:
            params['query'] = query

        if limit is not None:
            params['limit'] = limit

        result = self.get('/contacts', params)

        contacts = []
        for contact in results:
            if len(contact['email'].strip()) > 0:
                contacts.append(contact['email'].strip())

        return {
            'total_count': result['total_count'],
            'num_pages': result['num_pages'],
            'current_page': result['current_page'],
            'contacts': contacts
        }


    def get_currencies(self):
        result = self.get('/currencies')

        currencies = []
        for currency in result:
            currencies.append({
                'name': currency[0],
                'iso': currency[1]
            })

        return currencies


    def get_exchange_rate(self, from_=None, to=None):
        result = self.get('/currencies/exchange_rates')

        if from_ is not None and to is not None:
            return result[from_ + '_to_' + to]
        else:
            return result


    def get_order(self, id):
        return self.get('/orders/' + id)


    def get_orders(self, page=0):
        return self.__get_paginated_resource('/orders', 'orders', 'order', page)


    def __get_paginated_resource(self,
                                 resource,
                                 list_element,
                                 unwrap_element,
                                 page=0,
                                 params=None):
        if params is None:
            params = {}

        params['page'] = page

        result = self.get(resource, params)
        elements = []
        for element in result[list_element]:
            elements.append(element[unwrap_element])

        return {
            'total_count': result['total_count'],
            'num_pages': result['num_pages'],
            'current_page': result['current_page'],
            list_element: elements
        }


    def get_receive_address(self):
        return self.get('/account/receive_address')['address']


    def get_sell_price(self, qty=1):
        return self.get('/prices/sell', {'qty': qty})['amount']


    def get_transaction(self, id):
        return self.get('/transactions/' + id)


    def get_transactions(self, page=0):
        return self.__get_paginated_resource(
                '/transactions', 'transactions', 'transaction', page)


    def get_transfers(self, page=0):
        return self.__get_paginated_resource(
                '/transfers', 'transfers', 'transfer', page)


    def get_user(self):
        return self.get('/users')['users'][0]['user']


    def order(self, name, type_, price, price_currency_iso='USD'):
        params = {
            'button': {
                'name': name,
                'type': type_,
                'price_string': str(price),
                'price_currency_iso': price_currency_iso
            }
        }

        return self.post('/api/v1/orders', params)


    def post(self, path, params=None):
        return self.__rpc.request('POST', path, params)


    def put(self, path, params=None):
        return self.__rpc.request('PUT', path, params)


    def refund(self, transaction_id, refund_iso_code='BTC'):
        return self.__post('/orders/' + str(transaction_id) + '/refund',
                           {'order': {'refund_iso_code': refund_iso_code}})


    def request_money(self, from_, amount, notes, amount_currency):
        params = {
            'transaction': {
                'from': from_
            }
        }

        if amount_currency is not None:
            params['transaction']['amount_string'] = str(amount)
            params['transaction']['amount_currency_iso'] = amount_currency
        else:
            params['transaction']['amount'] = str(amount)

        if notes is not None:
            params['transaction']['notes'] = notes

        return self.post('/transactions/request_money', params)


    def resend_request(self, id):
        return self.put('/transactions/' + id + '/resend_request')


    def sell(self, amount):
        return self.post('/sells', {'qty': amount})


    def send_money(self,
                   to,
                   amount,
                   notes=None,
                   user_fee=None,
                   amount_currency=None):
        params = {
            'transaction': {
                'to': to
            }
        }

        if amount_currency is not None:
            params['transaction']['amount_string'] = str(amount)
            params['transaction']['amount_current_iso'] = amount_currency
        else:
            params['transaction']['amount'] = str(amount)

        if notes is not None:
            params['transaction']['notes'] = notes

        if user_fee is not None:
            params['transaction']['user_fee'] = user_fee

        return self.post('/transactions/send_money', params)
