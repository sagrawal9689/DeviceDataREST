from flask import Blueprint, request, jsonify
from DeviceData.models import Device
from DeviceData.models import Sensor
from .. import db
import uuid
import logging 

device= Blueprint('note',__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:%(message)s')

file_handler = logging.FileHandler('device.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# @desc    Create Device
# @route   POST /devices
# @access  Public

@device.route('',methods=['POST'])
def create_device():
    if not request.json or not 'name' in request.json:
        return jsonify('Please provide a Name.'),400

    name = request.json['name']

    # new device created with the provided name in the request body
    new_device = Device(name=name)
    db.session.add(new_device)
    db.session.commit()
    # new_device commited to the db

    # logging the info to the log file
    logger.info(f'Created Device: {new_device.name} - {new_device.device_id}')

    # adding two default sensor for the new_device created above

    s1 = Sensor(name='temperature sensor',device_id=new_device.device_id)
    s2 = Sensor(name='pressure sensor',device_id=new_device.device_id)
    db.session.add(s1)
    db.session.add(s2)
    db.session.commit()
    # s1 and s2 commited to the db
    logger.info(f'Created Sensor: {s1.name} - {s1.sensor_id} for device: {new_device.name} - {new_device.device_id}')
    logger.info(f'Created Sensor: {s2.name} - {s2.sensor_id} for device: {new_device.name} - {new_device.device_id}')

    # sending the information about the newly created device as the response
    return jsonify({ 'device_id' : new_device.device_id , 'name': new_device.name }),201

# @desc    Update a device name
# @route   PATCH /devices/<device_id>
# @access  Public

@device.route('/<device_id>',methods=['PATCH'])
def update_device(device_id):
    
    try:
        uuid_obj = uuid.UUID(device_id)
    except ValueError:
        return jsonify('Invalid device Id.'),400

    # getting the device with the provided device_id

    device = Device.query.filter_by(device_id= uuid_obj).first()

    if not device:
        return jsonify('No device found!'),404

    if not request.json or not 'name' in request.json:
        return jsonify('Please provide a name.'),400

    # updating name of device

    device.name = request.json['name']

    db.session.commit()
    # commiting the changes to the db
    logger.info(f'Updated Device: {device.name} - {device.device_id}')

    # sending the information about the updated device as the response
    return jsonify({ 'device_id' : device.device_id, 'name': device.name })