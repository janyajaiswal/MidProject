from flask import Blueprint, jsonify, Response, current_app
from bson import ObjectId

public_bp = Blueprint("public", __name__)
print("✅ public_routes.py loaded")

@public_bp.route("/public-files", methods=["GET"])
def get_public_files():
    files_cursor = current_app.db.files.find({}, {
        "filename": 1,
        "type": 1,
        "role": 1,
        "gridfs_id": 1
    })

    files = []
    for f in files_cursor:
        if "gridfs_id" in f:
            f["gridfs_id"] = str(f["gridfs_id"])
        if "_id" in f:
            f["_id"] = str(f["_id"])
        files.append(f)

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
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return jsonify({"error": "File not found"}), 404
