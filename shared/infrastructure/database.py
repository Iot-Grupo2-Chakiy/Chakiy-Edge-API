
from peewee import SqliteDatabase

# Initialize SQLite database
db = SqliteDatabase('chakiy_edge.db')

def init_db() -> None:

    db.connect()
    from iam.infrastructure.models import Device
    from healthDehumidifier.infrastructure.models import DehumidifierRecord
    from routines.infrastructure.models import RoutineRecord
    db.create_tables([Device, DehumidifierRecord, RoutineRecord], safe=True)
    db.close()

