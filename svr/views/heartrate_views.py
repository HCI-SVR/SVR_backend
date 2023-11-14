from flask import Flask, Blueprint, jsonify, request
from svr.models import Music
from svr import db

bp = Blueprint('rate', __name__, url_prefix="/rate")
count = {-1: 1}

@bp.route('/<int:heartrate>/')
def musicList(heartrate):
    if heartrate < 120:
        group_id = 1
    elif heartrate < 140:
        group_id = 2
    elif heartrate < 160:
        group_id = 3
    elif heartrate < 180:
        group_id = 4
    else:
        group_id = 5
    music_list = Music.query.all()
    music_list = [music for music in music_list if music.group_id == group_id]
    for music in music_list:
        if music.id in count.keys():
            count[music.id] += 1
        else:
            count[music.id] = 1

    # count_list = [music.count for music in music_list]
    # count_list.sort()
    # count_min = count_list[0]
    # music_list_min = [music for music in music_list if music.count == count_min]
    # return jsonify([music.serialize() for music in music_list_min])
    # return jsonify(music_list_min[0].serialize())
    # return str(count_min)


@bp.route('/all/')
def allmusic():
    music_list = Music.query.all()
    return jsonify([music.serialize() for music in music_list])


@bp.route('/insert/', methods=['POST'])
def insert():
    params = request.get_json()
    name = params['subject']
    group_id = params['group_id']
    uri = params['uri']
    count = params['count']

    music = Music(name=name, group_id = group_id,
                  uri=uri, count=count)
    db.session.add(music)
    db.session.commit()

    return jsonify(music)