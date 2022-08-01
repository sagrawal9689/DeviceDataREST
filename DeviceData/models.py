from . import db
# from sqlalchemy.sql import func
from sqlalchemy import Column, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Device(db.Model):
    device_id = Column(UUID(as_uuid=True), default=uuid.uuid4 ,nullable=False, primary_key=True)
    name = db.Column(db.String(150),nullable=False)    
    sensors = db.relationship('Sensor')

class Sensor(db.Model):
    sensor_id = Column(UUID(as_uuid=True), default=uuid.uuid4 ,nullable=False,primary_key=True)
    name = db.Column(db.String(150),nullable=False)
    value = Column(Float, nullable=False)
    device_id = db.Column(UUID(as_uuid=True), db.ForeignKey('device.device_id'))