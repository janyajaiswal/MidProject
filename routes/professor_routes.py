from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename
from utils.jwt_auth import role_required
from bson import ObjectId
import datetime

professor_bp = Blueprint("professor", __name__)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@professor_bp.route("/materials/upload", methods=["POST"])
@role_required("professor")
def upload_material():
    user = get_jwt_identity()
    file = request.files.get("file")

    if not file or not file.filename.lower().endswith((".pdf", ".doc", ".docx", ".ppt", ".pptx")):
        return jsonify({"error": "Invalid file type"}), 400

    file.seek(0, 2)
    size = file.tell()
    file.seek(0)

    if size > MAX_FILE_SIZE:
        return jsonify({"error": "File size exceeds 5MB limit"}), 400

    filename = secure_filename(file.filename)
    file_id = current_app.fs.put(file, filename=filename, content_type=file.content_type)

    current_app.db.files.insert_one({
        "filename": filename,
        "uploader": user["username"],
        "role": "professor",
        "type": "material",
        "gridfs_id": file_id,
        "uploaded_at": datetime.datetime.utcnow()
    })

    return jsonify({"msg": "✅ Material uploaded successfully", "file_id": str(file_id)}), 201

@professor_bp.route("/materials/delete/<file_id>", methods=["DELETE"])
@role_required("professor")
def delete_material(file_id):
    user = get_jwt_identity()
    try:
        file = current_app.db.files.find_one({"_id": ObjectId(file_id), "uploader": user["username"]})
        if not file:
            return jsonify({"error": "File not found or access denied"}), 404

        current_app.fs.delete(file["gridfs_id"])
        current_app.db.files.delete_one({"_id": ObjectId(file_id)})

        return jsonify({"msg": "🗑️ Material deleted successfully"}), 200
    except Exception:
        return jsonify({"error": "Invalid file ID"}), 400
