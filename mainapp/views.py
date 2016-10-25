from flask import render_template, flash, redirect, request, url_for
from mainapp import app
from .forms import NetForm
from switch_tool import cisco_switch_tool, run


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def _index():
    form = NetForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        do_stuff(form.ip_addr.data)
        return redirect('/index')
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
    flash(run.find_port(ip_addr))

