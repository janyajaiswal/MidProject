from flask import Blueprint, jsonify, Response, current_app
from bson import ObjectId

public_bp = Blueprint("public", __name__)

@public_bp.route("/public-files", methods=["GET"])
def get_public_files():
    cursor = current_app.db.files.find({})

    files = []
    for file in cursor:
        file["_id"] = str(file["_id"])  # convert MongoDB _id
        if "gridfs_id" in file:
            file["gridfs_id"] = str(file["gridfs_id"])
        files.append(file)

    return jsonify(files), 200


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
