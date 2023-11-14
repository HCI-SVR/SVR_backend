from flask import Flask, Blueprint

bp = Blueprint('main', __name__, url_prefix="/")

@bp.route('/svr')
def hello_pybo():
    return 'SVR! 화이팅!'

@bp.route('/')
def index():
    return 'index'
