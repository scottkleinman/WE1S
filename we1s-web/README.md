## Setup

### Requirements
1. Python 2.7 and up, but not Python 3.
2. The corresponding `pip`. To install `pip`, follow the instructions [here](https://pip.pypa.io/en/stable/installing/).


### Dependencies
Dependencies required by this application are listed in `requirements.txt`. To install dependencies, run 

```bash
pip install -r requirements.txt
```


### Configurations
1. Create an instance configuration file `instance/config.py` based on the template file at `instance/config.py.temp`. 
Configurations in this file should be instance-dependent, and thus the file is ignored in Git. 
2. `config.py` is another configuration file for rest of the configurations. Adjust them if needed.


## Run
1. Start a MongoDB instance. The instance can run on either localhost or any other service provider, e.g. [mLab](https://mlab.com).
2. Make sure `instance/config.py` is properly configured according to the MongoDB setup.
3. The application can be started by running:

    ```bash
    python run.py
    ```

4. If everything works properly, you should be able to access the application. The default address is (http://0.0.0.0:8081), 
if you access it from the same machine.


## Development


### File Structure


#### Tree
```
├── README.md
├── app
│   ├── __init__.py
│   ├── mod_create
│   ├── mod_display
│   ├── mod_upload
│   ├── static
│   └── templates
├── config.py
├── instance
│   ├── config.py
│   └── config.py.temp
├── obselete
│   └── ...
├── requirements.txt
├── run.py
└── uploads

```


#### Description

File | Description
--- | ---
run.py | This is the file that is invoked to start up a development server. It gets a copy of the app from the app package and runs it. This won’t be used in production, but it will see a lot of mileage in development.
requirements.txt | This file lists all of the Python packages that the app depends on. You may have separate files for production and development dependencies.
config.py | This file contains most of the configuration variables that the app needs.
/instance/config.py | This file contains configuration variables that shouldn’t be in version control. This includes things like API keys and database URIs containing passwords. This also contains variables that are specific to this particular instance of the application. For example, you might have DEBUG = False in config.py, but set DEBUG = True in instance/config.py on the local machine for development. Since this file will be read in after config.py, it will override it and set DEBUG = True.
/instance/config.py.temp | A template for `/instance/config.py`.
/app/ | This is the package that contains the WE1S application.
/app/__init__.py | This file initializes the application and brings together all of the various components.
/app/static/ | This directory contains the public CSS, JavaScript, images and other files that you want to make public via the app. It is accessible from `app.com/static/` by default.
/app/templates/ | This is where you’ll put the Jinja2 templates for the app.
/app/mod_create/ | This is a package for manifest creation related features.
/app/mod_display/ | This is a package for manifest display related features.
/app/mod_upload/ | This is a package for file uploads related features.
/uploads | This is where the app stores user uploaded files.


### Templates
This application uses Jinja2 as its template engine. For more information, please refer to Jinja2's official [documentation](http://jinja.pocoo.org/docs/dev/).

#### Basics
`templates/layout.html` is the layout of each page of the app. When a new page is created, it should extend the layout template by adding `{% extends "layout.html" %}` at the beginning of the HTML. 

Page contents can be added to `{% block content %}`. Extra scripts can be added to `{% block scripts %}` For example:


```html
{% extends "layout.html" %}

{% block content %}
    <div class="jumbotron">
        <h2>WhatEvery1Says Demo</h2>
    </div>
{% endblock %}

{% block scripts %}
    <script type="text/javascript"
            src={{ url_for('static', filename='lib/moment-with-locales.min.js') }}></script>
{% endblock %} 
```


#### Navigation Bar
Navigation bar is implemented in `templates/navbar.html`, and it's included by `layout.html`. 


#### Forms
All forms are based on `templates/create/main.html`, which extends `layout.html'. 