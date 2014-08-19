__author__ = 'mhluongo'

class CoinbasePaymentButton(object):

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

