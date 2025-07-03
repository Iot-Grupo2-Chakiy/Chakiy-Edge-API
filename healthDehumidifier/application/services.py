"""Application services for the Health-bounded context."""

from healthDehumidifier.domain.entities import DehumidifierRecord, IoTDevice
from healthDehumidifier.domain.services import HealthRecordService, IoTDeviceService
from healthDehumidifier.infrastructure.repositories import DehumidifierRecordRepository, IoTDeviceRepository
from iam.infrastructure.repositories import DeviceRepository

class DehumidifierRecordApplicationService:

    def __init__(self):
        self.health_record_repository = DehumidifierRecordRepository()
        self.health_record_service = HealthRecordService()
        self.device_repository = DeviceRepository()
        self.iot_device_repository = IoTDeviceRepository()
        self.iot_device_service = IoTDeviceService()

    def create_health_record(self, device_id: str, device_information: str, created_at: str,
                             api_key: str) -> DehumidifierRecord:
        if not self.device_repository.find_by_api_key(api_key):
            raise ValueError("Wrong api key")
        record = self.health_record_service.create_record(device_id, device_information, created_at)
        return self.health_record_repository.save(record)

    def get_all_records(self):
        return self.health_record_repository.get_all()

    def get_latest_record_by_device_id(self, device_id: str):
        return self.health_record_repository.get_latest_by_device_id(device_id)
    
    def get_iot_device_by_id(self, device_id: str):
        """Get an IoT device by device_id.
        
        Args:
            device_id (str): The device_id to search for
            
        Returns:
            IoTDevice: The device if found, None otherwise
        """
        return self.iot_device_repository.find_by_device_id(device_id)
    
    def update_iot_device(self, device_id: str, device_name: str = None, device_type: str = None, 
                         humidifier_info: str = None, api_key: str = None):
        """Update an existing IoT device.
        
        Args:
            device_id (str): The device_id to update
            device_name (str, optional): New device name
            device_type (str, optional): New device type
            humidifier_info (str, optional): New humidifier info
            api_key (str): API key for authentication
            
        Returns:
            IoTDevice: The updated device, None if not found
            
        Raises:
            ValueError: If API key is invalid
        """
        # Validate API key
        if api_key and not self.device_repository.find_by_api_key(api_key):
            raise ValueError("Wrong api key")
        
        # Get existing device
        existing_device = self.iot_device_repository.find_by_device_id(device_id)
        if not existing_device:
            return None
        
        # Update the device
        return self.iot_device_repository.update(
            device_id, device_name, device_type, humidifier_info
        )
    
    def update_iot_device_estado(self, device_id: str, estado: bool, api_key: str = None):
        """Update only the estado field in humidifier_info of an IoT device.
        
        Args:
            device_id (str): The device_id to update (can be numeric id as string)
            estado (bool): New estado value
            api_key (str, optional): API key for authentication
            
        Returns:
            IoTDevice: The updated device, None if not found
            
        Raises:
            ValueError: If API key is invalid
        """
        # Validate API key
        if api_key and not self.device_repository.find_by_api_key(api_key):
            raise ValueError("Wrong api key")
        
        # Update the device estado
        return self.iot_device_repository.update_estado(device_id, estado)
    
    def create_iot_device(self, device_id: str, device_name: str, device_type: str, 
                         humidifier_info: str, api_key: str) -> IoTDevice:
        """Create a new IoT device.
        
        Args:
            device_id (str): Unique identifier for the device
            device_name (str): Human readable name for the device
            device_type (str): Type of device
            humidifier_info (str): Device configuration information
            api_key (str): API key for authentication
            
        Returns:
            IoTDevice: The created device
            
        Raises:
            ValueError: If API key is invalid or device_id already exists
        """
        # Validate API key
        if not self.device_repository.find_by_api_key(api_key):
            raise ValueError("Wrong api key")
        
        # Check if device already exists
        existing_device = self.iot_device_repository.find_by_device_id(device_id)
        if existing_device:
            raise ValueError(f"Device with device_id '{device_id}' already exists")
        
        # Create the device
        device = self.iot_device_service.create_device(device_id, device_name, device_type, humidifier_info)
        return self.iot_device_repository.save(device)