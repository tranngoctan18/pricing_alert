from urllib.parse import urlparse

from flask import Blueprint, render_template, url_for, request, redirect, flash, json

from src.models.stores.store import Store
import src.models.users.decorators as user_decorators

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    return render_template('stores/store.jinja2', store=Store.get_by_id(store_id))


@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('stores/store_list.jinja2', stores=stores)


@store_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.require_admin_permisson
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = urlparse(request.form['url_prefix']).hostname
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        Store(name, url_prefix, tag_name, query).save_to_db()
        flash("dang ky store moi thanh cong")
        return redirect(url_for('stores.index'))

    return render_template('stores/create_store.jinja2')


@store_blueprint.route('/edit/<string:store_id>', methods=['POST', 'GET'])
@user_decorators.require_admin_permisson
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = urlparse(request.form['url_prefix']).hostname
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        store.name = name
        store.url_prefix = url_prefix
        store.tag_name = tag_name
        store.query = query

        store.save_to_db()
        flash("update store moi thanh cong")

        return redirect(url_for('stores.index'))
    return render_template('stores/edit_store.jinja2', store=store)


@store_blueprint.route('/delete/<string:store_id>')
def delete_store(store_id):
    Store.get_by_id(store_id).delete()
    return redirect(url_for('stores.index'))
