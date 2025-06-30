# healthDehumidifier/infrastructure/repositories.py
from healthDehumidifier.domain.entities import DehumidifierRecord, IoTDevice
from healthDehumidifier.infrastructure.models import DehumidifierRecord as DehumidifierRecordModel, IoTDeviceEdgeApi
from datetime import datetime

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

    @staticmethod
    def get_latest_by_device_id(device_id: str):
        try:
            # Get the most recent record for the specified device_id
            record = (DehumidifierRecordModel
                     .select()
                     .where(DehumidifierRecordModel.device_id == device_id)
                     .order_by(DehumidifierRecordModel.created_at.desc())
                     .get())
            
            return DehumidifierRecord(
                record.device_id,
                record.humidifier_info,
                record.created_at,
                record.id
            )
        except DehumidifierRecordModel.DoesNotExist:
            return None


class IoTDeviceRepository:
    
    @staticmethod
    def save(device: IoTDevice) -> IoTDevice:
        device_model = IoTDeviceEdgeApi.create(
            device_id=device.device_id,
            device_name=device.device_name,
            device_type=device.device_type,
            humidifier_info=device.humidifier_info,
            created_at=device.created_at,
            updated_at=device.updated_at
        )
        
        return IoTDevice(
            device.device_id,
            device.device_name,
            device.device_type,
            device.humidifier_info,
            device.created_at,
            device.updated_at,
            device_model.id
        )
    
    @staticmethod
    def find_by_device_id(device_id: str):
        try:
            device_model = IoTDeviceEdgeApi.get(IoTDeviceEdgeApi.device_id == device_id)
            return IoTDevice(
                device_model.device_id,
                device_model.device_name,
                device_model.device_type,
                device_model.humidifier_info,
                device_model.created_at,
                device_model.updated_at,
                device_model.id
            )
        except IoTDeviceEdgeApi.DoesNotExist:
            return None
    
    @staticmethod
    def get_all():
        devices = IoTDeviceEdgeApi.select()
        return [
            IoTDevice(
                d.device_id,
                d.device_name,
                d.device_type,
                d.humidifier_info,
                d.is_active,
                d.created_at,
                d.updated_at,
                d.id
            )
            for d in devices
        ]

    @staticmethod
    def update(device_id: str, device_name: str = None, device_type: str = None, 
               humidifier_info: str = None, is_active: str = None):
        """Update an existing IoT device.
        
        Args:
            device_id (str): The device_id to update
            device_name (str, optional): New device name
            device_type (str, optional): New device type  
            humidifier_info (str, optional): New humidifier info
            is_active (str, optional): New active status
            
        Returns:
            IoTDevice: The updated device, None if not found
        """
        try:
            from datetime import datetime, timezone
            
            # Get the existing device
            device_model = IoTDeviceEdgeApi.get(IoTDeviceEdgeApi.device_id == device_id)
            
            # Update only the fields that are provided
            update_data = {"updated_at": datetime.now(timezone.utc)}
            
            if device_name is not None:
                update_data["device_name"] = device_name
            if device_type is not None:
                update_data["device_type"] = device_type
            if humidifier_info is not None:
                update_data["humidifier_info"] = humidifier_info
            if is_active is not None:
                update_data["is_active"] = is_active
            
            # Perform the update
            query = IoTDeviceEdgeApi.update(**update_data).where(IoTDeviceEdgeApi.device_id == device_id)
            query.execute()
            
            # Get the updated device
            updated_device = IoTDeviceEdgeApi.get(IoTDeviceEdgeApi.device_id == device_id)
            
            return IoTDevice(
                updated_device.device_id,
                updated_device.device_name,
                updated_device.device_type,
                updated_device.humidifier_info,
                updated_device.is_active,
                updated_device.created_at,
                updated_device.updated_at,
                updated_device.id
            )
        except IoTDeviceEdgeApi.DoesNotExist:
            return None