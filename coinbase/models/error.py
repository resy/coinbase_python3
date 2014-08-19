# ----- Author ---------------------------------------------------------------

__author__ = 'mcmontero'

# ----- Public Classes --------------------------------------------------------

class CoinbaseError(Exception):

    def __init__(self, errorList):
        self.error = errorList
