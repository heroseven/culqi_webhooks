from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
import logging
from logging.handlers import RotatingFileHandler
import culqipy

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/token', methods=['GET'])
def token():
    return render_template('token.html')


@app.route('/charges', methods=['POST'])
def charge():
    if request.method == 'POST':

        token = request.form['token']
        installments = request.form['installments']

        culqipy.secret_key = 'sk_test_UTCQSGcXW8bCyU59'

        charge = {'amount': 3500,
                  'capture': True,
                  'currency_code': 'PEN',
                  'description': 'Culqi Store',
                  'email': 'wmuro@me.com',
                  'installments': installments,
                  'metadata': {'order_id': '1234'},
                  'source_id': token}

        charge = culqipy.Charge.create(charge)

        app.logger.info('response charge >>> %s', charge)

        return jsonify(charge)

    return jsonify({'error': 'nopost'})


@app.route('/tokens', methods=['POST'])
def tokens():
    if request.method == 'POST':

        token = request.form['token']

        app.logger.info('response token expired >>> %s', token)

        return jsonify(token)

    return jsonify({'error': 'nopost'})


# TOKEN
@app.route('/webhook/token/creation/succeeded', methods=['POST'])
def token_creation_succeeded():
    app.logger.info('response webhook - token creation succeeded >>> %s', charge)
    return jsonify({'response': 'token creation succeeded'})


@app.route('/webhook/token/expired', methods=['POST'])
def token_expired():
    app.logger.info('response webhook - token expired >>> %s', charge)
    return jsonify({'response': 'token expired'})


@app.route('/webhook/token/creation/failed', methods=['POST'])
def token_creation_failed():
    app.logger.info('response webhook - token creation failed >>> %s', charge)
    return jsonify({'response': 'token creation failed'})


#CHARGE
@app.route('/webhook/charge/creation/succeeded', methods=['POST'])
def charge_creation_succeeded():
    app.logger.info('response webhook - charge creation succeeded >>> %s', charge)
    return jsonify({'response': 'charge creation succeeded'})


@app.route('/webhook/charge/creation/failed', methods=['POST'])
def charge_creation_failed():
    app.logger.info('response webhook - charge creation failed >>> %s', charge)
    return jsonify({'response': 'charge creation failed'})


if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    app.run()
