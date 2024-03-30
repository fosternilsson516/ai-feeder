from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response, current_app
from app.availability_handler import Availability
import os


admin_center_bp = Blueprint('admin_center', __name__)
availability_handler = Availability()

@admin_center_bp.route('/')
def admin_center():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))

    subdomain = availability_handler.get_subdomain(user_id)
    full_url = f"http://{subdomain}.local:5000"

    return render_template('owner/admin_center.html', full_url=full_url)      
  
               