from flask import Blueprint, jsonify, request
from svr.models import Music
from svr import db

bp = Blueprint('rate', __name__, url_prefix="/rate")

count = {-1: 100}

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

    min_count = min(count.values())

    min_music_list = []
    for music_id in count.keys():
        if count[music_id] == min_count:
            min_music_list.append(music_id)
    min_music_list.sort()
    print(min_music_list)
    # if min_music_list:
    #     return jsonify(Music.query.get(min_music_list[1]).serialize())
    # else:
    #     return jsonify({})
    if min_music_list:
        selected_music = Music.query.get(min_music_list[1])
        return jsonify({
            "music": selected_music.serialize(),
            "count": count[selected_music.id]
        })
    else:
        return jsonify({})



    # count_list = [music.count for music in music_list]
    # count_list.sort()
    # count_min = count_list[0]
    # music_list_min = [music for music in music_list if music.count == count_min]
    # return jsonify([music.serialize() for music in music_list_min])
    # return jsonify(music_list_min[0].serialize())
    # return str(count_min)

# @bp.route('/count/')
# def show_count():
