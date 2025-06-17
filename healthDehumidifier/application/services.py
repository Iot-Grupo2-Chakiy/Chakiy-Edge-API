"""Application services for the Health-bounded context."""

from healthDehumidifier.domain.entities import DehumidifierRecord
from healthDehumidifier.domain.services import HealthRecordService
from healthDehumidifier.infrastructure.repositories import DehumidifierRecordRepository
from iam.infrastructure.repositories import DeviceRepository

class DehumidifierRecordApplicationService:

    def __init__(self):
        self.health_record_repository = DehumidifierRecordRepository()
        self.health_record_service = HealthRecordService()
        self.device_repository = DeviceRepository()

    def create_health_record(self, device_id: str, device_information: str, created_at: str,
                             api_key: str) -> DehumidifierRecord:
        if not self.device_repository.find_by_api_key(api_key):
            raise ValueError("Wrong api key")
        record = self.health_record_service.create_record(device_id, device_information, created_at)
        return self.health_record_repository.save(record)


    def get_all_records(self):
        return self.health_record_repository.get_all()