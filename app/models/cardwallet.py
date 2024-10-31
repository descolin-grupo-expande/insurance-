from app.extensions import db

class CardWallet(db.Model):

    """Docstring for CardWallet. """
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assistance_plan_id = db.Column(db.Integer, db.ForeignKey('assistance_plan.id'))
    foreground_color = db.Column(db.String(150))
    background_color = db.Column(db.String(150))
    label_color = db.Column(db.String(150))
    logo_text = db.Column(db.String(150))
    organization_name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    part_of_label = db.Column(db.String(150))
    attatchment_link = db.Column(db.String(255))
