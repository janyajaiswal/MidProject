from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from functools import wraps
from flask import jsonify

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                identity = get_jwt_identity()

                if not identity or "role" not in identity:
                    return jsonify({"error": "Missing role in token"}), 400

                if identity["role"] != required_role:
                    return jsonify({"error": f"{required_role.capitalize()} access required"}), 403

                return fn(*args, **kwargs)

            except Exception as e:
                return jsonify({"error": str(e)}), 401

        return decorator
    return wrapper
