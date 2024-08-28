#!/usr/bin/env python3
"""
Force locale with URL parameter
"""
from flask import Flask, g, render_template, request
from flask_babel import Babel
from typing import Union
import pytz


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    """
    Config class for Babel
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)
babel = Babel(app)


def get_user(login_as: int) -> Union[dict, None]:
    """
    Returns: user dict or None if ID cannot be found
    or if login_as was not passed.
    """
    if login_as and int(login_as) in users:
        return users[int(login_as)]
    return None


@app.before_request
def before_request():
    """
    Add user to flask.g if user is found
    """
    g.user = get_user(request.args.get('login_as'))


# @babel.localeselector
def get_locale() -> str:
    """
    Get locale from request
    """
    locale = request.args.get("locale")
    if locale and locale in app.config['LANGUAGES']:
        return locale

    if g.user:
        locale = g.user.get("locale")
        if locale and locale in app.config['LANGUAGES']:
            return locale

    h_locale = request.headers.get('locale')
    if h_locale and h_locale in app.config['LANGUAGES']:
        return h_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])
# babel.init_app(app, locale_selector=get_locale)
# @babel.localeselector has issues on this verion


@babel.timezoneselector
def get_timezone() -> str:
    """
    Get timezone from request and return
    """
    timezone = request.args.get('timezone')
    if not timezone and g.user and g.user['timezone']:
        timezone = g.user['timezone']
    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


# babel.init_app(app, locale_selector=get_locale, timezone_selector=get_timezone)
# decorator doesnt work for this version


@app.route("/", strict_slashes=False)
def index() -> str:
    """
    Returns 5-index.html
    """
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run()
