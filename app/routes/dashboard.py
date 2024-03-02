from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response
from app.user_handler import Users
from werkzeug.security import generate_password_hash

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    default_content = "Who What Where"
    return render_template('dashboard.html', default_content=default_content)

@dashboard_bp.route('/calendar')
def calendar():
    return render_template('calendar.html')    

@dashboard_bp.route('/admin_center')
def admin_center():
    return render_template('admin_center.html')

@dashboard_bp.route('/availability', methods=['GET', 'POST'])
def availability():
    if request.method == 'POST':
        day_mapping = {'Sunday': 1, 'Monday': 2, 'Tuesday': 3, 'Wednesday': 4, 'Thursday': 5, 'Friday': 6, 'Saturday': 7}

        days = []
        start_times = []
        stop_times = []
        
        # Iterate through form data and extract availability for each day
        for field_name, field_value in request.form.items():
            if field_name.endswith('_start'):
                day = field_name.split('_')[0]
                stop_time_field_name = day + '_stop'
                start_time_values = request.form.getlist(field_name)
                stop_time_values = request.form.getlist(stop_time_field_name)
                day_number = day_mapping.get(day)
                
                # Append day, start time, and stop time to their respective lists
                for start_time, stop_time in zip(start_time_values, stop_time_values):
                    days.append(day_number)
                    start_times.append(start_time)
                    stop_times.append(stop_time)
        print(days)
        print(start_times)
        print(stop_times)
        print(request.form)
                

        return Response(status=204)
    return render_template('availability.html')      

@dashboard_bp.route('/analytics')
def analytics():
    return render_template('analytics.html')    

@dashboard_bp.route('/help')
def help():
    return render_template('help.html')     