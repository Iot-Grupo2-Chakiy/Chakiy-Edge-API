
from peewee import Model, AutoField, FloatField, CharField, DateTimeField

from shared.infrastructure.database import db


class RoutineRecord(Model):

    id = AutoField()
    device_id = CharField()
    routine_data = CharField()
    created_at = DateTimeField()


    class Meta:
        database = db
        table_name = 'routine_records'

