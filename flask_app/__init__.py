"""
Q-Sentinel Flask Application Package.
SIH26141 • Egreen Quanta
"""

from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    
    from flask_app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
