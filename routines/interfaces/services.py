from flask import Blueprint, request, jsonify

from routines.application.services import RoutineRecordApplicationService
from iam.interfaces.services import authenticate_request

routine_api = Blueprint("routine_api", __name__)
routine_record_service = RoutineRecordApplicationService()


@routine_api.route("/api/v1/routine-monitoring/data-records", methods=["POST"])
def create_routine_record():

    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    data = request.json
    print("Datos recibidos en el POST /api/v1/routine-monitoring/data-records:", data)
    try:
        device_id = data["device_id"]
        routine_data = data["routine_data"]
        created_at = data.get("created_at")
        record = routine_record_service.create_routine_record(
            device_id, routine_data, created_at, request.headers.get("X-API-Key")
        )
        return jsonify({
            "id": record.id,
            "device_id": record.device_id,
            "routine_data": record.routine_data,
            "created_at": record.created_at.isoformat() + "Z"
        }), 201
    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

import datetime

@routine_api.route("/api/v1/routine-monitoring/data-records", methods=["GET"])
def get_routine_records():
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    records = routine_record_service.get_all_routine_records()
    result = []
    for r in records:
        created_at = r.created_at
        if isinstance(created_at, datetime.datetime):
            created_at_str = created_at.isoformat() + "Z"
        else:
            created_at_str = str(created_at)
            if not created_at_str.endswith("Z"):
                created_at_str += "Z"
        result.append({
            "id": r.id,
            "device_id": r.device_id,
            "routine_data": r.routine_data,
            "created_at": created_at_str
        })
    return jsonify(result), 200


@routine_api.route("/api/v1/routine-monitoring/data-records/<record_id>", methods=["GET"])
def get_routine_record_by_id(record_id):
    auth_result = authenticate_request()
    if auth_result:
        return auth_result
    record = routine_record_service.get_routine_record_by_id(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    created_at = record.created_at
    import datetime
    if isinstance(created_at, datetime.datetime):
        created_at_str = created_at.isoformat() + "Z"
    else:
        created_at_str = str(created_at)
        if not created_at_str.endswith("Z"):
            created_at_str += "Z"
    return jsonify({
        "id": record.id,
        "device_id": record.device_id,
        "routine_data": record.routine_data,
        "created_at": created_at_str
    }), 200

@routine_api.route("/api/v1/routine-monitoring/data-records/iot-device/<iot_device_id>", methods=["GET"])
def get_routine_record_by_iot_device_id(iot_device_id):
    auth_result = authenticate_request()
    if auth_result:
        return auth_result
    records = routine_record_service.get_routines_by_device(iot_device_id)
    if not records:
        return jsonify({"error": "No records found for this device"}), 404
    result = []
    for r in records:
        created_at = r.created_at
        if isinstance(created_at, datetime.datetime):
            created_at_str = created_at.isoformat() + "Z"
        else:
            created_at_str = str(created_at)
            if not created_at_str.endswith("Z"):
                created_at_str += "Z"
        result.append({
            "id": r.id,
            "device_id": r.device_id,
            "routine_data": r.routine_data,
            "created_at": created_at_str
        })
    return jsonify(result), 200