from dotenv import load_dotenv
import os
import certifi  

from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from utils.error_handlers import register_error_handlers
import gridfs

# ✅ Load environment variables
load_dotenv()

# ✅ Now access variables
mongo = PyMongo()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    MONGO_URI = os.getenv("MONGO_URI")  # ✅ INSIDE create_app
    SECRET_KEY = os.getenv("SECRET_KEY")

    # ✅ Append certifi CA bundle to ensure SSL handshake
    app.config["MONGO_URI"] = MONGO_URI + "&tlsCAFile=" + certifi.where()
    app.config["JWT_SECRET_KEY"] = SECRET_KEY

    mongo.init_app(app)
    jwt.init_app(app)

    if mongo.cx is None:
        raise RuntimeError("❌ Mongo client not initialized.")

    print("✅ Connected to DB:", mongo.cx.list_database_names())

    app.db = mongo.cx["midproject"]
    app.fs = gridfs.GridFS(app.db)

    # ✅ Blueprints
    from routes.auth_routes import auth_bp
    from routes.student_routes import student_bp
    from routes.professor_routes import professor_bp
    from routes.public_routes import public_bp

    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(student_bp, url_prefix="/")
    app.register_blueprint(professor_bp, url_prefix="/")
    app.register_blueprint(public_bp, url_prefix="/")

    print("🔁 Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} → {rule.endpoint}")

    register_error_handlers(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
