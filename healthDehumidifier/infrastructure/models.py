
from peewee import Model, AutoField, FloatField, CharField, DateTimeField

from shared.infrastructure.database import db


class DehumidifierRecord(Model):

    id = AutoField()
    device_id = CharField()
    humidifier_info = CharField()
    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'dehumidifier_records'

