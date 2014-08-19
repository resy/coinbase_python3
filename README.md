Unofficial Unofficial Coinbase Python3 Library
==============================================

This is a simple port to python3 based on the original work of:

    https://github.com/sibblegp

You can get a python3 compatible version of oauth2client, required for this
library, here:

    https://github.com/pferate/oauth2client/tree/python3

Unofficial Coinbase Python Library
==================================

Python Library for the Coinbase API for use with three legged oAuth2 and classic API key usage

[![Travis build status](https://travis-ci.org/sibblegp/coinbase_python.png?branch=master)](https://travis-ci.org/sibblegp/coinbase)

## Version

0.2.0

## Requirements
- [Coinbase Account](http://www.coinbase.com)
- [Requests](http://docs.python-requests.org/en/latest/)
- [oauth2client](https://developers.google.com/api-client-library/python/guide/aaa_oauth)

## Installation

Automatic installation using [pip](http://pypi.python.org/pypi):

    pip install coinbase

## Usage

```python
from coinbase import CoinbaseAccount
account = CoinbaseAccount(JSON_OAUTH2_TOKEN)
transaction = account.send('gsibble@gmail.com', 1.0)
print transaction.status
```

## Examples / Quickstart

This repo includes an example.py file which demonstrates:

* Creating the Account object
* Sending BitCoin
* Requesting BitCoin
* Getting the account's balance
* Getting the buy/sell price of BitCoin at CoinBase
* Listing historical transactions

It also includes a small webserver in the coinbase_oauth2 module which demonstrates how to obtain an oauth2 token.

## Methods

More documentation coming soon.

## Changelog

0.2.1

* Updated SSL Certs
* Added payment button support

0.2.0

* Push many updates to PyPi

0.1.0-7

* Fix SSL Certificates

0.1.0-5

* Set flag for token status when initializing
* Raise error if transaction fails

0.1.0-4

* User Details unittest
* Small tweaks

0.1.0-3

* Get User Details
* Refactor some attribute capitalization

0.1.0-2

* Generate New Receive Address

0.1.0

* Initial Commit

## Contributing

Contributions are greatly appreciated.  Please make all requests using built in issue tracking at GitHub.

## Credits

- George Sibble &lt;gsibble@gmail.com&gt;

## License

(The MIT License)

Copyright (c) 2013 George Sibble &lt;gsibble@gmail.com&gt;

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
