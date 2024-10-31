from flask import g, current_app
from app.extensions import db

def get_default_iterator(model):
    """Devuelve un iterador por defecto para el modelo especificado."""
    
    query = db.session.query(model)

    # Aplicar filtros si están definidos
    if g.filter is not None:
        query = query.filter(g.filter)
    
    # Verificar si hay un orden válido
    if g.sorting and len(g.sorting) > 0:
        query = query.order_by(g.sorting)
    else:
        # Aquí podrías definir un orden por defecto si es necesario
        # query = query.order_by(model.default_column)
        pass

    print(query)

    if g.options.get('all', False):
        items = query.limit(current_app.config['ALL_LIMIT']).all()
        return [serialize_model(item) for item in items], len(items)
    else:
        # Ajusta la llamada a paginate
        pagination = query.paginate(page=g.page + 1, per_page=g.per_page, error_out=False)
        return [serialize_model(item) for item in pagination.items], pagination.total


def serialize_model(model):
    """Convierte un modelo de SQLAlchemy en un diccionario."""
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}
