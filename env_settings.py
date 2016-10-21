import os

# *****************************
# Environment specific settings
# *****************************

# The settings below can (and should) be over-ruled by OS environment variable settings

# Flask settings                     # Generated with: import os; os.urandom(24)
SECRET_KEY = '\xb9\x8d\xb5\xc2\xc4Q\xe7\x8ej\xe0\x05\xf3\xa3kp\x99l\xe7\xf2i\x00\xb1-\xcd'
# PLEASE USE A DIFFERENT KEY FOR PRODUCTION ENVIRONMENTS!

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:PostgresSw4r4j@localhost/seq2flux'

# Flask-Mail setting
MAIL_USERNAME = 'seq2flux@gmail.com'
MAIL_PASSWORD = 'seq2fluxgui'
MAIL_DEFAULT_SENDER = '"Seq2Flux" <seq2flux@gmail.com>'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False

ADMINS = [
    '"Admin One" <admin1@gmail.com>',
    ]

UPLOAD_FOLDER = 'app/uploads/'
ALLOWED_EXTENSIONS = set(['csv', 'fasta'])

