from flask import Blueprint, jsonify, request
from svr.models import Music
import pandas as pd

bp = Blueprint('rate', __name__, url_prefix="/rate")

count = {}
# 노래 재생 횟수 딕셔너리(key: music_id, value: count)

# df = pd.read_csv("../resources/heartrate_seconds_merged.csv")

@bp.route('/<int:heartrate>/')
def music(heartrate):
    # 심박수 그룹화
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

    music_list = (Music.query.filter_by(group_id=group_id)
                  .order_by(Music.id).all())
    # music_list = Music.query.all().order_by(Music.id)
    # music_list = [music for music in music_list if music.group_id == group_id]  # 그룹 노래 꺼내오기



    # 재생되지 않은 노래가 있으면 그 노래를 선택하고 for문 break
    selected_music = None
    for music in music_list:
        if music.id not in count.keys():
            selected_music = music
            count[selected_music.id] = 1
            break

    # 재생되지 않는 노래가 있으면 노래 재생
    if selected_music:
        return jsonify(
            {
                "music": selected_music.serialize(),
                "count": count
            })


    min_count = min(count.values())
    min_music_list = []
    for music_id in count.keys():
        if count[music_id] == min_count:
            min_music_list.append(music_id)

    min_music_list.sort()

    if min_music_list:
        selected_music = Music.query.get(min_music_list[0])
        count[selected_music.id] += 1
        return jsonify({
            "music": selected_music.serialize(),
            "count": count
        })
    else:
        return jsonify({})


heartbeat_list = [77, 78, 77, 78, 72, 69, 69, 68, 68, 67, 67, 66, 67, 69, 68, 68, 67, 69, 69, 69, 68, 66, 67, 68, 68, 68, 69, 70, 68, 67, 67, 67, 68, 68, 69, 69, 69, 69, 67, 67, 67, 67, 67, 67, 67, 67, 67, 68, 67, 68, 68, 69, 69, 69, 69, 71, 72, 72, 73, 73, 74, 74, 74, 74, 74, 74, 73, 73, 72, 71, 71, 70, 70, 69, 70, 70, 70, 70, 70, 70, 70, 71, 71, 72, 73, 76, 77, 80, 84, 86, 87, 86, 89, 93, 94, 95, 96, 98, 99, 90, 89, 80, 74, 70, 68, 65, 66, 68, 68, 68, 66, 66, 65, 64, 66, 67, 71, 70, 67, 67, 65, 65, 63, 63, 65, 66, 67, 68, 68, 69, 70, 71, 73, 73, 73, 72, 71, 71, 71, 70, 69, 70, 70, 72, 74, 74, 73, 72, 73, 75, 74, 75, 80, 75, 76, 75, 75, 75, 80, 79, 78, 78, 78, 77, 76, 77, 76, 77, 78, 79, 80, 80, 81, 82, 82, 83, 82, 81]


@bp.route('/heartbeat/')
def heartrate():
    global heartbeat_list
    result = heartbeat_list[0:11]
    heartbeat_list = heartbeat_list[12:]
    return jsonify({"heartbeat": result})

