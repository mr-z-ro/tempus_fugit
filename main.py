# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

# [START imports]
from flask import Flask, render_template, request
# [END imports]

app = Flask(__name__)


# [START 404]
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
# [END 404]


# [START 500]
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
# [END 500]


# [START login]
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')
# [END login]


# [START submitted]
@app.route('/login', methods=['POST'])
def login_submission():
    company = request.form['company']
    username = request.form['username']
    password = request.form['password']

    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        company=company,
        username=username,
        password=password)
    # [END render_template]


# [START home]
@app.route('/')
def home():
    return render_template('home.html')
# [END home]


#############################################
#
#  All endpoints below are from the template
#  and are not yet customized. Make sure to
#  copy them to the section above and rename
#  the methods and routes if you plan to use
#  them for Tempus Fugit.
#
#############################################

# [START blank]
@app.route('/blank.html')
def blank():
    return render_template('blank.html')
# [END blank]


# [START boxed]
@app.route('/boxed.html')
def boxed():
    return render_template('boxed.html')
# [END boxed]


# [START buttons]
@app.route('/buttons.html')
def buttons():
    return render_template('buttons.html')
# [END buttons]


# [START calendar]
@app.route('/calendar.html')
def calendar():
    return render_template('calendar.html')
# [END calendar]


# [START chartjs]
@app.route('/chartjs.html')
def chartjs():
    return render_template('chartjs.html')
# [END chartjs]


# [START email]
@app.route('/email.html')
def email():
    return render_template('email.html')
# [END email]


# [START email-compose]
@app.route('/email-compose.html')
def email_compose():
    return render_template('email-compose.html')
# [END email-compose]


# [START email-inbox]
@app.route('/email-inbox.html')
def email_inbox():
    return render_template('email-inbox.html')
# [END email-inbox]


# [START fixed]
@app.route('/fixed.html')
def fixed():
    return render_template('fixed.html')
# [END fixed]


# [START form]
@app.route('/form.html')
def form():
    return render_template('form.html')
# [END form]


# [START forms-custom]
@app.route('/forms-custom.html')
def forms_custom():
    return render_template('forms-custom.html')
# [END forms-custom]


# [START forms-editor]
@app.route('/forms-editor.html')
def forms_editor():
    return render_template('forms-editor.html')
# [END forms-editor]


# [START forms-simple]
@app.route('/forms-simple.html')
def forms_simple():
    return render_template('forms-simple.html')
# [END forms-simple]


# [START icons]
@app.route('/icons.html')
def icons():
    return render_template('icons.html')
# [END icons]


# [START index]
@app.route('/index.html')
def index():
    return render_template('index.html')
# [END index]


# [START inline-charts]
@app.route('/inline-charts.html')
def inline_charts():
    return render_template('inline-charts.html')
# [END inline-charts]


# [START invoice]
@app.route('/invoice.html')
def invoice():
    return render_template('invoice.html')
# [END invoice]


# [START login]
@app.route('/login.html', methods=['GET'])
def login_html():
    return render_template('login.html')
# [END login]


# [START modals]
@app.route('/modals.html')
def modals():
    return render_template('modals.html')
# [END modals]


# [START morris]
@app.route('/morris.html')
def morris():
    return render_template('morris.html')
# [END morris]


# [START profile]
@app.route('/profile.html')
def profile():
    return render_template('profile.html')
# [END profile]


# [START signup]
@app.route('/signup.html')
def signup():
    return render_template('signup.html')
# [END signup]


# [START slider]
@app.route('/slider.html')
def slider():
    return render_template('slider.html')
# [END slider]


# [START submitted_form]
@app.route('/submitted_form.html')
def submitted_form():
    return render_template('submitted_form.html')
# [END submitted_form]


# [START tables-data]
@app.route('/tables-data.html')
def tables_data():
    return render_template('tables-data.html')
# [END tables-data]


# [START tables-simple]
@app.route('/tables-simple.html')
def tables_simple():
    return render_template('tables-simple.html')
# [END tables-simple]


# [START timeline]
@app.route('/timeline.html')
def timeline():
    return render_template('timeline.html')
# [END timeline]


# [START top-nav]
@app.route('/top-nav.html')
def top_nav():
    return render_template('top-nav.html')
# [END top-nav]


# [START ui-basic]
@app.route('/ui-basic.html')
def ui_basic():
    return render_template('ui-basic.html')
# [END ui-basic]


# [START widgets]
@app.route('/widgets.html')
def widgets():
    return render_template('widgets.html')
# [END widgets]
