from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from app.user_handler import Users
from werkzeug.security import generate_password_hash

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    default_content = "Who What Where"
    return render_template('dashboard.html', default_content=default_content)

@dashboard_bp.route('/dashboard/admin_center')
def admin_center():
    return render_template('admin_center.html')

@dashboard_bp.route('/dashboard/availability')
def availability():
    return render_template('availability.html')

@dashboard_bp.route('/dashboard/availability/submit_availability', methods=['GET', 'POST'])
def submit_availability():
    if request.method == 'POST':
        availability_data = {}
        days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        # Iterate through form data and extract availability for each day
        for day in days_of_week:
            start_times = request.form.getlist(day.lower() + '_start')
            stop_times = request.form.getlist(day.lower() + '_stop')
            availabilities = []
            for start_time, stop_time in zip(start_times, stop_times):
                availability = {'start_time': start_time, 'stop_time': stop_time}
                availabilities.append(availability)
            availability_data[day] = availabilities

    return render_template('availability.html', availability_data=availability_data)    

@dashboard_bp.route('/dashboard/analytics')
def analytics():
    return render_template('analytics.html')    

@dashboard_bp.route('/dashboard/help')
def help():
    return render_template('help.html')     