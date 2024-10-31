from functools import wraps
from flask import g, request
from app.config import config
import flask
from app import webserviceerror
from app.requestfilter.sorting import Sorting

def get_per_page():
    """TODO: Docstring for get_per_page.
    :returns: TODO
    """
    per_page = config.API_PER_PAGE
    if 'per_page' in flask.request.args:
        per_page = flask.request.args['per_page']
        try:
            per_page = int(per_page)
        except ValueError:
            # raise errors.ApiError('per_page should be integer', 400)
            raise webserviceerror.WebServiceError(
                400,
                message='per_page should be integer'
            )
        if per_page < 1:
            per_page = config.API_PER_PAGE
    return per_page


def get_page():
    """TODO: Docstring for get_page.
    :returns: TODO

    """
    page = 0
    if 'page' in flask.request.args:
        try:
            page = int(flask.request.args['page']) - 1
        except ValueError:
            raise webserviceerror.WebServiceError(
                400,
                message="page should be integer"
            )
        # raise errors.ApiError('page should be integer', 400)
        if page < 0:
            raise webserviceerror.WebServiceError(
                400,
                message="page can not be less then 1"
            )
        # raise errors.ApiError('page can not be less then 1')
    return page


def get_sorting(sort_rule):
    """TODO: Docstring for get_sorting.
    :returns: TODO

    """
    if not sort_rule:
        return []
    sort_values = sort_rule.split(',')
    sorting = []
    for sort_value in sort_values:
        if sort_value.startswith('-'):
            sorting.append(Sorting(field=sort_value[1:], desc=True))
        else:
            sorting.append(Sorting(field=sort_value, desc=False))
    return sorting

def get_filter(args, filter_fields, filter_converters):
    # Implementa tu lógica de filtros
    # Devuelve una expresión válida para SQLAlchemy
    pass

def get_options(args):
    # Implementa tu lógica para obtener opciones adicionales
    return {'all': args.get('all', 'false').lower() == 'true'}

def iterable(sort_fields=None, filter_fields=None, filter_converters=None):
    """Decorador para manejar paginación, filtros y ordenamiento."""
    filter_fields = filter_fields or []
    filter_converters = filter_converters or {}

    def wrapper(f):
        @wraps(f)
        def endpoint(*args, **kwargs):
            g.per_page = get_per_page()
            g.page = get_page()
            g.offset = g.page * g.per_page
            g.filter = get_filter(request.args, filter_fields, filter_converters)
            g.sorting = get_sorting(request.args.get('sort'))
            g.options = get_options(request.args)
            items, total = f(*args, **kwargs)
            return {
                'data': items,
                'total': total
            }

        return endpoint

    return wrapper
