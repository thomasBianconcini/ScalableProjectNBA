from flask import Flask, render_template,send_file,render_template_string
from flask_restx import Api
from api.routes import api
from flask_cors import CORS
# Crea l'applicazione Flask
app = Flask(__name__)
CORS(app)
api_instance = Api(app)

api_instance.add_namespace(api)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, ssl_context=('sec/backend-cert.pem', 'sec/backend-key.pem'), debug=True)
