from flask import Blueprint
from services.auth_service import register_user, login_user, refresh_access_token_service
from flask import request, g
from utils.responses import success_response
from utils.auth import require_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    result = register_user(
        data.get("username"),
        data.get("password")
    )

    return success_response(result, message="User created successfully", status=201)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    result = login_user(
        data.get("username"),
        data.get("password")
    )

    return success_response(result, message="Login successful")

@auth_bp.route("/refresh", methods=["POST"])
def refresh_route():
    data = request.get_json() or {}

    result = refresh_access_token_service(
        data.get("refresh_token")
    )

    return success_response(result, message="Tokens refreshed successfully")

@auth_bp.route("/me", methods=["GET"])
@require_access_token
def me():
    return success_response(
        {"user_id": g.user_id},
        message="Access token valid"
    )
