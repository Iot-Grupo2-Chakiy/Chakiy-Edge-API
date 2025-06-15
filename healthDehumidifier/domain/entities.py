# healthDehumidifier/domain/entities.py
from datetime import datetime

class DehumidifierRecord:


    def __init__(self, device_id: str, humidifier_info: str, created_at: datetime, id: int = None):

        self.id = id
        self.device_id = device_id
        self.humidifier_info = humidifier_info
        self.created_at = created_at