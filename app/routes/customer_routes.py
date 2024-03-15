from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response, current_app
from app.business_handler import Business
from app.logic.availability_logic import availabilityLogic
from app.logic.calendars_logic import calendarLogic
import calendar
import os

customer_routes_bp = Blueprint('customer_routes', __name__, subdomain='<subdomain>')
business_handler = Business()
availability_logic = availabilityLogic()
calendars_logic = calendarLogic()

@customer_routes_bp.route('/', subdomain="<subdomain>")
def customer_routes(subdomain):

    result1 = business_handler.get_subdomain_data(subdomain)
    if result1:
        (business_id, business_name, business_street, business_city,
         business_state, business_zip, _, business_bio, business_style_id,
         business_logo_filepath) = result1

    business_address = f"{business_street} {business_city} {business_state} {business_zip}" 
    styling = business_handler.get_styling(business_style_id)
    business_filename = os.path.basename(business_logo_filepath)
    logo_url = url_for('static', filename=f'img/{business_filename}')
    print(styling)

    other_main_page_data = business_handler.get_business_employee_data(business_id)
    if other_main_page_data:
        (employee_user_ids, employee_subdirectories, employee_bios,
         employee_headshots, emp_f_names, emp_l_names, service_names) = other_main_page_data  

    employees = []
    emp_bios = []
    for employee_headshot, emp_f_name, emp_l_name, service_array, employee_subdirectory, employee_bio in zip(employee_headshots, emp_f_names, emp_l_names, service_names, employee_subdirectories, employee_bios):
        if employee_headshot:
            headshot_filename = os.path.basename(employee_headshot)
            headshot = url_for('static', filename=f'img/{headshot_filename}')
        else:
            # Provide a default headshot URL or handle it differently
            headshot = url_for('static', filename='img/no-image.jpg')

        emp_f_name = emp_f_name if emp_f_name else "Unknown"
        emp_l_name = emp_l_name if emp_l_name else ""
        employee_subdirectory = employee_subdirectory if employee_subdirectory else "default_subdirectory"
        employee_bio = employee_bio if employee_bio else ""   

        services_string = ', '.join(service_array)    
        employee = f"{headshot} {emp_f_name} {emp_l_name} {employee_subdirectory} {services_string}"
        emp_bio = employee_bio
        print(employee)
        print(emp_bio)
        employees.append(employee)
        emp_bios.append(emp_bio)

    employees_with_bios = zip(employees, emp_bios) 
    return render_template("customer/customer_routes.html", styling=styling, business_name=business_name, address=business_address, logo_url=logo_url,
     business_story=business_bio, employees_with_bios=employees_with_bios, subdomain=subdomain)

############show employees availability on a calendar
############go set up customer information required and show to customer when they select a time 
###########set up testing emiat to sms to test message for approving appointment
##########show appointment time on employee calendar
@customer_routes_bp.route("/<subdirectory>", subdomain="<subdomain>")
def subdirectory(subdomain, subdirectory):

    subdirectory_with_space = subdirectory.replace("_", " ")
    heading = f"{subdirectory_with_space}'s Availability"


    user_id = availability_logic.get_user_id_by_subdirect(subdirectory, subdomain)

    avail = availability_logic.load_availability(user_id)
    processed_availability = {}
    for day, times in avail.items():
        if times == 'Not available':
            processed_availability[day] = [0] * 24  # Mark all hours as unavailable
        else:
            start_time, end_time = times.split(' - ')
            start_hour, _ = map(int, start_time.split(':'))
            end_hour, _ = map(int, end_time.split(':'))
            availability_hours = [1 if start_hour <= hour < end_hour else 0 for hour in range(24)]
            processed_availability[day] = availability_hours
        
    
    cal, month_name, year = calendars_logic.current_calendar()
    availability_month = []

    # Iterate over each day in the calendar
    for week in cal:
        for day in week:
            if day != 0:
                day_index = day % 7
                # Get the day of the week name corresponding to the index
                day_name_of_week = calendar.day_name[day_index]
                # Get the availability data for the corresponding day of the week
                availability_data = processed_availability[day_name_of_week]
                # Append the availability data for this day to the availability_month list
                availability_month.append(availability_data)
    zipped_data = zip(cal, availability_month)
    print(zipped_data)
    print(cal)
    return render_template("customer/calendar.html", subdirectory=subdirectory, zipped_data=zipped_data,
    month_name=month_name, year=year, heading=heading)