from app import app
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from instagram_api.blueprints.users.views import users_api_blueprint
app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')

from instagram_api.blueprints.login.views import login_api_blueprint
app.register_blueprint(login_api_blueprint, url_prefix='/api/v1/auth')

from instagram_api.blueprints.items.view import item_api_blueprint
app.register_blueprint(item_api_blueprint, url_prefix='/api/v1/item')

