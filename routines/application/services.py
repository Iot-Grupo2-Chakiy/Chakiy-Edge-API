"""Application services for the Routines-bounded context."""

from routines.domain.entities import RoutineRecord
from routines.domain.services import RoutineService
from routines.infrastructure.repositories import RoutineRecordRepository
from iam.infrastructure.repositories import DeviceRepository


class RoutineRecordApplicationService:
    def __init__(self):
        self.routine_record_repository = RoutineRecordRepository()
        self.routine_service = RoutineService()
        self.device_repository = DeviceRepository()

    def create_routine_record(self, device_id: str, routine_data: str, created_at: str, api_key: str) -> RoutineRecord:
        if not self.device_repository.find_by_api_key(api_key):
            raise ValueError("Device not found or unauthorized")

        record = self.routine_service.create_record(device_id, routine_data, created_at)
        return self.routine_record_repository.save(record)

    def get_all_routine_records(self):
        return self.routine_record_repository.get_all()

    def get_routines_by_device(self, iot_device_id: str):
        print(f"Buscando rutinas para iot_device_id: {iot_device_id}")
        return self.routine_record_repository.find_by_iot_device_id(iot_device_id)

    def get_routine_record_by_id(self, record_id: str) -> RoutineRecord:
        record = self.routine_record_repository.find_by_id(record_id)
        if not record:
            raise ValueError("Routine record not found")
        return record

    def delete_routine_record(self, record_id: str) -> bool:
        """Delete a routine record by its ID"""
        return self.routine_record_repository.delete(record_id)