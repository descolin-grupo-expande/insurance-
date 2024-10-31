# -*- coding: utf-8 -*-
"""
"""
import re
import os
from app.extensions import db
from app.utils.code import gen_code
from app.config import config

def check_full_token(full_token):
    """ Return True or False """
    full_token_re = re.compile(r'^[0-9]+\..+$')
    return bool(full_token_re.match(full_token))

def gen_token():
    """ Return generated token"""
    TOKEN_SYMBOLS = config.TOKEN_CONTENT
    TOKEN_LENGTH = 300
    token = gen_code(TOKEN_SYMBOLS, TOKEN_LENGTH)
    return token

def model_get_attr(model, exclude=[]):
    columnsStr = []

    try:
        inst = db.inspect(model)
        #columnsObj = model.__table__.columns
        columnsObj = [c_attr.key for c_attr in inst.mapper.column_attrs]
        for col in columnsObj:
            col_name = re.sub('^[^A-Za-z]*', '', col) #any non alphabets starting from the beginning of the string will be removed.
            if col_name not in exclude:
                columnsStr.append(col_name)
    except Exception as e:
        print (str(e))

    return columnsStr

def set_attributes_to_from(to_object, from_object, attributes):
    """description: Set the attributes of an object from an object
    :returns: object with setted attributes
    """
    for attribute in attributes:
        setattr(to_object, attribute, getattr(from_object, attribute))

    return to_object

def get_request_ip():
    """Return IP of client request"""
    return os.environ.get("REMOTE_ADDR")

def get_user_agent(request):
    """Return the browser info"""
    if request and request.headers:
        return request.headers.get('User-Agent')

    return None