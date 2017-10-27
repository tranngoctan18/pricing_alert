from flask import Flask, render_template
from src.common.database import Database
from flask_moment import Moment


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('src.config')
app.secret_key = '123'

app.route('/')
def hello_world():
    return "hello world!"

@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.jinja2')


from src.models.users.views  import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/users')

from src.models.alerts.views import alert_blueprint
app.register_blueprint(alert_blueprint, url_prefix='/alerts')

from src.models.stores.views import store_blueprint
app.register_blueprint(store_blueprint, url_prefix='/stores')