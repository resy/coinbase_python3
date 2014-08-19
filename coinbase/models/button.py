# ----- Author ---------------------------------------------------------------

__author__ = 'mcmontero'

# ----- Public Classes --------------------------------------------------------

class CoinbasePaymentButton(object):

    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)
