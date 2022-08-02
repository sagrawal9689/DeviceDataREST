from asyncio.log import logger
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logging import FileHandler, WARNING

# db instance 
db= SQLAlchemy()
DB_NAME= "DeviceData"

# create_app function creates the app instance and configures the db, and routes

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'hjshjhdjashkjdhjs'

    # adding logger for all errorlogs
    file_handler= FileHandler('errorlog.txt')
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # configuring the Postgres DB by providing the username, password, dbname etc in the uri
     
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:sahil@localhost/{DB_NAME}'
    db.init_app(app)

    from .controllers.deviceController import device
    from .controllers.sensorController import sensor
    
    # Sensor related routes
    app.register_blueprint(sensor, url_prefix='/devices/<device_id>/sensors')

    # Device related routes
    app.register_blueprint(device, url_prefix='/devices')

    return app