from flask import Blueprint, redirect, session, jsonify, request, url_for
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


# /login 접속하면 토근 반환
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
    print(token_info['access_token'])

    # 토큰을 세션에 저장 (보안상의 이유로 실제 애플리케이션에서는 안전한 방법으로 저장해야 함)
    session['spotify_token'] = token_info['access_token']

    # return 'Successfully logged in! You can now make API requests.'
    return redirect(url_for("auth.give_token"))


@bp.route('/token/')
def give_token():
    access_token = session.get('spotify_token')
    return jsonify({"access_token": access_token})

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
