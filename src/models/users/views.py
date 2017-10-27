from flask import Blueprint, render_template, redirect, url_for, request, session
import src.models.users.errors as UserErrors
from src.models.users.user import User

user_blueprint = Blueprint('users', __name__)
import src.models.users.decorators as user_decorators


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect((url_for('.user_alerts')))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/login.jinja2")  # Send the user an error if their login was invalid


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for('.user_alerts'))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/register.jinja2")


@user_blueprint.route('/alerts')
@user_decorators.requires_login
def user_alerts():
    user = User.from_db_by_email(session['email'])
    alerts = user.get_alerts()
    return render_template('users/alerts.jinja2', alerts=alerts, user_email=user.email)


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))


@user_blueprint.route('/check_alert/<string:user_id>')
def check_user_alert(user_id):
    pass
