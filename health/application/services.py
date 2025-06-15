"""Application services for the Health-bounded context."""

from health.domain.entities import HealthRecord
from health.domain.services import HealthRecordService
from health.infrastructure.repositories import HealthRecordRepository
from iam.infrastructure.repositories import DeviceRepository

class HealthRecordApplicationService:
    """Application service for creating health records."""

    def __init__(self):
        """Initialize the HealthRecordApplicationService."""
        self.health_record_repository = HealthRecordRepository()
        self.health_record_service = HealthRecordService()
        self.device_repository = DeviceRepository()

    def create_health_record(self, device_id: str, bpm: float, created_at: str, api_key: str) -> HealthRecord:
        """Create a health record after validating the device.

        Args:
            device_id (str): Device identifier.
            bpm (float): Heart rate in beats per minute.
            created_at (str): ISO 8601 timestamp.
            api_key (str): API key for device authentication.

        Returns:
            HealthRecord: The created health record.

        Raises:
            ValueError: If the device_id and api_key are invalid.
        """
        # Validate device_id exists in IAM context
        if not self.device_repository.find_by_id_and_api_key(device_id, api_key):
            raise ValueError("Device not found")
        record = self.health_record_service.create_record(device_id, bpm, created_at)
        return self.health_record_repository.save(record)