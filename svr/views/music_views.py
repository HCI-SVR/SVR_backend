import requests
from flask import jsonify, Blueprint, request, redirect, session
from svr import db
from svr.models import Music
from svr import create_app
from svr import config
import json

bp = Blueprint('music', __name__, url_prefix="/music")
# from svr.views.spotify import token


SPOTIFY_AUTH_URL = config.SPOTIFY_AUTH_URL
SPOTIFY_CLIENT_ID = config.SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = config.SPOTIFY_CLIENT_SECRET
SPOTIFY_REDIRECT_URI = config.SPOTIFY_REDIRECT_URI
SPOTIFY_API_BASE_URL = config.SPOTIFY_API_BASE_URL
SPOTIFY_TOKEN_URL = config.SPOTIFY_TOKEN_URL
SPOTIFY_SCOPE = config.SPOTIFY_SCOPE


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
    return uri

    # access_token = session.get('spotify_token')
    #
    # # Spotify API에 전송할 데이터 구성
    # endpoint = 'https://api.spotify.com/v1/me/player/play'
    # headers = {
    #     'Authorization': f'Bearer {access_token}',
    #     'Content-Type': 'application/json',
    # }
    # data = {
    #     'uris': [uri]  # 재생할 트랙의 Spotify URI
    # }
    #
    # # Spotify API에 PUT 요청 보내기
    # response = requests.put(f'{SPOTIFY_API_BASE_URL}{endpoint}', headers=headers, data=json.dumps(data))
    #
    # # API 응답 확인
    # if response.status_code == 204:
    #     return 'Playback started successfully!'
    # else:
    #     return f'Error: {response.status_code} - {response.text}'


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

# 로그인 라우트
# @bp.route('/login')
# def login():
#     # Spotify 로그인을 위한 URL 생성
#     auth_url = f'{SPOTIFY_AUTH_URL}?client_id={SPOTIFY_CLIENT_ID}&redirect_uri={SPOTIFY_REDIRECT_URI}' \
#                f'&scope={SPOTIFY_SCOPE}&response_type=code'
#     print(auth_url)
#     return redirect(auth_url)
#
#
# # 로그인 후 리디렉션 라우트
# @bp.route('/callback')
# def callback():
#     # Spotify에서 전달한 코드 가져오기
#     auth_code = request.args.get('code')
#
#     # Spotify API에 토큰 요청
#     token_data = {
#         'code': auth_code,
#         'redirect_uri': SPOTIFY_REDIRECT_URI,
#         'grant_type': 'authorization_code',
#         'client_id': SPOTIFY_CLIENT_ID,
#         'client_secret': SPOTIFY_CLIENT_SECRET
#     }
#
#     # 토큰 엔드포인트에 POST 요청 보내기
#     response = requests.post(SPOTIFY_TOKEN_URL, data=token_data)
#     token_info = response.json()
#
#     # 토큰을 세션에 저장 (보안상의 이유로 실제 애플리케이션에서는 안전한 방법으로 저장해야 함)
#     session['spotify_token'] = token_info['access_token']
#
#     return 'Successfully logged in! You can now make API requests.'


# 노래 재생 시작 라우트
# @bp.route('/play')
# def start_playback():
#     # 사용자의 Spotify 액세스 토큰 가져오기
#     access_token = session.get('spotify_token')
#
#     # Spotify API에 전송할 데이터 구성
#     endpoint = 'https://api.spotify.com/v1/me/player/play'
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json',
#     }
#     data = {
#         'uris': ['spotify:track:6rqhFgbbKwnb9MLmUQDhG6']  # 재생할 트랙의 Spotify URI
#     }
#
#     # Spotify API에 PUT 요청 보내기
#     response = requests.put(f'{SPOTIFY_API_BASE_URL}{endpoint}', headers=headers, data=json.dumps(data))
#
#     # API 응답 확인
#     if response.status_code == 204:
#         return 'Playback started successfully!'
#     else:
#         return f'Error: {response.status_code} - {response.text}'