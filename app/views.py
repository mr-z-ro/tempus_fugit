# app/views.py
"""
views.py - all our app routes are defined here
"""
from flask import render_template
from flask_login import login_required, login_user

from . import app, db
from .forms import LoginForm
from .models import User

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = EmailPasswordForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

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
@app.route('/login.html', methods=['GET','POST'])
def login():
	form = loginForm(csrf_enabled=True) # instantiate the LoginForm
	if form.validate_on_submit():
		# Login and validate the user
		# user should be an instance of your 'User' class
		# save the username to a session
		session['username'] = form.username.data.split('@')[0] # Generate ID from email address
		
		user = User(
            username = form.username.data,
            password = form.password.data
        )
		
		netsuite_key = app.config['NETSUITE_API_KEY'] # Retrieve key from config file
		
		if user.is_user_openair_allowed(form.password.data,netsuite_key):
			login_user(user)
			return redirect(url_for('index'))
			flash('Logged in successfully.')
			next = request.args.get('next')
			# next_is_valid should check if the user has validate
			# permission to access the 'next' url
			#if not next_is_valid(next):
			#	return abort(400)
			return redirect(next or url_for('index'))
	return render_template('login.html',form=form)


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
@login_required
def home():
    return render_template('home.html')
# [END home]

# [START Trials]
@app.route('/trial/')
@login_required
def trial():
	# To access my USERNAME >> app.config["USERNAME"]
	return "BCRYPT_LEVEL: {}".format(app.config["BCRYPT_LEVEL"])

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
@login_required
def agile_board():
    return render_template('agile_board.html')
# [END agile_board]


# [START article]
@app.route('/article.html')
@login_required
def article():
    return render_template('article.html')
# [END boxed]


# [START badges_labels]
@app.route('/badges_labels.html')
@login_required
def badges_labels():
    return render_template('badges_labels.html')
# [END badges_labels]


# [START basic_gallery]
@app.route('/basic_gallery.html')
@login_required
def basic_gallery():
    return render_template('basic_gallery.html')
# [END basic_gallery]


# [START blog]
@app.route('/blog.html')
@login_required
def blog():
    return render_template('blog.html')
# [END basic_gallery]


# [START buttons]
@app.route('/buttons.html')
@login_required
def buttons():
    return render_template('buttons.html')
# [END buttons]


# [START c3]
@app.route('/c3.html')
@login_required
def c3():
    return render_template('c3.html')
# [END c3]


# [START calendar]
@app.route('/calendar.html')
@login_required
def calendar():
    return render_template('calendar.html')
# [END calendar]


# [START carousel]
@app.route('/carousel.html')
@login_required
def carousel():
    return render_template('carousel.html')
# [END carousel]


# [START chat_view]
@app.route('/chat_view.html')
@login_required
def chat_view():
    return render_template('chat_view.html')
# [END chat_view]


# [START clients]
@app.route('/clients.html')
@login_required
def clients():
    return render_template('clients.html')
# [END clients]


# [START clipboard]
@app.route('/clipboard.html')
@login_required
def clipboard():
    return render_template('clipboard.html')
# [END clipboard]


# [START code_editor]
@app.route('/code_editor.html')
@login_required
def code_editor():
    return render_template('code_editor.html')
# [END code_editor]


# [START contacts]
@app.route('/contacts.html')
@login_required
def contacts():
    return render_template('contacts.html')
# [END contacts]


# [START contacts_2]
@app.route('/contacts_2.html')
@login_required
def contacts_2():
    return render_template('contacts_2.html')
# [END contacts_2]


# [START css_animation]
@app.route('/css_animation.html')
@login_required
def css_animation():
    return render_template('css_animation.html')
# [END css_animation]


# [START dashboard_2]
@app.route('/dashboard_2.html')
@login_required
def dashboard_2():
    return render_template('dashboard_2.html')
# [END dashboard_2]


# [START dashboard_3]
@app.route('/dashboard_3.html')
@login_required
def dashboard_3():
    return render_template('dashboard_3.html')
# [END dashboard_3]


# [START dashboard_4]
@app.route('/dashboard_4.html')
@login_required
def dashboard_4():
    return render_template('dashboard_4.html')
# [END dashboard_4]


# [START dashboard_4_1]
@app.route('/dashboard_4_1.html')
@login_required
def dashboard_4_1():
    return render_template('dashboard_4_1.html')
# [END dashboard_4_1]


# [START dashboard_5]
@app.route('/dashboard_5.html')
@login_required
def dashboard_5():
    return render_template('dashboard_5.html')
# [END dashboard_5]


# [START diff]
@app.route('/diff.html')
@login_required
def diff():
    return render_template('diff.html')
# [END diff]


# [START draggable_panels]
@app.route('/draggable_panels.html')
@login_required
def draggable_panels():
    return render_template('draggable_panels.html')
# [END draggable_panels]


# [START ecommerce-cart]
@app.route('/ecommerce-cart.html')
@login_required
def ecommerce_cart():
    return render_template('ecommerce-cart.html')
# [END ecommerce-cart]


# [START ecommerce-orders]
@app.route('/ecommerce-orders.html')
@login_required
def ecommerce_orders():
    return render_template('ecommerce-orders.html')
# [END ecommerce-orders]


# [START ecommerce_payments]
@app.route('/ecommerce_payments.html')
@login_required
def ecommerce_payments():
    return render_template('ecommerce_payments.html')
# [END ecommerce_payments]


# [START ecommerce_product]
@app.route('/ecommerce_product.html')
@login_required
def ecommerce_product():
    return render_template('ecommerce_product.html')
# [END ecommerce_product]


# [START ecommerce_product_detail]
@app.route('/ecommerce_product_detail.html')
@login_required
def ecommerce_product_detail():
    return render_template('ecommerce_product_detail.html')
# [END ecommerce_product_detail]


# [START ecommerce_product_list]
@app.route('/ecommerce_product_list.html')
@login_required
def ecommerce_product_list():
    return render_template('ecommerce_product_list.html')
# [END ecommerce_product_list]


# [START ecommerce_product_grid]
@app.route('/ecommerce_product_grid.html')
@login_required
def ecommerce_product_grid():
    return render_template('ecommerce_product_grid.html')
# [END ecommerce_product_grid]


# [START email_template]
@app.route('/email_template.html')
@login_required
def email_template():
    return render_template('email_template.html')
# [END email_template]


# [START empty_page]
@app.route('/empty_page.html')
@login_required
def empty_page():
    return render_template('empty_page.html')
# [END empty_page]


# [START faq]
@app.route('/faq.html')
@login_required
def faq():
    return render_template('faq.html')
# [END faq]


# [START file_manager]
@app.route('/file_manager.html')
@login_required
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
@login_required
def form_advanced():
    return render_template('form_advanced.html')
# [END form_advanced]


# [START form_basic]
@app.route('/form_basic.html')
@login_required
def form_basic():
    return render_template('form_basic.html')
# [END form_basic]


# [START form_editors]
@app.route('/form_editors.html')
@login_required
def form_editors():
    return render_template('form_editors.html')
# [END form_editors]


# [START form_file_upload]
@app.route('/form_file_upload.html')
@login_required
def form_file_upload():
    return render_template('form_file_upload.html')
# [END form_file_upload]


# [START form_markdown]
@app.route('/form_markdown.html')
@login_required
def form_markdown():
    return render_template('form_markdown.html')
# [END form_markdown]


# [START form_wizard]
@app.route('/form_wizard.html')
@login_required
def form_wizard():
    return render_template('form_wizard.html')
# [END form_wizard]


# [START forum_main]
@app.route('/forum_main.html')
@login_required
def forum_main():
    return render_template('forum_main.html')
# [END forum_main]


# [START forum_post]
@app.route('/forum_post.html')
@login_required
def forum_post():
    return render_template('forum_post.html')
# [END forum_post]


# [START full_height]
@app.route('/full_height.html')
@login_required
def full_height():
    return render_template('full_height.html')
# [END full_height]


# [START google_maps]
@app.route('/google_maps.html')
@login_required
def google_maps():
    return render_template('google_maps.html')
# [END google_maps]


# [START graph_chartist]
@app.route('/graph_chartist.html')
@login_required
def graph_chartist():
    return render_template('graph_chartist.html')
# [END graph_chartist]


# [START graph_chartjs]
@app.route('/graph_chartjs.html')
@login_required
def graph_chartjs():
    return render_template('graph_chartjs.html')
# [END graph_chartjs]


# [START graph_flot]
@app.route('/graph_flot.html')
@login_required
def graph_flot():
    return render_template('graph_flot.html')
# [END graph_flot]


# [START graph_morris]
@app.route('/graph_morris.html')
@login_required
def graph_morris():
    return render_template('graph_morris.html')
# [END graph_morris]


# [START graph_peity]
@app.route('/graph_peity.html')
@login_required
def graph_peity():
    return render_template('graph_peity.html')
# [END graph_peity]


# [START graph_rickshow]
@app.route('/graph_rickshow.html')
@login_required
def graph_rickshow():
    return render_template('graph_rickshow.html')
# [END graph_rickshow]


# [START graph_sparkline]
@app.route('/graph_sparkline.html')
@login_required
def graph_sparkline():
    return render_template('graph_sparkline.html')
# [END graph_sparkline]


# [START grid_options]
@app.route('/grid_options.html')
@login_required
def grid_options():
    return render_template('grid_options.html')
# [END grid_options]


# [START i18support]
@app.route('/i18support.html')
@login_required
def i18support():
    return render_template('i18support.html')
# [END i18support]


# [START icons]
@app.route('/icons.html')
@login_required
def icons():
    return render_template('icons.html')
# [END icons]


# [START idle_timer]
@app.route('/idle_timer.html')
@login_required
def idle_timer():
    return render_template('idle_timer.html')
# [END idle_timer]


# [START index]
@app.route('/index.html')
@login_required
def index():
    return render_template('index.html')
# [END index]


# [START invoice]
@app.route('/invoice.html')
@login_required
def invoice():
    return render_template('invoice.html')
# [END invoice]


# [START invoice_print]
@app.route('/invoice_print.html')
@login_required
def invoice_print():
    return render_template('invoice_print.html')
# [END invoice_print]


# [START issue_tracker]
@app.route('/issue_tracker.html')
@login_required
def issue_tracker():
    return render_template('issue_tracker.html')
# [END issue_tracker]


# [START jq_grid]
@app.route('/jq_grid.html')
@login_required
def jq_grid():
    return render_template('jq_grid.html')
# [END jq_grid]


# [START landing]
@app.route('/landing.html')
@login_required
def landing():
    return render_template('landing.html')
# [END landing]


# [START layouts]
@app.route('/layouts.html')
@login_required
def layouts():
    return render_template('layouts.html')
# [END layouts]


# [START loading_buttons]
@app.route('/loading_buttons.html')
@login_required
def loading_buttons():
    return render_template('loading_buttons.html')
# [END loading_buttons]


# [START lockscreen]
@app.route('/lockscreen.html')
@login_required
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
@login_required
def mail_compose():
    return render_template('mail_compose.html')
# [END mail_compose]


# [START mail_detail]
@app.route('/mail_detail.html')
@login_required
def mail_detail():
    return render_template('mail_detail.html')
# [END mail_detail]


# [START mailbox]
@app.route('/mailbox.html')
@login_required
def mailbox():
    return render_template('mailbox.html')
# [END mailbox]


# [START masonry]
@app.route('/masonry.html')
@login_required
def masonry():
    return render_template('masonry.html')
# [END masonry]


# [START md-skin]
@app.route('/md-skin.html')
@login_required
def md_skin():
    return render_template('md-skin.html')
# [END md-skin]


# [START metrics]
@app.route('/metrics.html')
@login_required
def metrics():
    return render_template('metrics.html')
# [END metrics]


# [START modal_window]
@app.route('/modal_window.html')
@login_required
def modal_window():
    return render_template('modal_window.html')
# [END modal_window]


# [START nestable_list]
@app.route('/nestable_list.html')
@login_required
def nestable_list():
    return render_template('nestable_list.html')
# [END nestable_list]


# [START notifications]
@app.route('/notifications.html')
@login_required
def notifications():
    return render_template('notifications.html')
# [END notifications]


# [START off_canvas_menu]
@app.route('/off_canvas_menu.html')
@login_required
def off_canvas_menu():
    return render_template('off_canvas_menu.html')
# [END off_canvas_menu]


# [START package]
@app.route('/package.html')
@login_required
def package():
    return render_template('package.html')
# [END package]


# [START pin_board]
@app.route('/pin_board.html')
@login_required
def pin_board():
    return render_template('pin_board.html')
# [END pin_board]


# [START profile]
@app.route('/profile.html')
@login_required
def profile():
    return render_template('profile.html')
# [END profile]


# [START profile_2]
@app.route('/profile_2.html')
@login_required
def profile_2():
    return render_template('profile_2.html')
# [END profile_2]


# [START project_detail]
@app.route('/project_detail.html')
@login_required
def project_detail():
    return render_template('project_detail.html')
# [END project_detail]


# [START projects]
@app.route('/projects.html')
@login_required
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
@login_required
def resizeable_panels():
    return render_template('resizeable_panels.html')
# [END resizeable_panels]


# [START search_results]
@app.route('/search_results.html')
@login_required
def search_results():
    return render_template('search_results.html')
# [END search_results]


# [START skin-config]
@app.route('/skin-config.html')
@login_required
def skin_config():
    return render_template('skin-config.html')
# [END skin-config]


# [START slick_carousel]
@app.route('/slick_carousel.html')
@login_required
def slick_carousel():
    return render_template('slick_carousel.html')
# [END slick_carousel]


# [START social_feed]
@app.route('/social_feed.html')
@login_required
def social_feed():
    return render_template('social_feed.html')
# [END social_feed]


# [START spinners]
@app.route('/spinners.html')
@login_required
def spinners():
    return render_template('spinners.html')
# [END spinners]


# [START sweetalert]
@app.route('/sweetalert.html')
@login_required
def sweetalert():
    return render_template('sweetalert.html')
# [END sweetalert]


# [START table_basic]
@app.route('/table_basic.html')
@login_required
def table_basic():
    return render_template('table_basic.html')
# [END table_basic]


# [START table_data_tables]
@app.route('/table_data_tables.html')
@login_required
def table_data_tables():
    return render_template('table_data_tables.html')
# [END table_data_tables]


# [START table_foo_table]
@app.route('/table_foo_table.html')
@login_required
def table_foo_table():
    return render_template('table_foo_table.html')
# [END table_foo_table]


# [START tabs]
@app.route('/tabs.html')
@login_required
def tabs():
    return render_template('tabs.html')
# [END tabs]


# [START tabs_panels]
@app.route('/tabs_panels.html')
@login_required
def tabs_panels():
    return render_template('tabs_panels.html')
# [END tabs_panels]


# [START teams_board]
@app.route('/teams_board.html')
@login_required
def teams_board():
    return render_template('teams_board.html')
# [END teams_board]


# [START timeline]
@app.route('/timeline.html')
@login_required
def timeline():
    return render_template('timeline.html')
# [END timeline]


# [START timeline_2]
@app.route('/timeline_2.html')
@login_required
def timeline_2():
    return render_template('timeline_2.html')
# [END timeline_2]


# [START tinycon]
@app.route('/tinycon.html')
@login_required
def tinycon():
    return render_template('tinycon.html')
# [END tinycon]


# [START toastr_notifications]
@app.route('/toastr_notifications.html')
@login_required
def toastr_notifications():
    return render_template('toastr_notifications.html')
# [END toastr_notifications]


# [START tour]
@app.route('/tour.html')
@login_required
def tour():
    return render_template('tour.html')
# [END tour]


# [START tree_view]
@app.route('/tree_view.html')
@login_required
def tree_view():
    return render_template('tree_view.html')
# [END tree_view]


# [START truncate]
@app.route('/truncate.html')
@login_required
def truncate():
    return render_template('truncate.html')
# [END truncate]


# [START typography]
@app.route('/typography.html')
@login_required
def typography():
    return render_template('typography.html')
# [END typography]


# [START validation]
@app.route('/validation.html')
@login_required
def validation():
    return render_template('validation.html')
# [END validation]


# [START video]
@app.route('/video.html')
@login_required
def video():
    return render_template('video.html')
# [END video]


# [START vote_list]
@app.route('/vote_list.html')
@login_required
def vote_list():
    return render_template('vote_list.html')
# [END vote_list]


# [START widgets]
@app.route('/widgets.html')
@login_required
def widgets():
    return render_template('widgets.html')
# [END widgets]