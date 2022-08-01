from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()
DB_NAME= "DeviceData"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjashkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:sahil@localhost/{DB_NAME}'
    db.init_app(app)

    from .device import device
    from .sensor import sensor
    
    app.register_blueprint(device, url_prefix='/devices')
    app.register_blueprint(sensor, url_prefix='/devices/<device_id>/<sensor_id>')

    return app