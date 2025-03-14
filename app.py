import os
from flask import Flask, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api
from sqlalchemy.orm import DeclarativeBase
from flask_swagger_ui import get_swaggerui_blueprint
import logging

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
    "pool_size": 5,  # Maximum number of database connections
    "pool_timeout": 30,  # Timeout for getting a connection from the pool
    "pool_recycle": 300,  # Recycle connections after 5 minutes
    "pool_pre_ping": True,  # Verify connection before use
    "max_overflow": 10  # Maximum number of connections that can be created beyond pool_size
}

# Setup rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Initialize extensions
db.init_app(app)

# Root route for testing
@app.route('/')
def index():
    return jsonify({"status": "healthy", "message": "API is running"})

# Serve swagger.json directly
@app.route('/static/swagger.json')
def serve_swagger():
    return send_from_directory('static', 'swagger.json')

# Swagger UI configuration
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI
API_URL = '/static/swagger.json'  # Our API url

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
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
    try:
        # Create tables without dropping existing data
        db.create_all()
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")