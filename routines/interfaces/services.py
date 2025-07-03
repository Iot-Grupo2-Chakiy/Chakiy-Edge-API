from flask import Blueprint, request, jsonify

from routines.application.services import RoutineRecordApplicationService
from iam.interfaces.services import authenticate_request
import datetime

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
        
        if isinstance(routine_data, str):
            try:
                import json
                routine_data = json.loads(routine_data)
                print("Parsed routine_data:", routine_data)
            except json.JSONDecodeError as e:
                print(f"Error parsing routine_data JSON: {e}")
                return jsonify({"error": "Invalid routine_data JSON format"}), 400
        
        record = routine_record_service.create_routine_record(
            device_id, routine_data, created_at, request.headers.get("X-API-Key")
        )
        
        return jsonify({
            "id": record.id,
            "device_id": record.device_id,
            "routine_data": record.routine_data,
            "created_at": record.created_at.isoformat() + "Z"
        }), 201
        
    except KeyError as e:
        print(f"Missing required field: {e}")
        return jsonify({"error": f"Missing required field: {e}"}), 400
    except ValueError as e:
        print(f"ValueError: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

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

@routine_api.route("/api/v1/routine-monitoring/data-records/device/<device_id>/routine/<routine_id>", methods=["DELETE"])
def delete_routine_record_by_device_and_routine_id(device_id, routine_id):
    """Delete routine record by device_id and routine ID from the backend"""
    auth_result = authenticate_request()
    if auth_result:
        return auth_result
    
    try:
        print(f"Attempting to delete routine record by device_id: {device_id} and routine_id: {routine_id}")
        
        # First, let's check all records to see what we have
        all_records = routine_record_service.get_all_routine_records()
        print(f"Total records in database: {len(all_records)}")
        
        # Find record by device_id and routine_id in routine_data
        # Try both methods to find the record
        records = routine_record_service.get_routines_by_device(device_id)
        print(f"Records found by get_routines_by_device for '{device_id}': {len(records) if records else 0}")
        
        # If no records found by device, let's search manually in all records
        if not records:
            print(f"No records found by get_routines_by_device, searching manually in all records...")
            records = []
            for record in all_records:
                if record.device_id == device_id:
                    records.append(record)
                    print(f"Found record with matching device_id: {record.device_id}")
        
        target_record = None
        
        for record in records:
            routine_data = record.routine_data
            print(f"Checking record ID: {record.id}, device_id: {record.device_id}")
            print(f"Raw routine_data: {repr(routine_data)}")
            print(f"routine_data type: {type(routine_data)}")
            
            if isinstance(routine_data, str):
                import json
                try:
                    routine_data = json.loads(routine_data)
                    print(f"Parsed routine_data: {routine_data}")
                except json.JSONDecodeError as e:
                    print(f"Failed to parse routine_data as JSON: {e}")
                    print(f"Trying to fix potential JSON issues...")
                    # Try to fix common JSON issues
                    try:
                        # Remove potential escaping issues
                        fixed_data = routine_data.replace('\\"', '"').replace('\\n', '').replace('\\t', '')
                        routine_data = json.loads(fixed_data)
                        print(f"Successfully parsed after fixing: {routine_data}")
                    except:
                        print(f"Still failed after attempting to fix, trying eval...")
                        # If it's a Python dict string representation, try using eval
                        try:
                            import ast
                            routine_data = ast.literal_eval(routine_data)
                            print(f"Successfully parsed using ast.literal_eval: {routine_data}")
                        except:
                            print(f"ast.literal_eval also failed, skipping this record")
                            continue
            
            if isinstance(routine_data, dict) and str(routine_data.get('id')) == str(routine_id):
                target_record = record
                print(f"Found matching routine: device_id={record.device_id}, routine_id={routine_data.get('id')}")
                break
        
        if not target_record:
            print(f"No routine record found with device_id: {device_id} and routine_id: {routine_id}")
            print("Available records:")
            for record in all_records:
                routine_data = record.routine_data
                print(f"  Record ID: {record.id}, device_id: {record.device_id}")
                print(f"    Raw routine_data: {repr(routine_data)[:500]}...")  
                if isinstance(routine_data, str):
                    try:
                        routine_data = json.loads(routine_data)
                        routine_id_in_data = routine_data.get('id')
                        print(f"    Parsed routine_id: {routine_id_in_data}")
                    except:
                        try:
                            import ast
                            routine_data = ast.literal_eval(routine_data)
                            routine_id_in_data = routine_data.get('id')
                            print(f"    Parsed routine_id using ast: {routine_id_in_data}")
                        except:
                            print(f"    Failed to parse JSON or eval")
                else:
                    routine_id_in_data = routine_data.get('id') if isinstance(routine_data, dict) else 'N/A'
                    print(f"    routine_id: {routine_id_in_data}")
            return jsonify({"error": f"No routine record found with device_id: {device_id} and routine_id: {routine_id}"}), 404
        
        # Delete the found record
        deleted = routine_record_service.delete_routine_record(target_record.id)
        
        if deleted:
            print(f"Successfully deleted routine record with device_id: {device_id} and routine_id: {routine_id}")
            return jsonify({
                "message": f"Routine record with device_id {device_id} and routine_id {routine_id} deleted successfully",
                "deleted_device_id": device_id,
                "deleted_routine_id": routine_id,
                "deleted_record_id": target_record.id
            }), 200
        else:
            return jsonify({"error": "Failed to delete record"}), 500
            
    except ValueError as e:
        print(f"ValueError: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Unexpected error deleting record: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500