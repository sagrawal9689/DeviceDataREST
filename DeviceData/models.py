from . import db
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime , func
from sqlalchemy.dialects.postgresql import UUID
import uuid

# ALL DB models representing table in db

class Device(db.Model):
    device_id = Column(UUID(as_uuid=True), default=uuid.uuid4 ,nullable=False, primary_key=True)
    name = db.Column(db.String(150),nullable=False)    
    sensors = db.relationship('Sensor')


class Sensor(db.Model):
    sensor_id = Column(UUID(as_uuid=True), default=uuid.uuid4 ,nullable=False,primary_key=True)
    name = db.Column(db.String(150),nullable=False)
    device_id = db.Column(UUID(as_uuid=True), db.ForeignKey('device.device_id'))
    values = db.relationship('Value')

class Value(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    ts = Column(DateTime, nullable=False, default=func.now())
    sensor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('sensor.sensor_id'))