# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

class WebServiceError(Exception):

    """Docstring for ApiError. """

    def __init__(self, code, message=None, errors=None):
        """TODO: to be defined1.

        :message: TODO
        :code: TODO
        :messages: TODO

        """
        self.message = message
        self.code = code
        self.errors = errors

        if message == None and errors != None:
            self.message = str(errors)

        Exception.__init__(self, message)
