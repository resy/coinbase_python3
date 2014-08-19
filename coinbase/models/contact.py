# ----- Author ----------------------------------------------------------------

__author__ = 'Michael Montero <mike@resy.com>'

# ----- Public Classes --------------------------------------------------------

class CoinbaseContact(object):

    def __init__(self, contact_id=None, name=None, email=None):
        self.id = contact_id
        self.name = name
        self.email = email
