# app/routes/__init__.py
from flask import Flask
from app.routes.users import users_bp
from app.routes.dashboard import dashboard_bp

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = 'your_secret_key_here'
app.register_blueprint(users_bp)
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
