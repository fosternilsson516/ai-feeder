from flask import Flask, render_template, session, Blueprint
from werkzeug.security import generate_password_hash

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    default_content = "Who What Where"
    return render_template('dashboard.html', default_content=default_content)

    

  

    