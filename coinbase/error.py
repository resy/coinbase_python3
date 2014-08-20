# ----- Author ----------------------------------------------------------------

__author__ = 'Michael Montero <mike@resy.com>'

# ----- Public Classes --------------------------------------------------------

class CoinbaseException(Exception):

    def __init__(self, message, http_code=None, response=None):
        self.message = message
        self.http_code = http_code
        self.response = response


    def get_http_code(self):
        return self.http_code


    def get_message(self):
        return self.message


    def get_response(self):
        return self.response


class CoinbaseAPIException(CoinbaseException):
    pass
