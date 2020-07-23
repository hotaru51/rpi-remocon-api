import os
import subprocess
import re
import time
from datetime import datetime
from yaml import load, SafeLoader as Loader
from flask import Flask, jsonify, make_response
import RPi.GPIO as GPIO
import dht11


app = Flask(__name__)

# GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# rpi-remocon-api config
config_file = open(os.path.dirname(os.path.realpath(__file__)) + '/config/config.yaml')
config = load(config_file, Loader=Loader)

sensor = dht11.DHT11(pin=config['gpio_pin']['temperature'])


@app.route('/')
def healthcheck():
    res = {'status': 'ok'}
    return make_response(jsonify(res))


@app.route('/aircon/off', methods=['post'])
def off():
    if send_signal('off'):
        status = 'ok'
    else:
        status = 'ng'

    res = {
            'timestamp': get_timestamp(),
            'command': "off",
            'status': status
            }
    return make_response(jsonify(res))


@app.route('/aircon/<command>/<temp>', methods=['post'])
def aircon(command, temp):
    if send_signal(command, temp):
        status = 'ok'
    else:
        status = 'ng'
    res = {
            'timestamp': get_timestamp(),
            'command': command + '_' + temp,
            'status': status
            }
    return make_response(jsonify(res))


@app.route('/temperature')
def temperature():
    result = get_temperature_and_humidity()
    if result is not None:
        res = {
                'timestamp': get_timestamp(),
                'temperature': result['temperature'],
                'humidity': result['humidity'],
                'status': 'ok'
                }
    else:
        res = {
                'timestamp': get_timestamp(),
                'temperature': None,
                'humidity': None,
                'status': 'ng'
                }

    return make_response(jsonify(res))


def get_timestamp():
    return datetime.now().isoformat()


def send_signal(command, temp=None):
    if temp is None:
        signal = 'aircon:' + remove_symbols(command)
    else:
        signal = 'aircon:' + remove_symbols(command) + '_' + remove_symbols(temp)

    ir_command = [
            '/usr/local/bin/irrp', '-p',
            '-g', str(config['gpio_pin']['ir']),
            '-f', os.path.dirname(os.path.realpath(__file__)) + '/signals/aircon',
            signal
            ]


    result = True
    try:
        # TODO: 存在しないIDで送信しようとしてもirrpの終了ステータスが0になるので対策する
        subprocess.run(ir_command, check=True)
    except subprocess.CalledProcessError:
        result = False

    return result


def remove_symbols(text):
    pattern = '[^a-z0-9]'
    return re.sub(pattern, '', text)


def get_temperature_and_humidity():
    for n in range(config['sensor']['retry_count']):
        result = sensor.read()
        if result.is_valid():
            return {
                    'temperature': result.temperature,
                    'humidity': result.humidity
                    }
        else:
            time.sleep(config['sensor']['interval'])
    return None


# TODO: 適切なエラーハンドリングの実装
@app.errorhandler(Exception)
def error(e):
    res = {
            'timestamp': get_timestamp(),
            'status': 'ng',
            'message': 'exception'
            }

    return jsonify(res)


if __name__ == '__main__':
    app.run()
