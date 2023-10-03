from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
from translate import Translator
from rich import print
from collections import OrderedDict
from dotenv import load_dotenv
import joblib
import os

load_dotenv()

translator= Translator(from_lang='pt', to_lang='en')

# Defina a ordem desejada das chaves
sort_key = ["Tamanho", "Ano", "Garagem"]

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.getenv('USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('PASSWORD')

basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return 'Minha primeira API'

@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    translation = translator.translate(frase)
    print(translation)
    tb = TextBlob(translation)
    polarity = tb.sentiment.polarity
    return f'Polaridade: {polarity:.0%}'

@app.route('/cotacao/', methods=['POST'])
def cotacao():
    payload = request.get_json()
    sorted_key = OrderedDict((key, payload[key]) for key in sort_key)
    data = list(sorted_key.values())
    modelo = joblib.load(os.path.join(os.getcwd(),'models/modelo-houses-price.pkl'))
    preco = float(modelo.predict([data]))
    return jsonify(preco=f"R${preco:,.2f}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)