from app import app
from celery import Celery
from flask.ext.mail import Message
from flask import current_app

# config
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# set up celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# put the processing task here
# GIANT HACK, FIX LATER
@celery.task
def send_results(filename, email_addr):
    msg = Message('testing email', recipients=[email_addr])
    msg.body = 'testing this funct'
    with app.app_context():
        current_app.mail.send(msg)
    print(filename)
    print(email_addr)