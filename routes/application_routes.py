from flask import Blueprint, request, g
from services.application_service import create_application_for_user, get_applications_for_user, get_applications_by_id, update_application_for_user, delete_application_for_user_service, get_application_stats_for_user_service
from utils.responses import success_response
from utils.auth import require_access_token

applications_bp = Blueprint("applications", __name__)

@applications_bp.route("/applications", methods=["POST"])
@require_access_token
def create_application_route():
    data = request.get_json() or {}

    result = create_application_for_user(
        g.user_id,
        data.get("company_id"),
        data.get("job_title"),
        data.get("notes"),
        data.get("status"),
        data.get("applied_at")
    )

    return success_response(result, message="Application created successfully", status=201)

@applications_bp.route("/applications", methods=["GET"])
@require_access_token
def get_applications_route():
    status = request.args.get("status", default=None, type=str)
    company_id = request.args.get("company_id", default=None, type=int)

    result = get_applications_for_user(g.user_id, status, company_id)

    return success_response(result, message="Applications retrieved successfully")

@applications_bp.route("/applications/<int:application_id>", methods=["GET"])
@require_access_token
def get_application_by_id_route(application_id):
    result = get_applications_by_id(g.user_id, application_id)

    return success_response(result, message="Application retrieved successfully")

@applications_bp.route("/applications/<int:application_id>", methods=["PATCH"])
@require_access_token
def update_application_route(application_id):
    data = request.get_json() or {}

    result = update_application_for_user(
        g.user_id,
        application_id,
        data.get("company_id"),
        data.get("job_title"),
        data.get("notes"),
        data.get("status"),
        data.get("applied_at")
    )

    return success_response(result, message="Application updated successfully")

@applications_bp.route("/applications/<int:application_id>", methods=["DELETE"])
@require_access_token
def delete_application_for_user_route(application_id):
    result = delete_application_for_user_service(g.user_id, application_id)

    return success_response(result, message="Application deleted successfully", status=200)

@applications_bp.route("/applications/stats", methods=["GET"])
@require_access_token
def get_application_stats_for_user_route():
    result = get_application_stats_for_user_service(g.user_id)

    return success_response(result, message="Application stats retrieved successfully")