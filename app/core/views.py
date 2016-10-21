# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import redirect, flash, render_template, render_template_string, Blueprint
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted
from app import app, db
from app.core.models import UserProfileForm, DataAnalysisForm

from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
import os

from flask import current_app
from flask_mail import Message

from jobqueue import celery, send_results

core_blueprint = Blueprint('core', __name__, url_prefix='/')


# The Home page is accessible to anyone
@core_blueprint.route('')
def home_page():
    return render_template('core/home_page.html')


# The User page is accessible to authenticated users (users that have logged in)
@core_blueprint.route('user')
@login_required  # Limits access to authenticated users
def user_page():
    return render_template('core/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@core_blueprint.route('admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('core/admin_page.html')


@core_blueprint.route('user/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('core.home_page'))

    # Process GET or invalid POST
    return render_template('core/user_profile_page.html',
                           form=form)

@core_blueprint.route('data_analysis', methods=['GET', 'POST'])
@login_required
def data_analysis():

    # print(request.form)
    form = DataAnalysisForm(CombinedMultiDict((request.files, request.form)))

    # print(form)

    if (request.method == 'POST' and form.validate()):

        # print(request.form)
        # print(request.files)
        file = request.files['seqFile']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        mail_engine = current_app.extensions.get('mail', None)
        # print(mail_engine)

        # print(current_user)
        send_results.delay(filename, current_user.email)


        flash('processing job scheduled!')

        # Redirect to home page
        return redirect(url_for('core.data_analysis'))


    return render_template('core/data_analysis.html', form=form)

@core_blueprint.route('tutorial')
def tutorial():
    return render_template('core/tutorial.html')

@core_blueprint.route('team')
def team():
    return render_template('core/team.html')

@core_blueprint.route('contact')
def contact():
    return render_template('core/contact.html')


# Register blueprint
app.register_blueprint(core_blueprint)
