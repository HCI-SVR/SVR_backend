# 임의 api 구현 파일
from flask import Blueprint, jsonify, request
from svr.hci.calories import get_calories
from svr.hci.heartbeat import get_heartbeat
from svr.hci.distance import get_distance

bp = Blueprint('hci', __name__, url_prefix="/hci")


heartbeat_global = []
calories_global = []
distance_global = []

heartbeat_list = []
calories_list = []
distance_list = []


@bp.route('/', methods=['POST'])
def get_info():
    global heartbeat_global
    global calories_global
    global distance_global

    params = request.get_json()
    group_id = params['group_id']
    age = params['age']
    weight = params['weight']

    heartbeat_global = get_heartbeat(group_id, age)
    calories_global = get_calories(group_id, weight)
    distance_global = get_distance(group_id)

    return jsonify({"response_code": 200})


# 심박수 api
@bp.route('/heartbeat')
def heartbeat():

    global heartbeat_global
    global heartbeat_list

    if len(heartbeat_list) < 12:
        last = 12 - len(heartbeat_list)
        heartbeat_return = heartbeat_list + heartbeat_global[:last]
        heartbeat_list = heartbeat_global[last:]
        return jsonify({"heartbeat": heartbeat_return})
    else:
        heartbeat_return = heartbeat_list[0:12]
        heartbeat_list = heartbeat_list[12:]
        return jsonify({"heartbeat": heartbeat_return})


# 칼로리, 거리 조회 api
@bp.route('/exercise')
def exercise():

    global calories_global
    global calories_list

    global distance_global
    global distance_list

    if len(calories_list) < 12:
        last = 12 - len(calories_list)
        calories_return = calories_list + calories_global[:last]
        distance_return = distance_list + distance_global[:last]
        calories_list = calories_global[last:]
        distance_list = distance_global[last:]
        return jsonify({
            "calories": calories_return,
            "distances": distance_return
        })
    else:
        calories_return = calories_list[0:12]
        distance_return = distance_list[0:12]
        calories_list = calories_list[12:]
        distance_list = distance_list[12:]
        return jsonify({
            "calories": calories_return,
            "distances": distance_return
        })


@bp.route('/reset')
def reset():
    global distance_global
    global calories_global
    global distance_list
    global calories_list

    distance_list = distance_global
    calories_list = calories_global
    return jsonify({"response_code": 200})