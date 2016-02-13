#! /usr/bin/env python3

from functools import wraps
from flask import request

from odie import ClientError
from db.fsmi import Cookie


def unauthorized():
    raise ClientError("unauthorized", status=401)


def get_user():
    cookie = request.cookies.get('FSMISESSID')
    if not cookie:
        return None
    active_session = Cookie.query.filter_by(sid=cookie).first()
    if active_session:
        active_session.refresh()
        return active_session.user


def login_required(f):
    @wraps(f)
    def wrapped_f(*args, **kwargs):
        user = get_user()
        if user:
            result = f(*args, **kwargs)
            return result
        return unauthorized()
    return wrapped_f
