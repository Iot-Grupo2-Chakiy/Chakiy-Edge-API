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
    def create_record(device_id: str, bpm: float, created_at: str | None) -> DehumidifierRecord:

        """Create a new healthDehumidifier record.

                    Args:
                        device_id (str): Device identifier.
                        bpm (float): Heart rate in beats per minute.
                        created_at (str): ISO 8601 timestamp (e.g., '2025-06-04T18:23:00-05:00').

                    Returns:
                        DehumidifierRecord: The created healthDehumidifier record entity.

                    Raises:
                        ValueError: If BPM is invalid (not 0–200) or created_at is malformed.
                    """
        try:
            bpm = float(bpm)
            if not (0 <= bpm <= 200):
                raise ValueError("Invalid BPM value")
            if created_at:
                parsed_created_at = parse(created_at).astimezone(timezone.utc)
            else:
                parsed_created_at = datetime.now(timezone.utc)
        except (ValueError, TypeError):
            raise ValueError("Invalid data format")

        return DehumidifierRecord(device_id, bpm, parsed_created_at)
