__author__ = 'kroberts'

class CoinbaseError(Exception):

    def __init__(self, errorList):
        self.error = errorList
