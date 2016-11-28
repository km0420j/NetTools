import socket
from flask import render_template, flash, redirect, request, url_for
from mainapp import app
from .forms import NetForm
from switch_tool import cisco_switch_tool, switch_tool_app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def _index():
    form = NetForm(request.form)
    message = ''
    if request.method == 'POST' and form.validate_on_submit():
        if form.ip_addr.data:
            message = do_stuff(form.ip_addr.data)
        elif form.computername.data:
            ip_addr = dns_query(form.computername.data)
            if ip_addr != None:
                message = do_stuff(ip_addr)
            else:
                message = 'Cannot find computername'
        elif form.username.data:
            message = ldap_search.computer_by_user(form.username.data)
        flash(message, 'info')
        #return render_template('modal.html', message=message)
    else:
        flash_errors(form)
    return render_template('index.html', form=form)

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

def do_stuff(ip_addr):
    try:
        #flash(switch_tool_app.find_port(ip_addr))
        return switch_tool_app.find_port(ip_addr)
    except:
        #flash('ERROR: could not connect to switch')
        return 'ERROR: could not connect to switch'
 
def dns_query(name):
    try:
        return socket.gethostbyname(name)
    except:
        return None
