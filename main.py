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

# [START agile_board]
@app.route('/agile_board.html')
def agile_board():
    return render_template('agile_board.html')
# [END agile_board]


# [START article]
@app.route('/article.html')
def article():
    return render_template('article.html')
# [END boxed]


# [START badges_labels]
@app.route('/badges_labels.html')
def badges_labels():
    return render_template('badges_labels.html')
# [END badges_labels]


# [START basic_gallery]
@app.route('/basic_gallery.html')
def basic_gallery():
    return render_template('basic_gallery.html')
# [END basic_gallery]


# [START blog]
@app.route('/blog.html')
def blog():
    return render_template('blog.html')
# [END basic_gallery]


# [START buttons]
@app.route('/buttons.html')
def buttons():
    return render_template('buttons.html')
# [END buttons]


# [START c3]
@app.route('/c3.html')
def c3():
    return render_template('c3.html')
# [END c3]


# [START calendar]
@app.route('/calendar.html')
def calendar():
    return render_template('calendar.html')
# [END calendar]


# [START carousel]
@app.route('/carousel.html')
def carousel():
    return render_template('carousel.html')
# [END carousel]


# [START chat_view]
@app.route('/chat_view.html')
def chat_view():
    return render_template('chat_view.html')
# [END chat_view]


# [START clients]
@app.route('/clients.html')
def clients():
    return render_template('clients.html')
# [END clients]


# [START clipboard]
@app.route('/clipboard.html')
def clipboard():
    return render_template('clipboard.html')
# [END clipboard]


# [START code_editor]
@app.route('/code_editor.html')
def code_editor():
    return render_template('code_editor.html')
# [END code_editor]


# [START contacts]
@app.route('/contacts.html')
def contacts():
    return render_template('contacts.html')
# [END contacts]


# [START contacts_2]
@app.route('/contacts_2.html')
def contacts_2():
    return render_template('contacts_2.html')
# [END contacts_2]


# [START css_animation]
@app.route('/css_animation.html')
def css_animation():
    return render_template('css_animation.html')
# [END css_animation]


# [START dashboard_2]
@app.route('/dashboard_2.html')
def dashboard_2():
    return render_template('dashboard_2.html')
# [END dashboard_2]


# [START dashboard_3]
@app.route('/dashboard_3.html')
def dashboard_3():
    return render_template('dashboard_3.html')
# [END dashboard_3]


# [START dashboard_4]
@app.route('/dashboard_4.html')
def dashboard_4():
    return render_template('dashboard_4.html')
# [END dashboard_4]


# [START dashboard_4_1]
@app.route('/dashboard_4_1.html')
def dashboard_4_1():
    return render_template('dashboard_4_1.html')
# [END dashboard_4_1]


# [START dashboard_5]
@app.route('/dashboard_5.html')
def dashboard_5():
    return render_template('dashboard_5.html')
# [END dashboard_5]


# [START diff]
@app.route('/diff.html')
def diff():
    return render_template('diff.html')
# [END diff]


# [START draggable_panels]
@app.route('/draggable_panels.html')
def draggable_panels():
    return render_template('draggable_panels.html')
# [END draggable_panels]


# [START ecommerce-cart]
@app.route('/ecommerce-cart.html')
def ecommerce_cart():
    return render_template('ecommerce-cart.html')
# [END ecommerce-cart]


# [START ecommerce-orders]
@app.route('/ecommerce-orders.html')
def ecommerce_orders():
    return render_template('ecommerce-orders.html')
# [END ecommerce-orders]


# [START ecommerce_payments]
@app.route('/ecommerce_payments.html')
def ecommerce_payments():
    return render_template('ecommerce_payments.html')
# [END ecommerce_payments]


# [START ecommerce_product]
@app.route('/ecommerce_product.html')
def ecommerce_product():
    return render_template('ecommerce_product.html')
# [END ecommerce_product]


# [START ecommerce_product_detail]
@app.route('/ecommerce_product_detail.html')
def ecommerce_product_detail():
    return render_template('ecommerce_product_detail.html')
# [END ecommerce_product_detail]


# [START ecommerce_product_list]
@app.route('/ecommerce_product_list.html')
def ecommerce_product_list():
    return render_template('ecommerce_product_list.html')
# [END ecommerce_product_list]


# [START ecommerce_product_grid]
@app.route('/ecommerce_product_grid.html')
def ecommerce_product_grid():
    return render_template('ecommerce_product_grid.html')
# [END ecommerce_product_grid]


# [START email_template]
@app.route('/email_template.html')
def email_template():
    return render_template('email_template.html')
# [END email_template]


# [START empty_page]
@app.route('/empty_page.html')
def empty_page():
    return render_template('empty_page.html')
# [END empty_page]


# [START faq]
@app.route('/faq.html')
def faq():
    return render_template('faq.html')
# [END faq]


# [START file_manager]
@app.route('/file_manager.html')
def file_manager():
    return render_template('file_manager.html')
# [END file_manager]


# [START forgot_password]
@app.route('/forgot_password.html')
def forgot_password():
    return render_template('forgot_password.html')
# [END forgot_password]


# [START form_advanced]
@app.route('/form_advanced.html')
def form_advanced():
    return render_template('form_advanced.html')
# [END form_advanced]


# [START form_basic]
@app.route('/form_basic.html')
def form_basic():
    return render_template('form_basic.html')
# [END form_basic]


# [START form_editors]
@app.route('/form_editors.html')
def form_editors():
    return render_template('form_editors.html')
# [END form_editors]


# [START form_file_upload]
@app.route('/form_file_upload.html')
def form_file_upload():
    return render_template('form_file_upload.html')
# [END form_file_upload]


# [START form_markdown]
@app.route('/form_markdown.html')
def form_markdown():
    return render_template('form_markdown.html')
# [END form_markdown]


# [START form_wizard]
@app.route('/form_wizard.html')
def form_wizard():
    return render_template('form_wizard.html')
# [END form_wizard]


# [START forum_main]
@app.route('/forum_main.html')
def forum_main():
    return render_template('forum_main.html')
# [END forum_main]


# [START forum_post]
@app.route('/forum_post.html')
def forum_post():
    return render_template('forum_post.html')
# [END forum_post]


# [START full_height]
@app.route('/full_height.html')
def full_height():
    return render_template('full_height.html')
# [END full_height]


# [START google_maps]
@app.route('/google_maps.html')
def google_maps():
    return render_template('google_maps.html')
# [END google_maps]


# [START graph_chartist]
@app.route('/graph_chartist.html')
def graph_chartist():
    return render_template('graph_chartist.html')
# [END graph_chartist]


# [START graph_chartjs]
@app.route('/graph_chartjs.html')
def graph_chartjs():
    return render_template('graph_chartjs.html')
# [END graph_chartjs]


# [START graph_flot]
@app.route('/graph_flot.html')
def graph_flot():
    return render_template('graph_flot.html')
# [END graph_flot]


# [START graph_morris]
@app.route('/graph_morris.html')
def graph_morris():
    return render_template('graph_morris.html')
# [END graph_morris]


# [START graph_peity]
@app.route('/graph_peity.html')
def graph_peity():
    return render_template('graph_peity.html')
# [END graph_peity]


# [START graph_rickshow]
@app.route('/graph_rickshow.html')
def graph_rickshow():
    return render_template('graph_rickshow.html')
# [END graph_rickshow]


# [START graph_sparkline]
@app.route('/graph_sparkline.html')
def graph_sparkline():
    return render_template('graph_sparkline.html')
# [END graph_sparkline]


# [START grid_options]
@app.route('/grid_options.html')
def grid_options():
    return render_template('grid_options.html')
# [END grid_options]


# [START i18support]
@app.route('/i18support.html')
def i18support():
    return render_template('i18support.html')
# [END i18support]


# [START icons]
@app.route('/icons.html')
def icons():
    return render_template('icons.html')
# [END icons]


# [START idle_timer]
@app.route('/idle_timer.html')
def idle_timer():
    return render_template('idle_timer.html')
# [END idle_timer]


# [START index]
@app.route('/index.html')
def index():
    return render_template('index.html')
# [END index]


# [START invoice]
@app.route('/invoice.html')
def invoice():
    return render_template('invoice.html')
# [END invoice]


# [START invoice_print]
@app.route('/invoice_print.html')
def invoice_print():
    return render_template('invoice_print.html')
# [END invoice_print]


# [START issue_tracker]
@app.route('/issue_tracker.html')
def issue_tracker():
    return render_template('issue_tracker.html')
# [END issue_tracker]


# [START jq_grid]
@app.route('/jq_grid.html')
def jq_grid():
    return render_template('jq_grid.html')
# [END jq_grid]


# [START landing]
@app.route('/landing.html')
def landing():
    return render_template('landing.html')
# [END landing]


# [START layouts]
@app.route('/layouts.html')
def layouts():
    return render_template('layouts.html')
# [END layouts]


# [START loading_buttons]
@app.route('/loading_buttons.html')
def loading_buttons():
    return render_template('loading_buttons.html')
# [END loading_buttons]


# [START lockscreen]
@app.route('/lockscreen.html')
def lockscreen():
    return render_template('lockscreen.html')
# [END lockscreen]


# [START login]
@app.route('/login.html', methods=['GET'])
def login_html():
    return render_template('login.html')
# [END login]


# [START login_two_columns]
@app.route('/login_two_columns.html', methods=['GET'])
def login_two_columns():
    return render_template('login_two_columns.html')
# [END login]


# [START mail_compose]
@app.route('/mail_compose.html')
def mail_compose():
    return render_template('mail_compose.html')
# [END mail_compose]


# [START mail_detail]
@app.route('/mail_detail.html')
def mail_detail():
    return render_template('mail_detail.html')
# [END mail_detail]


# [START mailbox]
@app.route('/mailbox.html')
def mailbox():
    return render_template('mailbox.html')
# [END mailbox]


# [START masonry]
@app.route('/masonry.html')
def masonry():
    return render_template('masonry.html')
# [END masonry]


# [START md-skin]
@app.route('/md-skin.html')
def md_skin():
    return render_template('md-skin.html')
# [END md-skin]


# [START metrics]
@app.route('/metrics.html')
def metrics():
    return render_template('metrics.html')
# [END metrics]


# [START modal_window]
@app.route('/modal_window.html')
def modal_window():
    return render_template('modal_window.html')
# [END modal_window]


# [START nestable_list]
@app.route('/nestable_list.html')
def nestable_list():
    return render_template('nestable_list.html')
# [END nestable_list]


# [START notifications]
@app.route('/notifications.html')
def notifications():
    return render_template('notifications.html')
# [END notifications]


# [START off_canvas_menu]
@app.route('/off_canvas_menu.html')
def off_canvas_menu():
    return render_template('off_canvas_menu.html')
# [END off_canvas_menu]


# [START package]
@app.route('/package.html')
def package():
    return render_template('package.html')
# [END package]


# [START pin_board]
@app.route('/pin_board.html')
def pin_board():
    return render_template('pin_board.html')
# [END pin_board]


# [START profile]
@app.route('/profile.html')
def profile():
    return render_template('profile.html')
# [END profile]


# [START profile_2]
@app.route('/profile_2.html')
def profile_2():
    return render_template('profile_2.html')
# [END profile_2]


# [START project_detail]
@app.route('/project_detail.html')
def project_detail():
    return render_template('project_detail.html')
# [END project_detail]


# [START projects]
@app.route('/projects.html')
def projects():
    return render_template('projects.html')
# [END projects]


# [START register]
@app.route('/register.html')
def register():
    return render_template('register.html')
# [END register]


# [START resizeable_panels]
@app.route('/resizeable_panels.html')
def resizeable_panels():
    return render_template('resizeable_panels.html')
# [END resizeable_panels]


# [START search_results]
@app.route('/search_results.html')
def search_results():
    return render_template('search_results.html')
# [END search_results]


# [START skin-config]
@app.route('/skin-config.html')
def skin_config():
    return render_template('skin-config.html')
# [END skin-config]


# [START slick_carousel]
@app.route('/slick_carousel.html')
def slick_carousel():
    return render_template('slick_carousel.html')
# [END slick_carousel]


# [START social_feed]
@app.route('/social_feed.html')
def social_feed():
    return render_template('social_feed.html')
# [END social_feed]


# [START spinners]
@app.route('/spinners.html')
def spinners():
    return render_template('spinners.html')
# [END spinners]


# [START sweetalert]
@app.route('/sweetalert.html')
def sweetalert():
    return render_template('sweetalert.html')
# [END sweetalert]


# [START table_basic]
@app.route('/table_basic.html')
def table_basic():
    return render_template('table_basic.html')
# [END table_basic]


# [START table_data_tables]
@app.route('/table_data_tables.html')
def table_data_tables():
    return render_template('table_data_tables.html')
# [END table_data_tables]


# [START table_foo_table]
@app.route('/table_foo_table.html')
def table_foo_table():
    return render_template('table_foo_table.html')
# [END table_foo_table]


# [START tabs]
@app.route('/tabs.html')
def tabs():
    return render_template('tabs.html')
# [END tabs]


# [START tabs_panels]
@app.route('/tabs_panels.html')
def tabs_panels():
    return render_template('tabs_panels.html')
# [END tabs_panels]


# [START teams_board]
@app.route('/teams_board.html')
def teams_board():
    return render_template('teams_board.html')
# [END teams_board]


# [START timeline]
@app.route('/timeline.html')
def timeline():
    return render_template('timeline.html')
# [END timeline]


# [START timeline_2]
@app.route('/timeline_2.html')
def timeline_2():
    return render_template('timeline_2.html')
# [END timeline_2]


# [START tinycon]
@app.route('/tinycon.html')
def tinycon():
    return render_template('tinycon.html')
# [END tinycon]


# [START toastr_notifications]
@app.route('/toastr_notifications.html')
def toastr_notifications():
    return render_template('toastr_notifications.html')
# [END toastr_notifications]


# [START tour]
@app.route('/tour.html')
def tour():
    return render_template('tour.html')
# [END tour]


# [START tree_view]
@app.route('/tree_view.html')
def tree_view():
    return render_template('tree_view.html')
# [END tree_view]


# [START truncate]
@app.route('/truncate.html')
def truncate():
    return render_template('truncate.html')
# [END truncate]


# [START typography]
@app.route('/typography.html')
def typography():
    return render_template('typography.html')
# [END typography]


# [START validation]
@app.route('/validation.html')
def validation():
    return render_template('validation.html')
# [END validation]


# [START video]
@app.route('/video.html')
def video():
    return render_template('video.html')
# [END video]


# [START vote_list]
@app.route('/vote_list.html')
def vote_list():
    return render_template('vote_list.html')
# [END vote_list]


# [START widgets]
@app.route('/widgets.html')
def widgets():
    return render_template('widgets.html')
# [END widgets]
