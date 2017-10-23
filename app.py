from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
import logging
from logging.handlers import RotatingFileHandler
import culqipy
import culqipy1_2
import uuid

from pip import req

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/1_2', methods=['GET'])
def index1_2():
    return render_template('index1_2.html')


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


@app.route('/cargos', methods=['POST'])
def cargos():
    if request.method == 'POST':

        token = request.form['token']

        culqipy1_2.llave_privada = '4QEdt+TTC1vSMga29rdHMz+h2564jFKKl50XWxOFskk='

        cargo = {
                    'token': token,
                    'moneda': 'PEN',
                    'monto': 200,
                    'descripcion': 'Venta de prueba',
                    'pedido': str(uuid.uuid4())[:8],
                    'codigo_pais': 'PE',
                    'direccion': 'Avenida Lima 123',
                    'ciudad': 'Lima',
                    'usuario': 'marti1125',
                    'telefono': 3333339,
                    'nombres': 'Willy',
                    'apellidos': 'Aguirre',
                    'correo_electronico': 'marti1125@gmail.com'
                 }

        cargo_respuesta = culqipy1_2.Cargo.crear(cargo)

        app.logger.info('respuesta creacion de cargo >>> %s', cargo_respuesta)

        return jsonify(cargo_respuesta)

    return jsonify({'error': 'nopost'})


@app.route('/tokens', methods=['POST'])
def tokens():
    if request.method == 'POST':

        token = request.form['token']

        app.logger.info('response token expired >>> %s', token)

        return jsonify(token)

    return jsonify({'error': 'nopost'})


# WEBHOOKS PARA CULQI API V1.2

# TOKEN
@app.route('/webhook_1_2/token/creacion', methods=['POST'])
def creacion_token():
    app.logger.info('response webhook - creacion de token >>> %s', request.data)
    return jsonify({'response': 'creacion de token'})

# CARGO
@app.route('/webhook_1_2/cargo/exitoso', methods=['POST'])
def cargo_exitoso():
    app.logger.info('response webhook - cargo exitoso >>> %s', request.data)
    return jsonify({'response': 'cargo exitoso'})


# WEBHOOKS PARA CULQI API V2

# TOKEN
@app.route('/webhook/token/creation/succeeded', methods=['POST'])
def token_creation_succeeded():
    app.logger.info('response webhook - token creation succeeded >>> %s', request.data)
    return jsonify({'response': 'token creation succeeded'})

# TOKEN
@app.route('/webhook/token/creation/succeeded/nobody', methods=['POST'])
def token_creation_succeeded():
    return '', 204

@app.route('/webhook/token/expired', methods=['POST'])
def token_expired():
    app.logger.info('response webhook - token expired >>> %s', request.data)
    return jsonify({'response': 'token expired'})


@app.route('/webhook/token/creation/failed', methods=['POST'])
def token_creation_failed():
    app.logger.info('response webhook - token creation failed >>> %s', request.data)
    return jsonify({'response': 'token creation failed'})


#CHARGE
@app.route('/webhook/charge/creation/succeeded', methods=['POST'])
def charge_creation_succeeded():
    app.logger.info('response webhook - charge creation succeeded >>> %s', request.data)
    return jsonify({'response': 'charge creation succeeded'})


@app.route('/webhook/charge/creation/failed', methods=['POST'])
def charge_creation_failed():
    app.logger.info('response webhook - charge creation failed >>> %s', request.data)
    return jsonify({'response': 'charge creation failed'})


if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    app.run()
