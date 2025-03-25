from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename
from utils.jwt_auth import role_required
from app import mongo
import datetime

student_bp = Blueprint("student", __name__)

@student_bp.route("/notes/upload", methods=["POST"])
@role_required("student")
def upload_note():
    user = get_jwt_identity()
    file = request.files.get("file")

    if not file or not file.filename.lower().endswith((".jpg", ".jpeg", ".png", ".pdf")):
        return jsonify({"error": "Invalid file type"}), 400

    filename = secure_filename(file.filename)
    file_id = current_app.fs.put(file, filename=filename, content_type=file.content_type)

    mongo.db.files.insert_one({
        "filename": filename,
        "uploader": user["username"],
        "role": "student",
        "type": "note",
        "gridfs_id": file_id,
        "uploaded_at": datetime.datetime.utcnow()
    })

    return jsonify({"msg": "Note uploaded", "file_id": str(file_id)}), 201
