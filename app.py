import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api
from sqlalchemy.orm import DeclarativeBase
from flask_swagger_ui import get_swaggerui_blueprint

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
api = Api(app)

# Configure app
app.secret_key = os.environ.get("SESSION_SECRET")
# Use PostgreSQL database URL from environment variables
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Setup rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Initialize extensions
db.init_app(app)

# Swagger UI configuration
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Social Quests API",
        'dom_id': '#swagger-ui',
        'deepLinking': True,
        'showExtensions': True,
        'showCommonExtensions': True
    }
)

# Register blueprint at URL
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Import routes after app initialization to avoid circular imports
from routes import *

with app.app_context():
    db.create_all()