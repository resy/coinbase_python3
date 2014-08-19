__author__ = 'kroberts'


class CoinbaseError(object):

    def __init__(self, errorList):
        self.error = errorList
