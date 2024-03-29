from app.availability_handler import Availability
from app.employee_handler import Employee
from werkzeug.security import generate_password_hash
from datetime import time, datetime
from flask import request, session
import json

availability_handler = Availability()
employee_handler = Employee()

class availabilityLogic:
    
    def load_availability(self, user_id):
        # Check if the user already has availability data in the database
        availability_data = availability_handler.get_avail(user_id)

        # Check if the user has existing availability data
        if availability_data:

            availability_by_day = {}
            for day, times in availability_data.items():
                start_time = times['start_time']
                stop_time = times['stop_time']
                # Format or process the times as needed
                availability_by_day[day] = f"{start_time} - {stop_time}"
        else:
            # Handle the case where there is no availability data
            availability_by_day = None

        return availability_by_day

    def send_availability(self, user_id):
        start_field_suffix = '_start'
        stop_field_suffix = '_stop'

        availability_data = {}  # Initialize an empty dictionary for availability data

        # Iterate through form data and extract availability for each day
        for field_name, field_value in request.form.items():
            if field_name.endswith(start_field_suffix):
                day = field_name[:-len(start_field_suffix)]
                stop_time_field_name = day + stop_field_suffix

                start_time = request.form.get(field_name)
                stop_time = request.form.get(stop_time_field_name)

  
                # Add the availability for the day to the dictionary
                availability_data[day] = {
                    'start_time': start_time,
                    'stop_time': stop_time
                }

        # Convert the availability data dictionary to a JSON string
        availability_json = json.dumps(availability_data)

        availability_handler.update_avail(user_id, availability_json)

    def get_user_id_by_subdirect(self, subdirectory, subdomain):
        result = availability_handler.get_user_id(subdirectory, subdomain)
        return result   
