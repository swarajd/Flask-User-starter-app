from app import app
from celery import Celery
from flask.ext.mail import Message
from flask import current_app
from flask_mail import Mail
import os
import csv
import random

# config
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

env_settings_file = os.environ.get('ENV_SETTINGS_FILE', 'env_settings_example.py')
app.config.from_pyfile(env_settings_file)

mail = Mail(app)

# set up celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# put the processor here
def parseFile(fl):
    ret_str = ''
    trans_data = csv.reader(fl)

    pred_dict = {}
    dataset_name = trans_data.__next__()
    dataset_num = len(dataset_name)-1
    for items in dataset_name[1:dataset_num]:
        pred_dict[items] = random.uniform(-5,5)
        
    # print(pred_dict)

    for k, v in pred_dict.items():
    #   print ("%s,"% k,)
    #   values = map(str, v)
        ret_str += ', '.join([k, str('%.2f' % v)]) + '\n'
    return ret_str

# put the processing task here
@celery.task
def send_results(filename, email_addr):
    file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    with app.app_context():
        msg = Message('testing email', recipients=[email_addr])
        msg.body = 'the parse result of: ' + filename + '\n'

        parse_result = parseFile(file)
        msg.attach("result.txt", "text/plain", parse_result)

        mail.send(msg)
    print(filename)
    print(email_addr)
