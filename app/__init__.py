# app/routes/__init__.py
from flask import Flask
from app.routes.users import users_bp
from app.routes.dashboard import dashboard_bp
from app.routes.customer_route import customer_route_bp
from app.routes.setup_chat import setup_chat_bp
from app.routes.url import url_bp
from app.db import config


app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = config["secret_key"]
app.config['SERVER_NAME'] = 'local:5000'
app.register_blueprint(users_bp)
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(customer_route_bp, subdomain='<subdomain>')
app.register_blueprint(setup_chat_bp, url_prefix='/dashboard/setup_chat')
app.register_blueprint(url_bp, url_prefix='/dashboard/url')

