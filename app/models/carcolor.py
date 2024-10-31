from app.extensions import db

class CarColor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    language = db.Column(db.Unicode(5), primary_key=True)

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'CarColor({})'.format(self.id)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }