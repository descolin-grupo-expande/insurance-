from app.extensions import db
from app import models as m
from app.utils.functions import model_get_attr, get_request_ip, get_user_agent
from flask import g, request

def save_updates(original, modified, update_type, exclude=[], include=[]):
    # Get class from both validate
    original_class = original.__class__

    modified_class = modified.__class__

    if original_class != modified_class:
        return []

    # Get fields to be checked as updated
    if include and len(include) > 0:
        attr_names = include
    else:
        attr_names = model_get_attr(modified_class, exclude=exclude)
    
    user_id = None
    if 'current_user' in g:
        user_id = g.current_user.id

    updates = []
    for attr_name in attr_names:
        original_value = getattr(original, attr_name)
        modified_value = getattr(modified, attr_name)

        # Compare str attributes, since str is going to be saved on db
        if str(original_value) != str(modified_value):
            update = m.TableUpdate(
                type=update_type,
                user_id=user_id,
                item_id=modified.id,
                item_name=attr_name,
                update_agent=get_user_agent(request),
                update_ip=get_request_ip(),
                value_old=original_value,
                value_new=modified_value
            )
            updates.append(update)
            db.session.add(update)
    
    return updates