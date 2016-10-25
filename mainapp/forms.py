from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SelectField, RadioField
from wtforms import validators
import re

class NetForm(Form):

    ip_addr = StringField('ip_addr', validators=[validators.DataRequired(), validators.IPAddress(message='Please enter a valid IP')])



