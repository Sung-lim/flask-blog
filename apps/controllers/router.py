# -*- coding: utf-8 -*-
from flask import Flask
from flask import redirect
from flask import request

from apps.common.database import db_session
from apps.common.register import BlueprintRegister
from apps.common.response import error

from config import Config

app = Flask(__name__, template_folder=Config.TEMPLATES_DIR, static_folder=Config.STATIC_DIR)
app.config.from_object(Config.from_app_mode())
BlueprintRegister(app, 'apps.controllers', 'controllers').register()


@app.errorhandler(403)
def forbidden(err):
    return error(40300)


@app.errorhandler(404)
def page_not_found(err):
    return error(40400)


@app.errorhandler(410)
def gone(err):
    return error(41000)


@app.errorhandler(500)
def internal_server_error(err):
    return error(50000)


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.before_request
def before_request():
    if request.url.startswith('http://'):
        request.headers['HTTP_X_FORWARDED_PROTO'] = 'https'
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
