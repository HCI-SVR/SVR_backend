from flask import Blueprint, redirect, session, jsonify, request
from svr import config
import requests

bp = Blueprint('auth', __name__, url_prefix="/auth")

SPOTIFY_AUTH_URL = config.SPOTIFY_AUTH_URL
SPOTIFY_CLIENT_ID = config.SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = config.SPOTIFY_CLIENT_SECRET
SPOTIFY_REDIRECT_URI = config.SPOTIFY_REDIRECT_URI
SPOTIFY_API_BASE_URL = config.SPOTIFY_API_BASE_URL
SPOTIFY_TOKEN_URL = config.SPOTIFY_TOKEN_URL
SPOTIFY_SCOPE = config.SPOTIFY_SCOPE


@bp.route('/login')
def login():
    # Spotify 로그인을 위한 URL 생성
    auth_url = f'{SPOTIFY_AUTH_URL}?client_id={SPOTIFY_CLIENT_ID}&redirect_uri={SPOTIFY_REDIRECT_URI}' \
               f'&scope={SPOTIFY_SCOPE}&response_type=code'
    return redirect(auth_url)


# 로그인 후 리디렉션 라우트
@bp.route('/callback')
def callback():
    # Spotify에서 전달한 코드 가져오기
    auth_code = request.args.get('code')

    # Spotify API에 토큰 요청
    token_data = {
        'code': auth_code,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'grant_type': 'authorization_code',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET
    }

    # 토큰 엔드포인트에 POST 요청 보내기
    response = requests.post(SPOTIFY_TOKEN_URL, data=token_data)
    token_info = response.json()

    # 토큰을 세션에 저장 (보안상의 이유로 실제 애플리케이션에서는 안전한 방법으로 저장해야 함)
    session['spotify_token'] = token_info['access_token']

    return 'Successfully logged in! You can now make API requests.'

@bp.route('/token/')
def give_token():
    access_token = session.get('spotify_token')
    return jsonify({"access_token": access_token})


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