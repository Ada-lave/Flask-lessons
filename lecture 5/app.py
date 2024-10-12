from flask import Flask
from routes.routers import register_routes

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "fASbA_A12312_asdS"
    register_routes(app)
    
    return app
    
    
