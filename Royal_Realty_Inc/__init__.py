from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .blueprints.site.routes import site
from .blueprints.auth.routes import auth
from .blueprints.api.routes import api
from config import Config
from .models import login_manager, db
from .helpers import JSONEncoder

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)
app.json_encoder = JSONEncoder

jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)
cors = CORS(app)

login_manager.init_app(app)
login_manager.login_view = 'auth.signin'
login_manager.login_message = "Hey you! Log in please!"
login_manager.login_message_category = 'warning'