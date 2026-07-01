from flask import Flask

app = Flask(__name__)

app.secret_key = "Skiers"

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'skierschoice.ai@gmail.com'
MAIL_PASSWORD = 'keqb tqye bedx mpva'
MAIL_DEFAULT_SENDER = 'skierschoice.ai@gmail.com'