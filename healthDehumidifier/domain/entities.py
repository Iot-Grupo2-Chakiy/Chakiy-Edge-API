# healthDehumidifier/domain/entities.py
from datetime import datetime

class DehumidifierRecord:

    def __init__(self, device_id: str, humidifier_info: str, created_at: datetime, id: int = None):

        self.id = id
        self.device_id = device_id
        self.humidifier_info = humidifier_info
        self.created_at = created_at


class IoTDevice:
    
    def __init__(self, device_id: str, device_name: str, device_type: str, 
                 humidifier_info: str,  
                 created_at: datetime = None, updated_at: datetime = None, id: int = None):
        
        self.id = id
        self.device_id = device_id
        self.device_name = device_name
        self.device_type = device_type
        self.humidifier_info = humidifier_info
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at