# ----- Author ---------------------------------------------------------------

__author__ = 'Michael Montero <mike@resy.com>'

# ----- Public Classes --------------------------------------------------------

class CoinbasePaymentButton(object):

    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)
