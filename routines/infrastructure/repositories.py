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
    def find_by_iot_device_id(device_id: str) -> list[RoutineRecord]:
        records = RoutineRecordModel.select()
        result = []
        for r in records:
            if r.device_id == device_id:
                result.append(RoutineRecord(
                    r.device_id,
                    r.routine_data,
                    r.created_at,
                    r.id
                ))
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

    @staticmethod
    def delete(record_id: str) -> bool:
        """Delete a routine record by its ID"""
        try:
            record = RoutineRecordModel.get(RoutineRecordModel.id == record_id)
            record.delete_instance()
            return True
        except RoutineRecordModel.DoesNotExist:
            return False
