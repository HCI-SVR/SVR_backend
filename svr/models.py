from svr import db


class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    group_id = db.Column(db.Integer, nullable=True)
    uri = db.Column(db.String(200), nullable=False)
    image_key = db.Column(db.String(200), nullable=True)
    singer = db.Column(db.String(100), nullable=False)
    preview_url = db.Column(db.String(200), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'group_id': self.group_id,
            'uri': self.uri,
            'image_key': self.image_key,
            'singer': self.singer,
            'preview_url': self.preview_url,
        }




