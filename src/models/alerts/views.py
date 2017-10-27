from flask import Blueprint, render_template, request, session, redirect, url_for, flash

from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.models.users.decorators as user_decorators

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/new', methods=['POST', 'GET'])
@user_decorators.requires_login  # redirect the users to the login page if session['email'] is None
def create_alert():
    if request.method == 'POST':
        name = request.form['item_name']
        url = request.form['item_url']
        price_limit = float(request.form['price_limit'])

        item = Item(name=name, url=url)
        item.save_to_db()

        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price()
        flash("Dang ky alert thanh cong")

        return redirect(url_for('users.user_alerts'))

    return render_template('alerts/create_alert.jinja2')


@alert_blueprint.route('/edit/<string:alert_id>', methods=['POST', 'GET'])
@user_decorators.requires_login
def edit_alert(alert_id):
    alert = Alert.from_db_by_id(alert_id)
    if request.method == 'POST':
        name = request.form['item_name']
        price_limit = float(request.form['price_limit'])

        alert.item.name = name
        alert.price_limit = price_limit

        alert.item.save_to_db()
        alert.save_to_db()
        flash("Update alert thanh cong")
        return redirect(url_for('users.user_alerts'))

    return render_template('alerts/edit_alert.jinja2', alert=alert)


@alert_blueprint.route('/deactivate/<string:alert_id>')
def deactivate_alert(alert_id):
    Alert.from_db_by_id(alert_id).deactivate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/activate/<string:alert_id>')
def activate_alert(alert_id):
    Alert.from_db_by_id(alert_id).activate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/delete/<string:alert_id>')
def delete_alert(alert_id):
    Alert.from_db_by_id(alert_id).delete()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/<string:alert_id>')
@user_decorators.requires_login
def get_alert_page(alert_id):
    alert = Alert.from_db_by_id(alert_id)
    return render_template("alerts/alerts.jinja2", alert=alert)


@alert_blueprint.route('/for_user/<string:user_id>')
def get_alert_for_user(user_id):
    pass


@alert_blueprint.route('/check_alert_price/<string:alert_id>')
def check_alert_price(alert_id):
    Alert.from_db_by_id(alert_id).load_item_price()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))
