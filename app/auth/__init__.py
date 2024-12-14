from app.blueprints.users import users_bp
from flask import request, jsonify, Flask


# Oauth verification

@users_bp.route("/auth-endpoint", method =['GET'])
def auth():
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({"error": "Missing token"}), 401
    
    token = auth_header.split(" ")[1]

    if token == "expected_token_value":
        return jsonify({"message": "Token is valid" })
    else:
        return jsonify ({ "error": "invaild token"}), 403
    

