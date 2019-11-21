from datetime import datetime
from flask import Flask, jsonify, make_response


app = Flask(__name__)


@app.route('/')
def healthcheck():
    res = {'status': 'OK'}
    return make_response(jsonify(res))


@app.route('/aircon/off', methods=['post'])
def off():
    res = {
            'timestamp': get_timestamp(),
            'command': "off"
            }
    return make_response(jsonify(res))


@app.route('/aircon/<command>/<temp>', methods=['post'])
def send_signal(command, temp):
    res = {
            'timestamp': get_timestamp(),
            'command': command + '_' + temp,
            'status': 'OK'
            }
    return make_response(jsonify(res))


@app.route('/temperature')
def get_temperature():
    res = {
            'timestamp': get_timestamp(),
            'temperature': '25.5',
            'humidity': '45.5',
            'status': 'OK'
            }
    return make_response(jsonify(res))


def get_timestamp():
    return datetime.now().isoformat()


if __name__ == '__main__':
    app.run()
