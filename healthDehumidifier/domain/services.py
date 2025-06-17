"""Domain services for the Health-bounded context."""
from datetime import datetime, timezone

from dateutil.parser import parse

from healthDehumidifier.domain.entities import DehumidifierRecord


class HealthRecordService:
    """Service for managing healthDehumidifier records."""

    def __init__(self):
        """Initialize the HealthRecordService.
        """


    @staticmethod
    def create_record(device_id: str, device_information: str, created_at: str | None) -> DehumidifierRecord:
        """Crea un nuevo registro healthDehumidifier.

        Args:
            device_id (str): Identificador del dispositivo.
            device_information (str): Información del dispositivo.
            created_at (str): Timestamp ISO 8601 (ejemplo: '2025-06-04T18:23:00-05:00').

        Returns:
            DehumidifierRecord: La entidad creada.

        Raises:
            ValueError: Si created_at es inválido.
        """
        try:
            if created_at:
                parsed_created_at = parse(created_at).astimezone(timezone.utc)
            else:
                parsed_created_at = datetime.now(timezone.utc)
        except (ValueError, TypeError):
            raise ValueError("Formato de fecha inválido")

        return DehumidifierRecord(device_id, device_information, parsed_created_at)
