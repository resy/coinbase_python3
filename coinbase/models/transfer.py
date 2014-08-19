__author__ = 'pmb6tz'

from amount import CoinbaseAmount

class CoinbaseTransfer(object):

    def __init__(self, transfer):
        self.type = transfer['type']
        self.code = transfer['code']
        self.created_at = transfer['created_at']

        fees_coinbase_cents = transfer['fees']['coinbase']['cents']
        fees_coinbase_currency_iso = transfer['fees']['coinbase']['currency_iso']
        self.fees_coinbase = CoinbaseAmount(fees_coinbase_cents, fees_coinbase_currency_iso)

        fees_bank_cents = transfer['fees']['bank']['cents']
        fees_bank_currency_iso = transfer['fees']['bank']['currency_iso']
        self.fees_bank = CoinbaseAmount(fees_bank_cents, fees_bank_currency_iso)

        self.payout_date = transfer['payout_date']
        self.transaction_id = transfer.get('transaction_id','')
        self.status = transfer['status']

        btc_amount = transfer['btc']['amount']
        btc_currency = transfer['btc']['currency']
        self.btc_amount = CoinbaseAmount(btc_amount, btc_currency)

        subtotal_amount = transfer['subtotal']['amount']
        subtotal_currency = transfer['subtotal']['currency']
        self.subtotal_amount = CoinbaseAmount(subtotal_amount, subtotal_currency)

        total_amount = transfer['total']['amount']
        total_currency = transfer['total']['currency']
        self.total_amount = CoinbaseAmount(total_amount, total_currency)

        self.description = transfer.get('description','')

    def refresh(self):
        pass
        #TODO:  Refresh the transfer

    def cancel(self):
        pass
        #TODO:  Cancel the transfer if possible

    def complete(self):
        pass
        #TODO:  Approve the transfer if possible

    def resend(self):
        pass
        #TODO:  Resend the transfer email if possible