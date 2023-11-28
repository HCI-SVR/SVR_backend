from flask import Blueprint, jsonify, request
from svr.models import Music

bp = Blueprint('rate', __name__, url_prefix="/rate")

count = {}
# 노래 재생 횟수 딕셔너리(key: music_id, value: count)


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
