# Unofficial Coinbase Python3 Client Library

An easy way to buy, send, and accept [bitcoin](http://en.wikipedia.org/wiki/Bitcoin) through the [Coinbase API](https://coinbase.com/docs/api/overview).

This library supports both the [API key authentication method](https://coinbase.com/docs/api/overview) and OAuth. The below examples use an API key - for instructions on how to use OAuth, see [OAuth Authentication](#oauth-authentication).

# About Resy

Resy is a mobile restaurant reservations app in beta on iOS and Android.  The app is for people who love eating at great restaurants but hate hassling for reservations.

The developers behind Resy are craftspeople that hold themselves and their peers to an extremely high but attainable standard for work product (code).  They ship constantly but never sacrifice code quality to meet a deadline.

The Resy application runs at AWS using python3, uWSGI, nginx, MySQL and [tinyAPI](https://github.com/mcmontero/tinyAPI).

If you're interested in working with us, please email jobs@resy.com.

## Installation

Obtain the latest version of the Coinbase PHP library with:

    git clone https://github.com/resy/coinbase_python3.git

Then, execute the following command:

    python3 setup.py install

## Usage

Start by [enabling an API Key on your account](https://coinbase.com/settings/api).

Next, create an instance of the client using the `Coinbase.with_api_key` method:

```python
import coinbase

coinbase = coinbase.Coinbase.with_api_key(coinbase_api_key, coinbase_api_secret)
```

Keeping your credentials safe is essential to maintaining good security.  Read more about the recommended [security practices](https://coinbase.com/docs/api/overview#security) provided by Coinbase.

Now you can call methods on `coinbase` similar to the ones described in the [API reference](https://coinbase.com/api/doc).  For example:

```python
balance = coinbase.get_balance()
print('Balance is ' + balance + ' BTC')
```

Currency amounts are returned as strings.

## Examples

### Get user information

```python
user = coinbase.get_user()
print(user['name'])
# 'User One'
print(user['email'])
# 'user1@example.com'
```

### Check your balance

```python
print(coinvase.get_balance() . ' BTC')
# '200.123 BTC'
```

### Send bitcoin

`def send_money(self, to, amount, notes=None, user_fee=None, amount_currency=None)`

```python
response = coinbase.send_money('user@example.com', '2')
print(response['success'])
# True
print(response['transaction']['status'])
# 'pending'
print(response['transaction']['id'])
# '518d8567ed3ddcd4fd000034'
```

The first parameter can also be a bitcoin address and the third parameter can be a note or description of the transaction.  Descriptions are only visible on Coinbase (not on the general bitcoin network).

```python
response = coinbase.send_money("mpJKwdmJKYjiyfNo26eRp4j6qGwuUUnw9x", "0.1", "thanks for the coffee!")
print(response['transaction']['notes'])
# 'thanks for the coffee!'
```

You can also send money in a number of currencies (see `get_currencies()`) using the fifth parameter.  The amount will be automatically converted to the correct BTC amount using the current exchange rate.

```python
response = coinbase.send_money("user@example.com", "2", amount_currency="CAD")
print(response['transaction']['amount']['amount'])
# '0.0169'
```

### Request bitcoin

This will send an email to the recipient, requesting payment, and give them an easy way to pay.

```python
response = coinbase.request_money('client@example.com', 50, "contractor hours in January (website redesign for 50 BTC)")
print(response['transaction']['request'])
# True
print(response['transaction']['id'])
# '501a3554f8182b2754000003'

response = coinbase.resend_request('501a3554f8182b2754000003)
print(response['success'])
# True

respoinse = coinbase.cancel_request('501a3554f8182b2754000003')
print(response['success'])
# True

// From the other account:
response = coinbase.complete_request('501a3554f8182b2754000003')
print(response['success'])
# True
```

### List your current transactions

Sorted in descending order by timestamp, 30 per page.  You can pass an integer as the first parameter to page through results, for example `coinbase.get_transactions(2)`.

```python
response = coinbase.get_transactions()
print(response['current_page'])
# 1
print(response['num_pages'])
# 2
print(response['transactions'][0]['id'])
# '5018f833f8182b129c00002f'
```

Transactions will always have an `id` attribute which is the primary way to identity them through the Coinbase api.  They will also have a `hsh` (bitcoin hash) attribute once they've been broadcast to the network (usually within a few seconds).

### Check bitcoin prices

Check the buy or sell price by passing a `quantity` of bitcoin that you'd like to buy or sell.  This price includes Coinbase's fee of 1% and the bank transfer fee of $0.15.

```python
print(coinbase.get_buy_price(1)
# '125.31'
print(coinbase.get_sell_price(1)
# '122.41'
```

### Buy or sell bitcoin

Buying and selling bitcoin requires you to [link and verify a bank account](https://coinbase.com/payment_methods) through the web interface first.

Then you can call `buy` or `sell` and pass a `quantity` of bitcoin you want to buy.

On a buy, we'll debit your bank account and the bitcoin will arrive in your Coinbase account four business days later (this is shown as the `payout_date` below).  This is how long it takes for the bank transfer to complete and verify, although we're working on shortening this window. In some cases, we may not be able to guarantee a price, and buy requests will fail. In that case, set the second parameter (`agree_btc_amount_varies`) to true in order to purchase bitcoin at the future market price when your money arrives.

On a sell we'll credit your bank account in a similar way and it will arrive within two business days.

```python
response = coinbase.buy(1.0)
print(response['transfer']['code'])
# '6H7GYLXZ'
print(response['transfer'][['btc']['amount'])
# '1.00000000'
print(response['transfer']['total']['amount'])
# '$17.95'
print(response['transfer']['payout_date'])
# '2013-02-01T18:00:00-08:00' (ISO 8601 format)
```

```python
response = coinbase.sell(1.0)
print(response['transfer']['code'])
# 'RD2OC8AL'
print(response['transfer']['btc']['amount'])
# '1.00000000'
print(response['transfer']['total']['amount'])
# '$17.95'
print(response['transfer']['payout_date'])
# '2013-02-01T18:00:00-08:00' (ISO 8601 format)
```

### Create a payment button

This will create the code for a payment button (and modal window) that you can use to accept bitcoin on your website.  You can read [more about payment buttons here and try a demo](https://coinbase.com/docs/merchant_tools/payment_buttons).

The method signature is `def create_button(self, name, price, currency, custom=None, options=None)`.  The `custom` parameter will get passed through in [callbacks](https://coinbase.com/docs/merchant_tools/callbacks) to your site.  The list of valid `options` [are described here](https://coinbase.com/api/doc/1.0/buttons/create.html).

```python
response = \
    coinbase.create_button(
        "Your Order #1234",
        "42.95",
        "EUR",
        "my custom tracking code for this order",
        {"description": "1 widget at €42.95"})
print(response['button']['code'])
# '93865b9cae83706ae59220c013bc0afd'
print(response['embed_html'])
# '<div class=\"coinbase-button\" data-code=\"93865b9cae83706ae59220c013bc0afd\"></div><script src=\"https://coinbase.com/assets/button.js\" type=\"text/javascript\"></script>'
```

### Exchange rates and currency utilties

You can fetch a list of all supported currencies and ISO codes with the `get_currencies()` method.

```python
currencies = coinbase.get_currencies()
print(currencies[0]['name'])
# 'Afghan Afghani (AFN)'
```

`get_exchange_rate()` will return a list of exchange rates. Pass two parameters to get a single exchange rate.

```python
rates = coinbase.get_exchange_rate()
print(rates['btc_to_cad'])
# '117.13892'
print(coinbase.get_exchange_rate('btc', 'cad'))
# '117.13892'
```

### Create a new user

```python
response = coinbase.create_user("newuser@example.com", "some password");
print(response['user']['email'])
# 'newuser@example.com'
print(response['user']['receive_address'])
# 'mpJKwdmJKYjiyfNo26eRp4j6qGwuUUnw9x'
```

A receive address is returned also in case you need to send the new user a payment right away.

### Get autocomplete contacts

This will return a list of contacts the user has previously sent to or received from. Useful for auto completion. By default, 30 contacts are returned at a time; use the `page` and `limit` parameters to adjust how pagination works.

```python
response = coinbase.get_contacts("exa");
print(', '.join(response['contacts']))
# 'user1@example.com, user2@example.com'
```

## Adding new methods

You can see a [list of method calls here](https://github.com/resy/coinbase_python3/blob/master/coinbase/__init__.py) and how they are implemented.  They are a wrapper around the [Coinbase JSON API](https://coinbase.com/api/doc).

If there are any methods listed in the [API Reference](https://coinbase.com/api/doc) that don't have an explicit function name in the library, you can also call `get`, `post`, `put`, or `delete` with a `path` and optional `params` array for a quick implementation.  The raw JSON object will be returned. For example:

```python
print(coinbase.get('/account/balance'))
# {
#   'amount': "0.56902981",
#   'current': "BTC"
# }
```

Or feel free to add a new wrapper method and submit a pull request.

## OAuth Authentication

To authenticate with OAuth, first create an OAuth application at https://coinbase.com/oauth/applications.  When a user wishes to connect their Coinbase account, redirect them to a URL created with `CoinbaseOAuth.create_authorize_url()`:

```python
coinbase_oauth = CoinbaseOAuth(client_id, client_secret, redirect_url)
```

You can then redirect using a "Location" header and the result from this call:

```python
coinbase_oauth.create_authorize_url('all')
```

After the user has authorized your application, they will be redirected back to the redirect URL specified above. A `code` parameter will be included - pass this into `get_tokens()` to receive a set of tokens:

```python
tokens = coinbase_oauth.get_tokens(code)
```

Store these tokens safely, and use them to make Coinbase API requests in the future. For example:

```python
coinbase = coinbase.Coinbase.with_oauth(access_token, refresh_token)
coinbase.get_balance()
```

## Simple API Key Authentication

This mechanism is deprecated and was not included in this library.  If it is essential for your implementation, please contact us.

## Security notes

If someone gains access to your API Key they will have complete control of your Coinbase account.  This includes the abillity to send all of your bitcoins elsewhere.

For this reason, API access is disabled on all Coinbase accounts by default.  If you decide to enable API key access you should take precautions to store your API key securely in your application.  How to do this is application specific, but it's something you should [research](http://programmers.stackexchange.com/questions/65601/is-it-smart-to-store-application-keys-ids-etc-directly-inside-an-application) if you have never done this before.
