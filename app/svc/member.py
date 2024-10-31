from app.extensions import db
from app import models as m
from app.svc import models as models_svc
from app.svc import update as update_svc
import copy

def create_edit(attr_dict):
    member = None

    is_member_new = False
    original_member = None

    if 'id' in attr_dict and attr_dict['id'] is not None:
        # Editing existing member
        member = db.session.get(m.Member,attr_dict['id'])
        print('Has Id')
    else:
        # Look the member by national id
        
        member = db.session.execute(db.select(m.Member).where(
            m.Member.country == attr_dict['country'],
            m.Member.national_id == str(attr_dict['national_id']).strip() if attr_dict['national_id'] else attr_dict['national_id']
        )).scalar()
        
    if not member:
        # If member not found, create it
        
        member = m.Member()
        is_member_new = True
    else:
        print('ya existe')
        # Member exists and is going to be updated
        original_member = copy.deepcopy(member)



    # Set member attributes based on attr_dict
    exclude_fields = [
        'id', 'facebook_uid', 'facebook_token',
        'google_uid', 'device_id'
    ]
    member = models_svc.set_attributes(
        member, attr_dict, exclude=exclude_fields
    )

    # Set as active
    member.status = m.Member.STATUS_ACTIVE

    if not is_member_new:
        # Save updates of members
        updates = update_svc.save_updates(
            original_member, member, m.Update.UPDATE_MEMBER ,
            exclude=exclude_fields
        )

    return member