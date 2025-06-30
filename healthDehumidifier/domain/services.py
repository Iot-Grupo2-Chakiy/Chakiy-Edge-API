"""Domain services for the Health-bounded context."""
from datetime import datetime, timezone

from dateutil.parser import parse

from healthDehumidifier.domain.entities import DehumidifierRecord, IoTDevice


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


class IoTDeviceService:
    """Service for managing IoT devices."""
    
    @staticmethod
    def create_device(device_id: str, device_name: str, device_type: str, 
                     humidifier_info: str) -> IoTDevice:
        """Create a new IoT device.
        
        Args:
            device_id (str): Unique identifier for the device
            device_name (str): Human readable name for the device
            device_type (str): Type of device (e.g., 'dehumidifier')
            humidifier_info (str): Device configuration information
            
        Returns:
            IoTDevice: The created device entity
        """
        return IoTDevice(
            device_id=device_id,
            device_name=device_name,
            device_type=device_type,
            humidifier_info=humidifier_info,
            created_at=datetime.now(timezone.utc)
        )
