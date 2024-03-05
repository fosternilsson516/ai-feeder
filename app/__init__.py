# app/routes/__init__.py
from flask import Flask
from app.routes.users import users_bp
from app.routes.dashboard import dashboard_bp
from app.routes.calendars import calendar_bp
from app.routes.availability import availability_bp
from app.routes.analytics import analytics_bp
from app.routes.admin_center import admin_center_bp
from app.routes.help import help_bp
from app.db import config

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = config["secret_key"]
app.register_blueprint(users_bp)
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(calendar_bp, url_prefix='/dashboard/calendar')
app.register_blueprint(admin_center_bp, url_prefix='/dashboard/admin_center')
app.register_blueprint(availability_bp, url_prefix='/dashboard/availability')
app.register_blueprint(analytics_bp, url_prefix='/dashboard/analytics')
app.register_blueprint(help_bp, url_prefix='/dashboard/help')
