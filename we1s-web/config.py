# Statement for enabling the development environment
DEBUG = True

# Define the database we are working with
MONGODB_HOST = "ds023435.mlab.com"
MONGODB_NAME = "we1s"
MONGODB_URI = "mongodb://dbuser:we1s@ds023435.mlab.com:23435/we1s"
MONGODB_PORT = 23435


# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
