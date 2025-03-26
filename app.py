from dotenv import load_dotenv
import os

from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from config import MONGO_URI, SECRET_KEY
from utils.error_handlers import register_error_handlers
import gridfs


MONGO_URI = os.getenv("MONGO_URI")
SECRET_KEY = os.getenv("SECRET_KEY")

load_dotenv()
mongo = PyMongo()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")

    mongo.init_app(app)
    jwt.init_app(app)

    if mongo.cx is None:
        raise RuntimeError("❌ Mongo client not initialized.")

    print("✅ Connected to DB:", mongo.cx.list_database_names())  # Safe here

    app.db = mongo.cx["midproject"]
    app.fs = gridfs.GridFS(app.db)

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.student_routes import student_bp
    from routes.professor_routes import professor_bp
    from routes.public_routes import public_bp

    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(student_bp, url_prefix="/")
    app.register_blueprint(professor_bp, url_prefix="/")
    app.register_blueprint(public_bp, url_prefix="/")

    print("🔁 Registered routes:")
    print(app.url_map)

    register_error_handlers(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
