from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.extensions import db
from app.routes.project import bp as project_bp
import os
from dotenv import load_dotenv

# Add to existing imports
from app.routes.canvas import bp as canvas_bp
from app.routes.configuration import bp as configuration_bp
from app.routes.damage_scenario import bp as damage_scenario_bp  # Make sure this import works


# Load environment variables immediately
load_dotenv(override=True)

def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    cors = CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS","PATCH"],
            "allow_headers": ["Content-Type", "Authorization","X-Requested-With"],
            "expose_headers": ["Content-Range", "X-Content-Range"],
            "supports_credentials": True,
            "max_age": 120  # Cache preflight requests for 2 minutes
        }
    })
    
    # Configure database
    print(os.getenv('DATABASE_URL'))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') #'postgresql://username:password@localhost:5432/vtara_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    
    # Register blueprints
    app.register_blueprint(project_bp, url_prefix='/api')
    # Add to blueprint registration
    app.register_blueprint(canvas_bp, url_prefix='/api')

    # Add to blueprint registration
    app.register_blueprint(configuration_bp, url_prefix='/api')
    app.register_blueprint(damage_scenario_bp, url_prefix='/api')  # Add this line


    
    @app.route('/')
    def home():
        return jsonify({'message': 'API is running'})
    
    return app