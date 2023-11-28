from flask import jsonify, Blueprint, request, redirect, session, url_for
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
    endpoint = 'https://api.spotify.com/v1/me/player/play'
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

# 노래 재생 api
@bp.route('/play')
def start_playback():
    # 사용자의 Spotify 액세스 토큰 가져오기
    access_token = session.get('spotify_token')

    # Spotify API에 전송할 데이터 구성
    endpoint = '/me/player/play'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    data = {
        "offset": {"uri": "spotify:track:3Ua0m0YmEjrMi9XErKcNiR"},  # 재생할 트랙의 Spotify URI
        "position_ms": 0
    }

    # Spotify API에 PUT 요청 보내기
    response = requests.put(f'{SPOTIFY_API_BASE_URL}{endpoint}', headers=headers, data=json.dumps(data))


    # API 응답 확인
    if response.status_code == 204:
        return jsonify({"url": response.url})
    else:
        return f'Error: {response.status_code} - {response.text}'