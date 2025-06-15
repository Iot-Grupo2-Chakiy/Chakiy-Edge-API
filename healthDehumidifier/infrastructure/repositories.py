# healthDehumidifier/infrastructure/repositories.py
from healthDehumidifier.domain.entities import DehumidifierRecord
from healthDehumidifier.infrastructure.models import DehumidifierRecord as DehumidifierRecordModel

class DehumidifierRecordRepository:

    @staticmethod
    def save(dehumidifier_record) -> DehumidifierRecord:

        record = DehumidifierRecordModel.create(
            device_id        = dehumidifier_record.device_id,
            humidifier_info  = dehumidifier_record.humidifier_info,
            created_at       = dehumidifier_record.created_at
        )
        return DehumidifierRecord(
            dehumidifier_record.device_id,
            dehumidifier_record.humidifier_info,
            dehumidifier_record.created_at,
            record.id
        )
    @staticmethod
    def get_all():

        records = DehumidifierRecordModel.select()
        return [
            DehumidifierRecord(
                r.device_id,
                r.humidifier_info,
                r.created_at,
                r.id
            )
            for r in records
        ]