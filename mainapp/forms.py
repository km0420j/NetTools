from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SelectField, RadioField
from wtforms import validators
import re

class NetForm(Form):

    ip_addr = StringField('ip_addr', validators=[validators.Optional(), validators.IPAddress(message='Please enter a valid IP')])

    computername = StringField('computername', validators=[validators.Optional()])
    username = StringField('username', validators=[validators.Optional()])

