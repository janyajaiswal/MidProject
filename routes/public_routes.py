from flask import Blueprint, jsonify, Response, current_app
from bson import ObjectId
from app import mongo

public_bp = Blueprint("public", __name__)

@public_bp.route("/public-files", methods=["GET"])
def get_public_files():
    files = mongo.db.files.find({}, {"_id": 0, "filename": 1, "type": 1, "role": 1})
    return jsonify(list(files)), 200

@public_bp.route("/download/<file_id>", methods=["GET"])
def download_file(file_id):
    try:
        file_id = ObjectId(file_id)
        file_doc = current_app.fs.get(file_id)
        return Response(
            file_doc.read(),
            mimetype=file_doc.content_type,
            headers={"Content-Disposition": f"attachment;filename={file_doc.filename}"}
        )
    except Exception:
        return jsonify({"error": "File not found"}), 404
