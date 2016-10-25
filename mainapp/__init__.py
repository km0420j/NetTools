from flask import Flask
#from switch_tool import views

app = Flask(__name__)
app.config.from_object('config')

app.secret_key = '\x855Ou\xb4\xde\xa0\x92z\xfd\x1d\x1a\x9f\xeez<\x13\xa97\x93\x91\x95\x10\xc0'

from mainapp import views

