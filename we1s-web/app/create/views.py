from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from models import *

create = Blueprint('create', __name__,
                   template_folder='templates')


@create.route('/create/publication')
def create_publication(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)
