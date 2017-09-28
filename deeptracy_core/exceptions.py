
class DeeptracyException(Exception):

    def __init__(self, message, status_code=None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.api_status_code = status_code
