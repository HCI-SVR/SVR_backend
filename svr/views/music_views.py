from flask import jsonify, Blueprint, request, redirect, session, url_for, render_template
from svr import db
from svr.models import Music
import requests
import json
from svr import config


bp = Blueprint('music', __name__, url_prefix="/music")
SPOTIFY_API_BASE_URL = config.SPOTIFY_API_BASE_URL

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


# 노래 재생 시작 라우트
@bp.route('/<int:music_id>/')
def play(music_id):
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


    # spotify_url = "https://api.spotify.com/v1/me/player/play"
    # request_body = {
    #     "offset": {"uri": uri}
    # }
    #
    # headers = {
    #     "Authorization": token,
    #     "Content-Type": "application/json"
    # }
    #
    # response = requests.put(spotify_url, json=request_body, headers=headers)
    # print(response.status_code)
    # print(response.text)
    #
    # if response.status_code == 200:
    #
    #     return jsonify({'message': "Music played successfully"})
    # else:
    #     return jsonify({'error': 'Failed to play music'})
@bp.route('/')
def music_player():
    return render_template('music_player.html')
@bp.route('/ready')
def play_ready():

    access_token = session.get('spotify_token')
    print(access_token)
    endpoint = '/me/player/devices'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    response = requests.get(f'{SPOTIFY_API_BASE_URL}{endpoint}', headers=headers)

    # return jsonify({
    #     # "response": response.text,
    #     "response1": response.raw
    # })
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return f'Error: {response.status_code} - {response.text}'




# 노래 재생 api
@bp.route('/play')
def start_playback():
    # 사용자의 Spotify 액세스 토큰 가져오기
    access_token = session.get('spotify_token')

    # Spotify API에 전송할 데이터 구성
    endpoint = '/me/player/play'
    endpoint2 = '/me/player/devices'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    response_device = requests.get(f'{SPOTIFY_API_BASE_URL}{endpoint2}', headers=headers)
    devices = response_device.json().get('devices', [])
    # device_id = response_device.json()['devices'][0]["id"]
    device_id = devices[0].get('id')
    session['device_id'] = device_id
    print(f"device_id = {device_id}")

    data = {
        "uris": ["spotify:track:3Ua0m0YmEjrMi9XErKcNiR"],
    }


    # Spotify API에 PUT 요청 보내기
    response = requests.put(f'{SPOTIFY_API_BASE_URL}{endpoint}?device_id={device_id}', headers=headers, data=json.dumps(data))
    print(response.text)

    # API 응답 확인
    if response.status_code == 200 | response.status_code == 204:
        # return jsonify({
        #     "url": response.url,
        #     "message": f'Error: {response.status_code} - {response.text}'
        # })
        return redirect(url_for('music.get_state'))
    else:
        return f'Error: {response.status_code} - {response.text}'

@bp.route('/state')
def get_state():
    endpoint = '/me/player'
    access_token = session.get('spotify_token')

    # Spotify API에 전송할 데이터 구성
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    device_id = session.get('device_id')
    response = requests.get(f'{SPOTIFY_API_BASE_URL}{endpoint}', headers=headers)
    print(response.text)
    return jsonify(response.json())

