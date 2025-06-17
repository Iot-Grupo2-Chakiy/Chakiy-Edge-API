from routines.domain.entities import RoutineRecord
from routines.infrastructure.models import RoutineRecord as RoutineRecordModel
import json
import re


class RoutineRecordRepository:

    @staticmethod
    def save(routine_record: RoutineRecord) -> RoutineRecord:

        record = RoutineRecordModel.create(
            device_id    = routine_record.device_id,
            routine_data = routine_record.routine_data,
            created_at   = routine_record.created_at
        )
        return RoutineRecord(
            routine_record.device_id,
            routine_record.routine_data,
            routine_record.created_at,
            record.id
        )

    @staticmethod
    def get_all() -> list[RoutineRecord]:

        records = RoutineRecordModel.select()
        return [
            RoutineRecord(
                r.device_id,
                r.routine_data,
                r.created_at,
                r.id
            )
            for r in records
        ]


    @staticmethod
    def find_by_iot_device_id(iot_device_id: str) -> list[RoutineRecord]:
        records = RoutineRecordModel.select()
        result = []
        for r in records:
            try:
                routine_data_str = r.routine_data
                print(f"routine_data de id {r.id}: {routine_data_str}")
                routine_data_str = routine_data_str.replace("'", '"')
                routine_data_str = re.sub(r'\bTrue\b', 'true', routine_data_str)
                routine_data_str = re.sub(r'\bFalse\b', 'false', routine_data_str)
                data = json.loads(routine_data_str)
                if int(data.get("iotDeviceId", -1)) == int(iot_device_id):
                    result.append(RoutineRecord(
                        r.device_id,
                        r.routine_data,
                        r.created_at,
                        r.id
                    ))
            except Exception as e:
                print(f"Excepción al parsear routine_data con id {r.id}: {e}")
                continue
        return result

    @staticmethod
    def find_by_id(record_id: str) -> RoutineRecord:

        try:
            record = RoutineRecordModel.get(RoutineRecordModel.id == record_id)
            return RoutineRecord(
                record.device_id,
                record.routine_data,
                record.created_at,
                record.id
            )
        except RoutineRecordModel.DoesNotExist:
            return None
