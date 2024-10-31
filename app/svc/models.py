from app.extensions import db
import re

def set_attributes(instance, attr_dict, include=[], exclude=[]):
    if include and len(include) > 0:
        fields = include
    else:
        # From object get which model it is
        model = instance.__class__
        # Get fields to set
        fields = model_get_attr(model, exclude=exclude)
    
    print(fields)
    for field in fields:
        if field in attr_dict:
            setattr(instance, field, attr_dict[field])

    return instance

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