# app.py

from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.request_log import Base
from controllers.math_controller import math_bp
import os

print("App is writing to:", os.path.abspath("requests.db"))

def create_app():
    app = Flask(__name__)

    # --- DATABASE SETUP ---
    engine = create_engine('sqlite:///requests.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    app.session_factory = Session  # ✅ this replaces the old line
    # -----------------------

    # Register blueprint from math_controller
    app.register_blueprint(math_bp)

    @app.route('/')
    def home():
        return jsonify({
            "message": "Welcome to the Math Microservice API!"
        })

    return app

# Only run if this file is the main program
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
