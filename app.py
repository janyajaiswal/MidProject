# app.py
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from config import MONGO_URI, SECRET_KEY
from utils.error_handlers import register_error_handlers
import gridfs

mongo = PyMongo()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = MONGO_URI
    app.config["JWT_SECRET_KEY"] = SECRET_KEY

    mongo.init_app(app)
    jwt.init_app(app)

    app.fs = gridfs.GridFS(mongo.cx.get_database())#acessing mongodb

    from routes.auth_routes import auth_bp
    from routes.student_routes import student_bp
    from routes.professor_routes import professor_bp
    from routes.public_routes import public_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(professor_bp)
    app.register_blueprint(public_bp)

    register_error_handlers(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
