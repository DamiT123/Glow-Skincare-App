# Author: Oluwadamilola Tinubu - C24344666
# __init__.py - Application factory and Flask-Babel configuration

from flask import Flask
from flask_babel import Babel, get_locale

def get_locale_selector():
    from flask import session, request
    # Check if user has selected a language in session
    return session.get('lang', request.accept_languages.best_match(['en', 'ja', 'es']))

def create_app():
    app = Flask(__name__)
    app.secret_key = 'skincare-secret-key'
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'ja', 'es']
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = '../translations'

    babel = Babel(app, locale_selector=get_locale_selector)

    from app import routes
    app.register_blueprint(routes.bp)

    return app