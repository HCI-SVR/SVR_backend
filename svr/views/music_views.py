from flask import jsonify, Blueprint, request, redirect, session, url_for, render_template
from svr import db
from svr.models import Music
import requests
import json
# from svr import config_local as config  # 로컬 config
from svr import config    # ec2 config


bp = Blueprint('music', __name__, url_prefix="/music")
SPOTIFY_API_BASE_URL = config.SPOTIFY_API_BASE_URL


# 모든 노래 반환
@bp.route('/all')
def findall():
    music_list = Music.query.all()
    return jsonify([music.serialize() for music in music_list])


# 노래 삽입 api (데이터 삽입하고 프로젝트 사용할거라 사용x)
@bp.route('/insert', methods=['POST'])
def insert():
    params = request.get_json()
    name = params['name']
    group_id = params['group_id']
    uri = params['uri']
    image_key = params['image_key']
    singer = params['singer']

    music = Music(name=name, group_id=group_id,
                  uri=uri, image_key=image_key, singer=singer)
    db.session.add(music)
    db.session.commit()

    return jsonify(music.serialize())


# 노래 재생 시작(데이터 구축 후에 사용)
# @bp.route('/<int:music_id>')
def play2(music_id):
    music = Music.query.get(music_id)
    uri = music.uri
    # return uri

    access_token = session.get('spotify_token')

    # Spotify API에 전송할 데이터 구성
    endpoint = '/me/player/play'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    data = {
        'uris': [uri]  # 재생할 트랙의 Spotify URI
    }

    # Spotify API에 PUT 요청 보내기
    response = requests.put(f'{SPOTIFY_API_BASE_URL}{endpoint}', headers=headers, data=json.dumps(data))

    # API 응답 확인
    if response.status_code == 204:
        return 'Playback started successfully!'
    else:
        return f'Error: {response.status_code} - {response.text}'


# 테스트용 (노래 재생 화면 출력)
@bp.route('/')
def music_player():
    return render_template('music_player.html')


# 노래 재생할 수 있는 장치 확인
@bp.route('/ready')
def play_ready():
    access_token = session.get('spotify_token')
    endpoint = '/me/player/devices'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    response = requests.get(f'{SPOTIFY_API_BASE_URL}{endpoint}', headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return f'Error: {response.status_code} - {response.text}'


# 노래 재생 api
# 로그인 후 받은 토큰 필요
@bp.route('/<int:music_id>')
def play(music_id):
    music = Music.query.get(music_id)
    uri = music.uri

    # 사용자의 Spotify 액세스 토큰 가져오기
    access_token = session.get('spotify_token')

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    # 노래 재생 가능한 device 반환 api 엔드포인트
    endpoint2 = '/me/player/devices'

    response_device = requests.get(f'{SPOTIFY_API_BASE_URL}{endpoint2}', headers=headers)
    devices = response_device.json().get('devices', [])

    # 노래 재생 가능한 디바이스들 중 첫번째 디바이스 사용
    device_id = devices[0].get('id')
    session['device_id'] = device_id
    print(f"device_id = {device_id}")   # 디바이스 확인

    # 노래 재생 api 엔드포인트
    endpoint = '/me/player/play'

    # 노래 재생 시 해당 노래 uri 필요함
    data = {
        "uris": [uri],
    }

    # Spotify API에 PUT 요청 보내기
    response = requests.put(f'{SPOTIFY_API_BASE_URL}{endpoint}?device_id={device_id}', headers=headers, data=json.dumps(data))
    print(response.text)

    # API 응답 확인
    if response.status_code == 200 | response.status_code == 204:

        # 노래 재생하고 재생 상태 확인 함수 호출
        return redirect(url_for('music.get_state'))
    else:
        return f'Error: {response.status_code} - {response.text}'


# spotify web playback 상태 확인
@bp.route('/state')
def get_state():

    access_token = session.get('spotify_token')
    endpoint = '/me/player'
    # Spotify API에 전송할 데이터 구성
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    response = requests.get(f'{SPOTIFY_API_BASE_URL}{endpoint}', headers=headers)
    print(response.text)

    # 현재 재생 상태, 재생 노래의 정보
    return jsonify(response.json())
    # return response.text
