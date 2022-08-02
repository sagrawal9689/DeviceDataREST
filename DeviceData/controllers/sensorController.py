import datetime
from flask import Blueprint, request, jsonify
from DeviceData.models import Device
from DeviceData.models import Sensor
from DeviceData.models import Value
from .. import db
import uuid
import logging

sensor= Blueprint('sensor',__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:%(message)s')

file_handler = logging.FileHandler('sensor.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# @desc    Create a Sensor
# @route   POST /devices/<device_id>/sensors
# @access  Public

@sensor.route('/',methods=['POST'])
def create_sensor(device_id):

    try:
        uuid_obj = uuid.UUID(device_id)
    except ValueError:
        return jsonify('Invalid device Id.'),400

    # getting the device with the provided device_id in the url.

    device = Device.query.filter_by(device_id= uuid_obj).first()

    if not device:
        return jsonify('No device found!'),404

    if not request.json or not 'name' in request.json:
        return jsonify('Please provide a name.'),400

    # new sensor created with the provided name in the request body.

    new_sensor = Sensor(name=request.json['name'], device_id= uuid_obj)

    db.session.add(new_sensor)
    db.session.commit()
    # new_sensor commited to the db.

    logger.info(f'Created Sensor: {new_sensor.name} - {new_sensor.sensor_id} for device: {device.name} - {device.device_id}')

    return jsonify({ 'sensor_id' : new_sensor.sensor_id, 'name': new_sensor.name , 'device_id': new_sensor.device_id }),201



# @desc    Create a Sensor Value
# @route   POST /devices/<device_id>/sensors/<sensor_id>/values
# @access  Public

@sensor.route('/<sensor_id>/values',methods=['POST'])
def create_sensor_value(device_id,sensor_id):
    
    try:
        device_uuid_obj = uuid.UUID(device_id)
    except ValueError:
        return jsonify('Invalid device Id.'),400

    # getting the device with the provided device_id in the url.

    device = Device.query.filter_by(device_id= device_uuid_obj).first()

    if not device:
        return jsonify('No device found!'),404

    try:
        sensor_uuid_obj = uuid.UUID(sensor_id)
    except ValueError:
        return jsonify('Invalid sensor Id.'),400

    # getting the sensor belonging to device having the sensor_id given in the url.
    sensor = Sensor.query.filter_by(sensor_id= sensor_uuid_obj,device_id=device_uuid_obj).first()

    if not sensor:
        return jsonify('No Sensor found!'),404
    
    if not request.json or not 'value' in request.json:
        return jsonify('Please provide a value.'),400

    # new sensor value created for the sensor with the provided value in the request body having timestamp equal to time.now()

    new_sensor_value = Value(value=request.json['value'], sensor_id= sensor_uuid_obj)

    db.session.add(new_sensor_value)
    db.session.commit()

    logger.info(f'inserted Sensor Value: {sensor.name} - {sensor.sensor_id} value : {new_sensor_value.value} - at ts {new_sensor_value.ts}')

    return jsonify({ 'sensor_id' : new_sensor_value.sensor_id, 'value': new_sensor_value.value, 'id': new_sensor_value.id, 'ts': new_sensor_value.ts }),201


# @desc    Get sensor values between a time range
# @route   GET /devices/<device_id>/sensors/<sensor_id>/values?tsStart=321235&tsEnd=321235
# @access  Public

@sensor.route('/<sensor_id>/values',methods=['GET'])
def get_sensor_value(device_id,sensor_id):

    try:
        device_uuid_obj = uuid.UUID(device_id)
    except ValueError:
        return jsonify('Invalid device Id.'),400

    # getting the device with the provided device_id in the url.
    device = Device.query.filter_by(device_id= device_uuid_obj).first()

    if not device:
        return jsonify('No device found!'),404

    try:
        sensor_uuid_obj = uuid.UUID(sensor_id)
    except ValueError:
        return jsonify('Invalid sensor Id.'),400

    # getting the sensor belonging to device having the sensor_id given in the url.
    sensor = Sensor.query.filter_by(sensor_id= sensor_uuid_obj,device_id=device_uuid_obj).first()

    if not sensor:
        return jsonify('No Sensor found!'),404
    
    # if query parametes provided filter result according to time range
    if request.args.get('tsStart') and request.args.get('tsEnd'):
        tsStart = request.args.get('tsStart')
        tsEnd = request.args.get('tsEnd')

        try:
            timestampStart = datetime.datetime.fromtimestamp(int(tsStart))
            timestampeEnd = datetime.datetime.fromtimestamp(int(tsEnd))  
        except Exception:
            return jsonify('Invalid Start and End Time.'),400

        values_obj = Value.query.filter(Value.sensor_id ==sensor_id,
                                    Value.ts>= timestampStart,
                                    Value.ts<= timestampeEnd,
                                    ).all()
    else:
        values_obj = Value.query.filter(Value.sensor_id ==sensor_id
                                    ).all()
    
    # convert values_obj(array of object of type Value) to array of dictionary
    values = []

    for value in values_obj:
        value_data = {}
        value_data['id'] = value.id
        value_data['value'] = value.value
        value_data['ts'] = value.ts
        value_data['sensor_id'] = value.sensor_id
        values.append(value_data)
        
    # sending the array of sensor values as response
    return jsonify(values)