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


class IoTDeviceEdgeApi(Model):
    
    id = AutoField()
    device_id = CharField(unique=True)
    device_name = CharField()
    device_type = CharField(default='dehumidifier')
    humidifier_info = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField(null=True)

    class Meta:
        database = db
        table_name = 'iot_device_edge_api'

