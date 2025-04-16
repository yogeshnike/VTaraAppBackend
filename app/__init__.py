from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.extensions import db
from app.routes.project import bp as project_bp
import os
from dotenv import load_dotenv

# Load environment variables immediately
load_dotenv(override=True)

def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    cors = CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Range", "X-Content-Range"],
            "supports_credentials": True
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
    
    @app.route('/')
    def home():
        return jsonify({'message': 'API is running'})
    
    return app