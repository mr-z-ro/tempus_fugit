#############################################
#
#  All endpoints below are from the template
#  and are not yet customized. Make sure to
#  copy them to the section above and rename
#  the methods and routes if you plan to use
#  them for Tempus Fugit.
#
#############################################

from flask import Blueprint
from flask import render_template, redirect
from flask import url_for
from flask_login import login_required

mod_wrap_bootstrap_templates = Blueprint('mod_wrap_bootstrap_templates', __name__)


# [START agile_board]
@mod_wrap_bootstrap_templates.route('/agile_board.html')
@login_required
def agile_board():
    return render_template('agile_board.html')
# [END agile_board]


# [START article]
@mod_wrap_bootstrap_templates.route('/article.html')
@login_required
def article():
    return render_template('article.html')
# [END boxed]


# [START badges_labels]
@mod_wrap_bootstrap_templates.route('/badges_labels.html')
@login_required
def badges_labels():
    return render_template('badges_labels.html')
# [END badges_labels]


# [START basic_gallery]
@mod_wrap_bootstrap_templates.route('/basic_gallery.html')
@login_required
def basic_gallery():
    return render_template('basic_gallery.html')
# [END basic_gallery]


# [START blog]
@mod_wrap_bootstrap_templates.route('/blog.html')
@login_required
def blog():
    return render_template('blog.html')
# [END basic_gallery]


# [START buttons]
@mod_wrap_bootstrap_templates.route('/buttons.html')
@login_required
def buttons():
    return render_template('buttons.html')
# [END buttons]


# [START c3]
@mod_wrap_bootstrap_templates.route('/c3.html')
@login_required
def c3():
    return render_template('c3.html')
# [END c3]

# [START c4]
@mod_wrap_bootstrap_templates.route('/c4.html')
@login_required
def c4():
    return render_template('c4.html')
# [END c4]

# [START calendar]
@mod_wrap_bootstrap_templates.route('/calendar.html')
@login_required
def calendar():
    return render_template('calendar.html')
# [END calendar]


# [START carousel]
@mod_wrap_bootstrap_templates.route('/carousel.html')
@login_required
def carousel():
    return render_template('carousel.html')
# [END carousel]


# [START chat_view]
@mod_wrap_bootstrap_templates.route('/chat_view.html')
@login_required
def chat_view():
    return render_template('chat_view.html')
# [END chat_view]


# [START clients]
@mod_wrap_bootstrap_templates.route('/clients.html')
@login_required
def clients():
    return render_template('clients.html')
# [END clients]


# [START clipboard]
@mod_wrap_bootstrap_templates.route('/clipboard.html')
@login_required
def clipboard():
    return render_template('clipboard.html')
# [END clipboard]


# [START code_editor]
@mod_wrap_bootstrap_templates.route('/code_editor.html')
@login_required
def code_editor():
    return render_template('code_editor.html')
# [END code_editor]


# [START contacts]
@mod_wrap_bootstrap_templates.route('/contacts.html')
@login_required
def contacts():
    return render_template('contacts.html')
# [END contacts]


# [START contacts_2]
@mod_wrap_bootstrap_templates.route('/contacts_2.html')
@login_required
def contacts_2():
    return render_template('contacts_2.html')
# [END contacts_2]


# [START css_animation]
@mod_wrap_bootstrap_templates.route('/css_animation.html')
@login_required
def css_animation():
    return render_template('css_animation.html')
# [END css_animation]


# [START dashboard_2]
@mod_wrap_bootstrap_templates.route('/dashboard_2.html')
@login_required
def dashboard_2():
    return render_template('dashboard_2.html')
# [END dashboard_2]


# [START dashboard_3]
@mod_wrap_bootstrap_templates.route('/dashboard_3.html')
@login_required
def dashboard_3():
    return render_template('dashboard_3.html')
# [END dashboard_3]


# [START dashboard_4]
@mod_wrap_bootstrap_templates.route('/dashboard_4.html')
@login_required
def dashboard_4():
    return render_template('dashboard_4.html')
# [END dashboard_4]


# [START dashboard_4_1]
@mod_wrap_bootstrap_templates.route('/dashboard_4_1.html')
@login_required
def dashboard_4_1():
    return render_template('dashboard_4_1.html')
# [END dashboard_4_1]


# [START dashboard_5]
@mod_wrap_bootstrap_templates.route('/dashboard_5.html')
@login_required
def dashboard_5():
    return render_template('dashboard_5.html')
# [END dashboard_5]


# [START diff]
@mod_wrap_bootstrap_templates.route('/diff.html')
@login_required
def diff():
    return render_template('diff.html')
# [END diff]


# [START draggable_panels]
@mod_wrap_bootstrap_templates.route('/draggable_panels.html')
@login_required
def draggable_panels():
    return render_template('draggable_panels.html')
# [END draggable_panels]


# [START ecommerce-cart]
@mod_wrap_bootstrap_templates.route('/ecommerce-cart.html')
@login_required
def ecommerce_cart():
    return render_template('ecommerce-cart.html')
# [END ecommerce-cart]


# [START ecommerce-orders]
@mod_wrap_bootstrap_templates.route('/ecommerce-orders.html')
@login_required
def ecommerce_orders():
    return render_template('ecommerce-orders.html')
# [END ecommerce-orders]


# [START ecommerce_payments]
@mod_wrap_bootstrap_templates.route('/ecommerce_payments.html')
@login_required
def ecommerce_payments():
    return render_template('ecommerce_payments.html')
# [END ecommerce_payments]


# [START ecommerce_product]
@mod_wrap_bootstrap_templates.route('/ecommerce_product.html')
@login_required
def ecommerce_product():
    return render_template('ecommerce_product.html')
# [END ecommerce_product]


# [START ecommerce_product_detail]
@mod_wrap_bootstrap_templates.route('/ecommerce_product_detail.html')
@login_required
def ecommerce_product_detail():
    return render_template('ecommerce_product_detail.html')
# [END ecommerce_product_detail]


# [START ecommerce_product_list]
@mod_wrap_bootstrap_templates.route('/ecommerce_product_list.html')
@login_required
def ecommerce_product_list():
    return render_template('ecommerce_product_list.html')
# [END ecommerce_product_list]


# [START ecommerce_product_grid]
@mod_wrap_bootstrap_templates.route('/ecommerce_product_grid.html')
@login_required
def ecommerce_product_grid():
    return render_template('ecommerce_product_grid.html')
# [END ecommerce_product_grid]


# [START email_template]
@mod_wrap_bootstrap_templates.route('/email_template.html')
@login_required
def email_template():
    return render_template('email_template.html')
# [END email_template]


# [START empty_page]
@mod_wrap_bootstrap_templates.route('/empty_page.html')
@login_required
def empty_page():
    return render_template('empty_page.html')
# [END empty_page]


# [START faq]
@mod_wrap_bootstrap_templates.route('/faq.html')
@login_required
def faq():
    return render_template('faq.html')
# [END faq]


# [START file_manager]
@mod_wrap_bootstrap_templates.route('/file_manager.html')
@login_required
def file_manager():
    return render_template('file_manager.html')
# [END file_manager]


# [START forgot_password]
@mod_wrap_bootstrap_templates.route('/forgot_password.html')
@mod_wrap_bootstrap_templates.route('/forgot')
def forgot_password():
    # redirect to the Netsuite OpenAir forgot password page
    return redirect('https://www.openair.com/index.pl?action=lost_info;')
    #return render_template('forgot_password.html')
# [END forgot_password]


# [START form_advanced]
@mod_wrap_bootstrap_templates.route('/form_advanced.html')
@login_required
def form_advanced():
    return render_template('form_advanced.html')
# [END form_advanced]


# [START form_basic]
@mod_wrap_bootstrap_templates.route('/form_basic.html')
@login_required
def form_basic():
    return render_template('form_basic.html')
# [END form_basic]


# [START form_editors]
@mod_wrap_bootstrap_templates.route('/form_editors.html')
@login_required
def form_editors():
    return render_template('form_editors.html')
# [END form_editors]


# [START form_file_upload]
@mod_wrap_bootstrap_templates.route('/form_file_upload.html')
@login_required
def form_file_upload():
    return render_template('form_file_upload.html')
# [END form_file_upload]


# [START form_markdown]
@mod_wrap_bootstrap_templates.route('/form_markdown.html')
@login_required
def form_markdown():
    return render_template('form_markdown.html')
# [END form_markdown]


# [START form_wizard]
@mod_wrap_bootstrap_templates.route('/form_wizard.html')
@login_required
def form_wizard():
    return render_template('form_wizard.html')
# [END form_wizard]


# [START forum_main]
@mod_wrap_bootstrap_templates.route('/forum_main.html')
@login_required
def forum_main():
    return render_template('forum_main.html')
# [END forum_main]


# [START forum_post]
@mod_wrap_bootstrap_templates.route('/forum_post.html')
@login_required
def forum_post():
    return render_template('forum_post.html')
# [END forum_post]


# [START full_height]
@mod_wrap_bootstrap_templates.route('/full_height.html')
@login_required
def full_height():
    return render_template('full_height.html')
# [END full_height]


# [START google_maps]
@mod_wrap_bootstrap_templates.route('/google_maps.html')
@login_required
def google_maps():
    return render_template('google_maps.html')
# [END google_maps]


# [START graph_chartist]
@mod_wrap_bootstrap_templates.route('/graph_chartist.html')
@login_required
def graph_chartist():
    return render_template('graph_chartist.html')
# [END graph_chartist]


# [START graph_chartjs]
@mod_wrap_bootstrap_templates.route('/graph_chartjs.html')
@login_required
def graph_chartjs():
    return render_template('graph_chartjs.html')
# [END graph_chartjs]


# [START graph_flot]
@mod_wrap_bootstrap_templates.route('/graph_flot.html')
@login_required
def graph_flot():
    return render_template('graph_flot.html')
# [END graph_flot]


# [START graph_morris]
@mod_wrap_bootstrap_templates.route('/graph_morris.html')
@login_required
def graph_morris():
    return render_template('graph_morris.html')
# [END graph_morris]


# [START graph_peity]
@mod_wrap_bootstrap_templates.route('/graph_peity.html')
@login_required
def graph_peity():
    return render_template('graph_peity.html')
# [END graph_peity]


# [START graph_rickshow]
@mod_wrap_bootstrap_templates.route('/graph_rickshow.html')
@login_required
def graph_rickshow():
    return render_template('graph_rickshow.html')
# [END graph_rickshow]


# [START graph_sparkline]
@mod_wrap_bootstrap_templates.route('/graph_sparkline.html')
@login_required
def graph_sparkline():
    return render_template('graph_sparkline.html')
# [END graph_sparkline]


# [START grid_options]
@mod_wrap_bootstrap_templates.route('/grid_options.html')
@login_required
def grid_options():
    return render_template('grid_options.html')
# [END grid_options]


# [START i18support]
@mod_wrap_bootstrap_templates.route('/i18support.html')
@login_required
def i18support():
    return render_template('i18support.html')
# [END i18support]


# [START icons]
@mod_wrap_bootstrap_templates.route('/icons.html')
@login_required
def icons():
    return render_template('icons.html')
# [END icons]


# [START idle_timer]
@mod_wrap_bootstrap_templates.route('/idle_timer.html')
@login_required
def idle_timer():
    return render_template('idle_timer.html')
# [END idle_timer]


# [START invoice]
@mod_wrap_bootstrap_templates.route('/invoice.html')
@login_required
def invoice():
    return render_template('invoice.html')
# [END invoice]


# [START invoice_print]
@mod_wrap_bootstrap_templates.route('/invoice_print.html')
@login_required
def invoice_print():
    return render_template('invoice_print.html')
# [END invoice_print]


# [START issue_tracker]
@mod_wrap_bootstrap_templates.route('/issue_tracker.html')
@login_required
def issue_tracker():
    return render_template('issue_tracker.html')
# [END issue_tracker]


# [START jq_grid]
@mod_wrap_bootstrap_templates.route('/jq_grid.html')
@login_required
def jq_grid():
    return render_template('jq_grid.html')
# [END jq_grid]


# [START landing]
@mod_wrap_bootstrap_templates.route('/landing.html')
@login_required
def landing():
    return render_template('landing.html')
# [END landing]


# [START layouts]
@mod_wrap_bootstrap_templates.route('/layouts.html')
@login_required
def layouts():
    return render_template('layouts.html')
# [END layouts]


# [START loading_buttons]
@mod_wrap_bootstrap_templates.route('/loading_buttons.html')
@login_required
def loading_buttons():
    return render_template('loading_buttons.html')
# [END loading_buttons]


# [START lockscreen]
@mod_wrap_bootstrap_templates.route('/lockscreen.html')
@login_required
def lockscreen():
    return render_template('lockscreen.html')
# [END lockscreen]

'''
# [START login]
@mod_wrap_bootstrap_templates.route('/login.html', methods=['GET','POST'])
def login_html():
    return render_template('login.html',form=form)
# [END login]
'''

# [START login_two_columns]
@mod_wrap_bootstrap_templates.route('/login_two_columns.html', methods=['GET'])
def login_two_columns():
    return render_template('login_two_columns.html')
# [END login]


# [START mail_compose]
@mod_wrap_bootstrap_templates.route('/mail_compose.html')
@login_required
def mail_compose():
    return render_template('mail_compose.html')
# [END mail_compose]


# [START mail_detail]
@mod_wrap_bootstrap_templates.route('/mail_detail.html')
@login_required
def mail_detail():
    return render_template('mail_detail.html')
# [END mail_detail]


# [START mailbox]
@mod_wrap_bootstrap_templates.route('/mailbox.html')
@login_required
def mailbox():
    return render_template('mailbox.html')
# [END mailbox]


# [START masonry]
@mod_wrap_bootstrap_templates.route('/masonry.html')
@login_required
def masonry():
    return render_template('masonry.html')
# [END masonry]


# [START md-skin]
@mod_wrap_bootstrap_templates.route('/md-skin.html')
@login_required
def md_skin():
    return render_template('md-skin.html')
# [END md-skin]


# [START metrics]
@mod_wrap_bootstrap_templates.route('/metrics.html')
@login_required
def metrics():
    return render_template('metrics.html')
# [END metrics]


# [START modal_window]
@mod_wrap_bootstrap_templates.route('/modal_window.html')
@login_required
def modal_window():
    return render_template('modal_window.html')
# [END modal_window]


# [START nestable_list]
@mod_wrap_bootstrap_templates.route('/nestable_list.html')
@login_required
def nestable_list():
    return render_template('nestable_list.html')
# [END nestable_list]


# [START notifications]
@mod_wrap_bootstrap_templates.route('/notifications.html')
@login_required
def notifications():
    return render_template('notifications.html')
# [END notifications]


# [START off_canvas_menu]
@mod_wrap_bootstrap_templates.route('/off_canvas_menu.html')
@login_required
def off_canvas_menu():
    return render_template('off_canvas_menu.html')
# [END off_canvas_menu]


# [START package]
@mod_wrap_bootstrap_templates.route('/package.html')
@login_required
def package():
    return render_template('package.html')
# [END package]


# [START pin_board]
@mod_wrap_bootstrap_templates.route('/pin_board.html')
@login_required
def pin_board():
    return render_template('pin_board.html')
# [END pin_board]


# [START profile]
@mod_wrap_bootstrap_templates.route('/profile.html')
@login_required
def profile():
    return render_template('profile.html')
# [END profile]


# [START profile_2]
@mod_wrap_bootstrap_templates.route('/profile_2.html')
@login_required
def profile_2():
    return render_template('profile_2.html')
# [END profile_2]


# [START register]
@mod_wrap_bootstrap_templates.route('/register.html')
def register():
    return render_template('register.html')
# [END register]


# [START resizeable_panels]
@mod_wrap_bootstrap_templates.route('/resizeable_panels.html')
@login_required
def resizeable_panels():
    return render_template('resizeable_panels.html')
# [END resizeable_panels]


# [START search_results]
@mod_wrap_bootstrap_templates.route('/search_results.html')
@login_required
def search_results():
    return render_template('search_results.html')
# [END search_results]


# [START skin-config]
@mod_wrap_bootstrap_templates.route('/skin-config.html')
@login_required
def skin_config():
    return render_template('skin-config.html')
# [END skin-config]


# [START slick_carousel]
@mod_wrap_bootstrap_templates.route('/slick_carousel.html')
@login_required
def slick_carousel():
    return render_template('slick_carousel.html')
# [END slick_carousel]


# [START social_feed]
@mod_wrap_bootstrap_templates.route('/social_feed.html')
@login_required
def social_feed():
    return render_template('social_feed.html')
# [END social_feed]


# [START spinners]
@mod_wrap_bootstrap_templates.route('/spinners.html')
@login_required
def spinners():
    return render_template('spinners.html')
# [END spinners]


# [START sweetalert]
@mod_wrap_bootstrap_templates.route('/sweetalert.html')
@login_required
def sweetalert():
    return render_template('sweetalert.html')
# [END sweetalert]


# [START table_basic]
@mod_wrap_bootstrap_templates.route('/table_basic.html')
@login_required
def table_basic():
    return render_template('table_basic.html')
# [END table_basic]


# [START table_data_tables]
@mod_wrap_bootstrap_templates.route('/table_data_tables.html')
@login_required
def table_data_tables():
    return render_template('table_data_tables.html')
# [END table_data_tables]


# [START table_foo_table]
@mod_wrap_bootstrap_templates.route('/table_foo_table.html')
@login_required
def table_foo_table():
    return render_template('table_foo_table.html')
# [END table_foo_table]


# [START tabs]
@mod_wrap_bootstrap_templates.route('/tabs.html')
@login_required
def tabs():
    return render_template('tabs.html')
# [END tabs]


# [START tabs_panels]
@mod_wrap_bootstrap_templates.route('/tabs_panels.html')
@login_required
def tabs_panels():
    return render_template('tabs_panels.html')
# [END tabs_panels]


# [START teams_board]
@mod_wrap_bootstrap_templates.route('/teams_board.html')
@login_required
def teams_board():
    return render_template('teams_board.html')
# [END teams_board]


# [START timeline]
@mod_wrap_bootstrap_templates.route('/timeline.html')
@login_required
def timeline():
    return render_template('timeline.html')
# [END timeline]


# [START timeline_2]
@mod_wrap_bootstrap_templates.route('/timeline_2.html')
@login_required
def timeline_2():
    return render_template('timeline_2.html')
# [END timeline_2]


# [START tinycon]
@mod_wrap_bootstrap_templates.route('/tinycon.html')
@login_required
def tinycon():
    return render_template('tinycon.html')
# [END tinycon]


# [START toastr_notifications]
@mod_wrap_bootstrap_templates.route('/toastr_notifications.html')
@login_required
def toastr_notifications():
    return render_template('toastr_notifications.html')
# [END toastr_notifications]


# [START tour]
@mod_wrap_bootstrap_templates.route('/tour.html')
@login_required
def tour():
    return render_template('tour.html')
# [END tour]


# [START tree_view]
@mod_wrap_bootstrap_templates.route('/tree_view.html')
@login_required
def tree_view():
    return render_template('tree_view.html')
# [END tree_view]


# [START truncate]
@mod_wrap_bootstrap_templates.route('/truncate.html')
@login_required
def truncate():
    return render_template('truncate.html')
# [END truncate]


# [START typography]
@mod_wrap_bootstrap_templates.route('/typography.html')
@login_required
def typography():
    return render_template('typography.html')
# [END typography]


# [START validation]
@mod_wrap_bootstrap_templates.route('/validation.html')
@login_required
def validation():
    return render_template('validation.html')
# [END validation]


# [START video]
@mod_wrap_bootstrap_templates.route('/video.html')
@login_required
def video():
    return render_template('video.html')
# [END video]


# [START vote_list]
@mod_wrap_bootstrap_templates.route('/vote_list.html')
@login_required
def vote_list():
    return render_template('vote_list.html')
# [END vote_list]


# [START widgets]
@mod_wrap_bootstrap_templates.route('/widgets.html')
@login_required
def widgets():
    return render_template('widgets.html')
# [END widgets]
