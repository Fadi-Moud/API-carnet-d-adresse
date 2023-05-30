import os
from flask import Flask
from modules.contacts.contact import contact_request

app = Flask(__name__)

app.register_blueprint(contact_request, url_prefix='/contacts')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
