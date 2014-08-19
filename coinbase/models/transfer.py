# ----- Author ----------------------------------------------------------------

__author__ = 'Michael Montero <mike@resy.com>'

# ----- Imports ---------------------------------------------------------------

from .amount import CoinbaseAmount

# ----- Public Classes --------------------------------------------------------

class CoinbaseTransfer(object):

    def __init__(self, transfer):
        self.type = \
            transfer['type']
        self.code = \
            transfer['code']
        self.created_at = \
            transfer['created_at']
        self.fees_coinbase = \
            CoinbaseAmount(
                transfer['fees']['coinbase']['cents'],
                transfer['fees']['coinbase']['currency_iso'])
        self.fees_bank = \
            CoinbaseAmount(
                transfer['fees']['bank']['cents'],
                transfer['fees']['bank']['currency_iso'])
        self.payout_date = \
            transfer['payout_date']
        self.transaction_id = \
            transfer.get('transaction_id','')
        self.status = \
            transfer['status']
        self.btc_amount = \
            CoinbaseAmount(
                transfer['btc']['amount'],
                transfer['btc']['currency'])
        self.subtotal_amount = \
            CoinbaseAmount(
                transfer['subtotal']['amount'],
                transfer['subtotal']['currency'])
        self.total_amount = \
            CoinbaseAmount(
                transfer['total']['amount'],
                transfer['total']['currency'])
        self.description = \
            transfer.get('description','')
