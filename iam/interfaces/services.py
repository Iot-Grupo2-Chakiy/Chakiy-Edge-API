from flask import Blueprint, request, jsonify
from iam.application.services import AuthApplicationService

iam_api = Blueprint("iam_api", __name__)

# Initialize dependencies
auth_service = AuthApplicationService()

def authenticate_request():
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return jsonify({"error": "Missing X-API-Key"}), 401
    if not auth_service.authenticate_api_key(api_key):
        return jsonify({"error": "Invalid API key"}), 401
    return None