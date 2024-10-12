# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_static_digest import FlaskStaticDigest

bcrypt = Bcrypt()
cache = Cache()
csrf_protect = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
debug_toolbar = DebugToolbarExtension()
flask_static_digest = FlaskStaticDigest()
