from flask import Blueprint, render_template, abort, redirect, request
from jinja2 import TemplateNotFound


create = Blueprint('create', __name__,
                   template_folder='templates')


@create.route('/create/publication', methods=['GET', 'POST'])
def create_publication():

    if request.method == 'POST':
        # do something
        redirect('index')
    return render_template('create/form.html',
                           formname='Publications Manifest Form',
                           formfile='publicationform.js')

