from routines.domain.entities import RoutineRecord
from routines.infrastructure.models import RoutineRecord as RoutineRecordModel

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
    def find_by_device_id(device_id: str) -> list[RoutineRecord]:

        records = RoutineRecordModel.select().where(RoutineRecordModel.device_id == device_id)
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
