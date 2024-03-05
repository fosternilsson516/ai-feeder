from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response
from app.user_handler import Users
from werkzeug.security import generate_password_hash
from datetime import time, datetime

availability_bp = Blueprint('availability', __name__)
user_handler = Users()

@availability_bp.route('/', methods=['GET'])
def get_availability():
    # Check if the user is logged in
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))

    # Check if the user already has availability data in the database
    existing_availability = user_handler.get_avail(user_id)

    # If user has existing availability data, retrieve the data
    if existing_availability[0] == True:
        #availability_data = user_handler.get_avail(user_id)
        # Unpack the availability data tuple
        _, _, start_times, stop_times, days = existing_availability[1]
        print(existing_availability[1])
        
        # Create a dictionary to hold the availability data for each day
        availability_by_day = {}
        for day, start_time, stop_time in zip(days, start_times, stop_times):
        # Check if both start and stop times are provided
            if start_time and stop_time:
                availability_by_day[day] = f"{start_time.strftime('%H:%M')} - {stop_time.strftime('%H:%M')}"
            else:
                availability_by_day[day] = "Not available"
            
        print(availability_by_day)
        
    else:
        availability_by_day = None

    # Render the availability template with existing data if available
    return render_template('availability.html', availability_by_day=availability_by_day)    

@availability_bp.route('/', methods=['POST'])
def availability():
    # Check if the user is logged in
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
    
    start_field_suffix = '_start'
    stop_field_suffix = '_stop'

    days = []
    start_times = []
    stop_times = []
    
    # Iterate through form data and extract availability for each day
    for field_name, field_value in request.form.items():
        if field_name.endswith(start_field_suffix):
            day = field_name[:-len(start_field_suffix)]
            stop_time_field_name = day + stop_field_suffix
            start_time_values = request.form.getlist(field_name)
            stop_time_values = request.form.getlist(stop_time_field_name)
            #day_number = day_mapping.get(day)
            
            # Append day, start time, and stop time to their respective lists
            for start_time, stop_time in zip(start_time_values, stop_time_values):
                days.append(day)
                if start_time and stop_time:  # Check if both start and stop times are provided
                    start_time_obj = time.fromisoformat(start_time)
                    stop_time_obj = time.fromisoformat(stop_time)
                else:
                    start_time_obj = stop_time_obj = None  # Set to None if time is not provided
                start_times.append(start_time_obj)
                stop_times.append(stop_time_obj)

    # Check if the user already has availability data in the database
    existing_availability = user_handler.get_avail(user_id)
    print(existing_availability)

    # If user has existing availability data, update the corresponding row
    if existing_availability[0] == True:
        # Update existing availability data in the database
        user_handler.update_avail(user_id, days, start_times, stop_times)
    else:
        user_handler.submit_avail(user_id, days, start_times, stop_times)

    return Response(status=204)