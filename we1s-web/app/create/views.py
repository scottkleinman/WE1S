from flask import Blueprint, render_template, redirect, request


create = Blueprint('create', __name__,
                   template_folder='templates')


@create.route('/create/publication', methods=['GET', 'POST'])
def create_publication():
    if request.method == 'POST':
        print request.get_json()
        redirect('index')

    return render_template('create/form.html',
                           formname='Publications Manifest Form',
                           formfile='publicationform.js')
