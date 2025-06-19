from flask import Blueprint, request, jsonify
import datetime
from healthDehumidifier.application.services import DehumidifierRecordApplicationService
from iam.interfaces.services import authenticate_request

health_api = Blueprint("health_api", __name__)

health_record_service = DehumidifierRecordApplicationService()

@health_api.route("/api/v1/health-monitoring/data-records", methods=["POST"])
def create_health_record():

    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    data = request.json
    try:
        device_id = data["device_id"]
        humidifier_info = data["humidifier_info"]
        created_at = data.get("created_at")
        record = health_record_service.create_health_record(
            device_id, humidifier_info, created_at, request.headers.get("X-API-Key")
        )
        return jsonify({
            "id": record.id,
            "device_id": record.device_id,
            "humidifier_info": record.humidifier_info,
            "created_at": record.created_at.isoformat() + "Z"
        }), 201
    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@health_api.route("/api/v1/health-monitoring/data-records", methods=["GET"])
def get_health_records():
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    records = health_record_service.get_all_records()
    result = [
        {
            "id": r.id,
            "device_id": r.device_id,
            "humidifier_info": r.humidifier_info,
            "created_at": r.created_at.isoformat() + "Z" if isinstance(r.created_at, datetime.datetime) else str(
                r.created_at)
        }
        for r in records
    ]
    return jsonify(result), 200