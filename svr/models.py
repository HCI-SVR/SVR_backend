from svr import db

class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    group_id = db.Column(db.Integer, nullable=True)
    uri = db.Column(db.String(200), nullable=False)
    # count = db.Column(db.Integer, default=0)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'group_id': self.group_id,
            'uri': self.uri,
            # 'count': self.count,
        }




