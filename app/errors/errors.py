class ApiError(Exception):

    """Docstring for ApiError. """

    def __init__(self, message, error_code, messages=None):
        """TODO: to be defined1.

        :message: TODO
        :error_code: TODO
        :messages: TODO

        """
        Exception.__init__(self, message)
        self.message = message
        self.error_code = error_code
        self.messages = messages

unauthorized_error = ApiError('Unauthorized', 401)
bad_request_error = ApiError('Bad Request', 400)
client_exist = ApiError('Client exist', 400)
forbidden_error = ApiError('Forbidden', 403)
not_found_error = ApiError('Not Found', 404)
invalid_client = ApiError('invalid_client', 400)