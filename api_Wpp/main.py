from flask import Flask, render_template, request, jsonify
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import logging

app = Flask(__name__, template_folder='template')

logging.basicConfig(level=logging.INFO)

account_sid = '' # teu sid twillo
auth_token = '' # Token twillo
from_number = '' # Teu numero twillo ex: whatsapp:+55123456789

client = Client(account_sid, auth_token)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/send-message', methods=['POST'])
def send_message():
    print(client)

    try:
        if not request.is_json:
            app.logger.error('A solicitação não tem o tipo de conteúdo JSON.')
            return jsonify({'error': 'Solicitação deve ter o Content-Type como application/json.'}), 400
        
        data = request.get_json()
        app.logger.info(f'Recebido: {data}')
    
        number = data.get('to')
        bodyCabra = data.get('message')
        app.logger.info(f'Mensagem recebida: {bodyCabra}')
        
        if not number or not bodyCabra:
            app.logger.error('Número de telefone ou mensagem ausente no JSON.')
            return jsonify({'error': 'Número de telefone e mensagem são obrigatórios.'}), 400

        message = client.messages.create(
            from_=from_number,
            body="tesetese", # msg 
            to=f'whatsapp:{number}' # numero que vai receber a msg
        )

        return jsonify({'message_sid': message.sid}), 200

    except TwilioRestException as e:
        app.logger.error(f'Erro do Twilio: {e}')
        return jsonify({'error': f'Erro do Twilio: {e}'}), 500
    
    except Exception as e:
        app.logger.error(f'Ocorreu um erro: {e}')
        return jsonify({'error': f'Ocorreu um erro: {e}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

