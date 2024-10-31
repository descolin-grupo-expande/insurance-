from app.extensions import db

class EmailInfo(db.Model):

    """Docstring for EmailInfo. """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_email = db.Column(db.Unicode(255), nullable=True)
    subject = db.Column(db.Unicode(50), nullable=True)
    body_attachment_id = db.Column(db.Integer, db.ForeignKey('attachment.id'))
    policy_template_attachment_id = db.Column(db.Integer, db.ForeignKey('attachment.id'))
    sender_domain = db.Column(db.Unicode(60), nullable=True)
    
    policy_template_attachment = db.relationship('Attachment', foreign_keys=[policy_template_attachment_id])
    body_attachment = db.relationship('Attachment', foreign_keys=[body_attachment_id])



    def __repr__(self):
        """
        TODO: Docstring for __repr__.
        :return:TODO
        """
        return 'EmailInfo({})'.format(self.id)
