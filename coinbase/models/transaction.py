# ----- Author ----------------------------------------------------------------

__author__ = 'Michael Montero <mike@resy.com>'

# ----- Imports ---------------------------------------------------------------

from .amount import CoinbaseAmount
from .contact import CoinbaseContact

# ----- Public Classes --------------------------------------------------------

class CoinbaseTransaction(object):

    def __init__(self, transaction):
        self.transaction_id = \
            transaction['id']
        self.created_at = \
            transaction['created_at']
        self.notes = \
            transaction['notes']
        self.amount = \
            CoinbaseAmount(
                transaction['amount']['amount'],
                transaction['amount']['currency'])
        self.status = \
            transaction['status']
        self.request = \
            transaction['request']

        self.sender = None
        if 'sender' in transaction:
            self.sender = \
                CoinbaseContact(
                    contact_id = transaction['sender'].get('id', None),
                    name = transaction['sender'].get('name', None),
                    email = transaction['sender'].get('email', None))

        self.recipient = None
        self.recipient_address = None
        self.recipient_type = None
        if 'recipient' in transaction:
            self.recipient = \
                CoinbaseContact(
                    contact_id = transaction['recipient'].get('id', None),
                    name = transaction['recipient'].get('name', None),
                    email = transaction['recipient'].get('email', None))
            self.recipient_address = \
                None
            self.recipient_type = \
                'CoinBase'
        elif 'recipient_address' in transaction:
            self.recipient = None
            self.recipient_address = transaction['recipient_address']
            self.recipient_type = 'Bitcoin'
