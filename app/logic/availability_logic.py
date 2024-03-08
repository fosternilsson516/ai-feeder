from app.availability_handler import Availability
from app.employee_handler import Employee
from werkzeug.security import generate_password_hash
from datetime import time, datetime
from flask import request

availability_handler = Availability()
employee_handler = Employee()

class availabilityLogic:
    def load_availability(self, user_id):
        # Check if the user already has availability data in the database
        existing_availability = availability_handler.get_avail(user_id)

        # If user has existing availability data, retrieve the data
        if existing_availability[0] == True:
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
        return availability_by_day 

    def send_availability(self, user_id):
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
        existing_availability = availability_handler.get_avail(user_id)

        # If user has existing availability data, update the corresponding row
        if existing_availability[0] == True:
            # Update existing availability data in the database
            availability_handler.update_avail(user_id, days, start_times, stop_times)
        else:
            availability_handler.submit_avail(user_id, days, start_times, stop_times) 

    def employee_availability(self, user_id):
        result = employee_handler.get_owner_name(user_id)
        if result:
            f_name, l_name = result[0], result[1]
        owner_name = f_name + " " + l_name    

        employee_list = employee_handler.get_employees(user_id)
        visible_names = []
        hidden_ids = []
        for employee in employee_list[1]:
            id, _, _, _, f_name, l_name = employee
            visible_names += f"{f_name} {l_name}"
            hidden_ids.append(id)
        employee_data = zip(visible_names, hidden_ids)

        return owner_name, employee_data
