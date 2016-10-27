# Run a test server.
from app import app

app.run(host=app.config['HOSTNAME'], port=app.config['PORT'], debug=True)
