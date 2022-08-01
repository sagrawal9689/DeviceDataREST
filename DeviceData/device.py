from gc import DEBUG_SAVEALL
from multiprocessing.dummy import Value
from flask import Blueprint, request, jsonify
from DeviceData.models import Device,Sensor
from . import db
import uuid

device= Blueprint('note',__name__)


@device.route('',methods=['POST'])
def create_device():
    db.create_all()
    
    if not request.json or not 'name' in request.json:
        return jsonify('Please provide a Name.'),400

    name = request.json['name']

    new_device = Device(name=name)
    db.session.add(new_device)
    db.session.commit()
    s1 = Sensor(name='temperature sensor',device_id=new_device.device_id,value=0)
    s2 = Sensor(name='pressure sensor',device_id=new_device.device_id,value=0)
    db.session.add(s1)
    db.session.add(s2)
    db.session.commit()

    return jsonify({ 'device_id' : new_device.device_id , 'name': new_device.name }),201


@device.route('/<device_id>',methods=['PATCH'])
def update_device(device_id):
    
    try:
        uuid_obj = uuid.UUID(device_id)
    except ValueError:
        return jsonify('Invalid device Id.'),400

    device = Device.query.filter_by(device_id= uuid_obj).first()

    if not device:
        return jsonify('No device found!'),404

    if not request.json or not 'name' in request.json:
        return jsonify('Please provide a name.'),400

    device.name = request.json['name']
    db.session.commit()

    return jsonify({ 'device_id' : device.device_id, 'name': device.name })