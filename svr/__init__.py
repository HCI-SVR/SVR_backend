from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine
import os
import pymysql

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app(test_config = None):
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')
    app.config['JSON_AS_ASCII'] = False

    pymysql.install_as_MySQLdb()

    db.init_app(app)
    migrate.init_app(app, db)

    if test_config is None:
        app.config.from_pyfile("../config.py")
    else:
        app.config.update(test_config)

    from .views import main_views, heartrate_views, music_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(heartrate_views.bp)
    app.register_blueprint(music_views.bp)


    return app