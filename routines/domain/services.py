"""Domain services for the Routines-bounded context."""
from datetime import datetime, timezone
from dateutil.parser import parse
import json

from routines.domain.entities import RoutineRecord


class RoutineService:

    def __init__(self):
        pass

    @staticmethod
    def create_record(device_id: str, routine_data: str, created_at: str | None) -> RoutineRecord:
        try:
            if isinstance(routine_data, str):
                routine_data = json.loads(routine_data)
            if not isinstance(routine_data, dict):
                raise ValueError("routine_data debe ser un JSON válido (dict)")

            if created_at:
                parsed_created_at = parse(created_at).astimezone(timezone.utc)
            else:
                parsed_created_at = datetime.now(timezone.utc)
        except (ValueError, TypeError, json.JSONDecodeError):
            raise ValueError("routine_data debe ser un JSON válido o created_at tiene formato incorrecto")

        return RoutineRecord(device_id=device_id, routine_data=routine_data, created_at=parsed_created_at)

