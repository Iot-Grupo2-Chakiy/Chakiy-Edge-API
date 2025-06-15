from datetime import datetime

class RoutineRecord:
    def __init__(self, device_id: str, routine_data: str, created_at: datetime, id: str = None):
        self.id = id
        self.device_id = device_id
        self.routine_data = routine_data
        self.created_at = created_at
