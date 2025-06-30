from flask import Blueprint, request, jsonify
import datetime
import logging
import json
from healthDehumidifier.application.services import DehumidifierRecordApplicationService
from iam.interfaces.services import authenticate_request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

health_api = Blueprint("health_api", __name__)

health_record_service = DehumidifierRecordApplicationService()

@health_api.route("/api/v1/health-dehumidifier/data-records", methods=["POST"])
def create_health_record():
    auth_result = authenticate_request()
    if auth_result:
        logger.warning("Authentication failed")
        return auth_result

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = None
    try:
        data = request.json
    except Exception as e:
        data = None
    
    if data is None:
        try:
            raw_data = request.get_data(as_text=True)
            
            fixed_data = raw_data
            if '"humidifier_info":"{"' in raw_data:
                import re
                pattern = r'"humidifier_info":"(\{[^}]*\})"'
                match = re.search(pattern, raw_data)
                if match:
                    inner_json = match.group(1)
                    escaped_inner_json = inner_json.replace('"', '\\"')
                    fixed_data = raw_data.replace(match.group(0), f'"humidifier_info":"{escaped_inner_json}"')
                    logger.info(f"Fixed JSON: {fixed_data}")
            
            data = json.loads(fixed_data)
            logger.info(f"Successfully parsed manually: {data}")
        except Exception as e:
            logger.error(f"Manual JSON parsing also failed: {e}")
            return jsonify({"error": "Invalid JSON data"}), 400
    
    
    try:
        if "device_id" not in data:
            return jsonify({"error": "Missing required field: device_id"}), 400
        if "humidifier_info" not in data:
            return jsonify({"error": "Missing required field: humidifier_info"}), 400
            
        device_id = data["device_id"]
        humidifier_info = data["humidifier_info"]
        
        if isinstance(humidifier_info, str):
            try:
                humidifier_info = json.loads(humidifier_info)
            except json.JSONDecodeError as e:
                return jsonify({"error": "Invalid JSON in humidifier_info field"}), 400
        
        created_at = data.get("created_at")
        
        logger.info(f"Creating record with device_id={device_id}, humidifier_info={humidifier_info}, created_at={created_at}")
        
        record = health_record_service.create_health_record(
            device_id, humidifier_info, created_at, request.headers.get("X-API-Key")
        )
        
        logger.info(f"Successfully created record with id={record.id}")
        
        return jsonify({
            "id": record.id,
            "device_id": record.device_id,
            "humidifier_info": record.humidifier_info,
            "created_at": record.created_at.isoformat() + "Z"
        }), 201
    except KeyError as e:
        logger.error(f"KeyError: {str(e)}")
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@health_api.route("/api/v1/health-dehumidifier/data-records", methods=["GET"])
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

@health_api.route("/api/v1/health-dehumidifier/data-records/latest", methods=["GET"])
def get_latest_health_record_by_device():
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    device_id = request.args.get("device_id")
    if not device_id:
        return jsonify({"error": "Missing required query parameter: device_id"}), 400

    record = health_record_service.get_latest_record_by_device_id(device_id)
    if not record:
        return jsonify({"error": "No records found for the specified device_id"}), 404

    result = {
        "id": record.id,
        "device_id": record.device_id,
        "humidifier_info": record.humidifier_info,
        "created_at": record.created_at.isoformat() + "Z" if isinstance(record.created_at, datetime.datetime) else str(record.created_at)
    }
    return jsonify(result), 200

@health_api.route("/api/v1/health-dehumidifier/create-dehumidifier", methods=["POST"])
def create_dehumidifier():
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = None
    try:
        data = request.json
    except Exception as e:
        data = None
    
    if data is None:
        try:
            raw_data = request.get_data(as_text=True)
            
            fixed_data = raw_data
            if '"humidifier_info":"{"' in raw_data:
                import re
                pattern = r'"humidifier_info":"(\{[^}]*\})"'
                match = re.search(pattern, raw_data)
                if match:
                    inner_json = match.group(1)
                    escaped_inner_json = inner_json.replace('"', '\\"')
                    fixed_data = raw_data.replace(match.group(0), f'"humidifier_info":"{escaped_inner_json}"')
            
            data = json.loads(fixed_data)
        except Exception as e:
            logger.error(f"JSON parsing failed: {e}")
            return jsonify({"error": "Invalid JSON data"}), 400

    if not data or "device_id" not in data:
        return jsonify({"error": "Missing required field: device_id"}), 400
    if "humidifier_info" not in data:
        return jsonify({"error": "Missing required field: humidifier_info"}), 400

    try:
        device_id = data["device_id"]
        device_name = data.get("device_name", device_id)
        device_type = data.get("device_type", "dehumidifier")
        humidifier_info = data["humidifier_info"]
        
        if isinstance(humidifier_info, str):
            try:
                humidifier_info = json.loads(humidifier_info)
            except json.JSONDecodeError:
                pass 
        
        if isinstance(humidifier_info, dict):
            humidifier_info = json.dumps(humidifier_info)
        
        logger.info(f"Creating device: device_id={device_id}, device_name={device_name}, device_type={device_type}")
        
        device = health_record_service.create_iot_device(
            device_id, device_name, device_type, humidifier_info, 
            request.headers.get("X-API-Key")
        )
        
        logger.info(f"Successfully created device with id={device.id}")
        
        return jsonify({
            "id": device.id,
            "device_id": device.device_id,
            "device_name": device.device_name,
            "device_type": device.device_type,
            "humidifier_info": device.humidifier_info,
            "created_at": device.created_at.isoformat() + "Z"
        }), 201
        
    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@health_api.route("/api/v1/health-dehumidifier/get-dehumidifier", methods=["GET"])
def get_dehumidifier():
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    device_id = request.args.get("device_id")
    if not device_id:
        return jsonify({"error": "Missing required query parameter: device_id"}), 400

    try:
        logger.info(f"Getting device with device_id={device_id}")
        
        device = health_record_service.get_iot_device_by_id(device_id)
        if not device:
            return jsonify({"error": "Device not found"}), 404

        logger.info(f"Successfully retrieved device with id={device.id}")
        
        # Parse humidifier_info if it's a JSON string
        humidifier_info = device.humidifier_info
        if isinstance(humidifier_info, str):
            try:
                humidifier_info = json.loads(humidifier_info)
            except json.JSONDecodeError:
                pass  # Keep as string if it's not valid JSON
        
        return jsonify({
            "id": device.id,
            "device_id": device.device_id,
            "device_name": device.device_name,
            "device_type": device.device_type,
            "humidifier_info": humidifier_info,
            "created_at": device.created_at.isoformat() + "Z" if isinstance(device.created_at, datetime.datetime) else str(device.created_at),
            "updated_at": device.updated_at.isoformat() + "Z" if device.updated_at and isinstance(device.updated_at, datetime.datetime) else str(device.updated_at) if device.updated_at else None
        }), 200
        
    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@health_api.route("/api/v1/health-dehumidifier/update-dehumidifier", methods=["PUT"])
def update_dehumidifier():
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = None
    try:
        data = request.json
    except Exception as e:
        data = None
    
    if data is None:
        try:
            raw_data = request.get_data(as_text=True)
            
            fixed_data = raw_data
            if '"humidifier_info":"{"' in raw_data:
                import re
                pattern = r'"humidifier_info":"(\{[^}]*\})"'
                match = re.search(pattern, raw_data)
                if match:
                    inner_json = match.group(1)
                    escaped_inner_json = inner_json.replace('"', '\\"')
                    fixed_data = raw_data.replace(match.group(0), f'"humidifier_info":"{escaped_inner_json}"')
            
            data = json.loads(fixed_data)
        except Exception as e:
            logger.error(f"JSON parsing failed: {e}")
            return jsonify({"error": "Invalid JSON data"}), 400

    if not data or "device_id" not in data:
        return jsonify({"error": "Missing required field: device_id"}), 400

    try:
        device_id = data["device_id"]
        device_name = data.get("device_name")
        device_type = data.get("device_type")
        humidifier_info = data.get("humidifier_info")
        is_active = data.get("is_active")
        
        # Handle humidifier_info JSON parsing
        if humidifier_info is not None:
            if isinstance(humidifier_info, str):
                try:
                    humidifier_info = json.loads(humidifier_info)
                except json.JSONDecodeError:
                    pass 
            
            if isinstance(humidifier_info, dict):
                humidifier_info = json.dumps(humidifier_info)
        
        logger.info(f"Updating device: device_id={device_id}, device_name={device_name}, device_type={device_type}")
        
        device = health_record_service.update_iot_device(
            device_id, device_name, device_type, humidifier_info, is_active,
            request.headers.get("X-API-Key")
        )
        
        if not device:
            return jsonify({"error": "Device not found"}), 404
        
        logger.info(f"Successfully updated device with id={device.id}")
        
        return jsonify({
            "id": device.id,
            "device_id": device.device_id,
            "device_name": device.device_name,
            "device_type": device.device_type,
            "humidifier_info": device.humidifier_info,
            "is_active": device.is_active,
            "created_at": device.created_at.isoformat() + "Z" if isinstance(device.created_at, datetime.datetime) else str(device.created_at),
            "updated_at": device.updated_at.isoformat() + "Z" if device.updated_at and isinstance(device.updated_at, datetime.datetime) else str(device.updated_at) if device.updated_at else None
        }), 200
        
    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500