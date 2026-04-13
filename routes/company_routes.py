from flask import Blueprint, request, g
from utils.auth import require_access_token
from services.company_service import create_company_for_user, get_companies_for_user
from utils.responses import success_response

company_bp = Blueprint("companies", __name__)

@company_bp.route("/companies", methods=["POST"])
@require_access_token
def create_company_route():
    data = request.get_json() or {}

    result = create_company_for_user(
        g.user_id,
        data.get("company_name")
    )

    return success_response(result, message="Company created successfully", status=201)

@company_bp.route("/companies", methods=["GET"])
@require_access_token
def get_companies():
    result = get_companies_for_user(g.user_id)

    return success_response(result, message="Companies retrieved successfully")