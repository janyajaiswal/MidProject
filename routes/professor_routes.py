from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename
from utils.jwt_auth import role_required
from app import mongo
import datetime

professor_bp = Blueprint("professor", __name__)

@professor_bp.route("/materials/upload", methods=["POST"])
@role_required("professor")
def upload_material():
    user = get_jwt_identity()
    file = request.files.get("file")

    if not file or not file.filename.lower().endswith((".pdf", ".doc", ".docx", ".ppt", ".pptx")):
        return jsonify({"error": "Invalid file type"}), 400

    filename = secure_filename(file.filename)
    file_id = current_app.fs.put(file, filename=filename, content_type=file.content_type)

    mongo.db.files.insert_one({
        "filename": filename,
        "uploader": user["username"],
        "role": "professor",
        "type": "material",
        "gridfs_id": file_id,
        "uploaded_at": datetime.datetime.utcnow()
    })

    return jsonify({"msg": "Material uploaded", "file_id": str(file_id)}), 201
