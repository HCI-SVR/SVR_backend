from flask import jsonify, Blueprint, request
from svr import db
from svr.models import Music

bp = Blueprint('music', __name__, url_prefix="/music")

@bp.route('/all/')
def findall():
    music_list = Music.query.all()
    return jsonify([music.serialize() for music in music_list])


@bp.route('/insert/', methods=['POST'])
def insert():
    params = request.get_json()
    name = params['subject']
    group_id = params['group_id']
    uri = params['uri']
    image_key = params['image_key']
    singer = params['singer']


    music = Music(name=name, group_id = group_id,
                  uri=uri, image_key=image_key, singer=singer)
    db.session.add(music)
    db.session.commit()

    return jsonify(music)