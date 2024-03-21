from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response, current_app
from app.business_handler import Business
from app.logic.availability_logic import availabilityLogic
from app.logic.calendars_logic import calendarLogic
from calendar import datetime
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
         business_logo_filepath, services) = result1

    service_list = [service.strip() for service in services.split('\n')]
    print(service_list)
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
 
        employees.append(employee)
        emp_bios.append(emp_bio)

    employees_with_bios = zip(employees, emp_bios) 
    return render_template("customer/customer_routes.html", styling=styling, business_name=business_name, address=business_address, logo_url=logo_url,
     business_story=business_bio, employees_with_bios=employees_with_bios, subdomain=subdomain, service_list=service_list)


@customer_routes_bp.route("/<subdirectory>", subdomain="<subdomain>")
def subdirectory(subdomain, subdirectory):

    subdirectory_with_space = subdirectory.replace("_", " ")
    heading = f"{subdirectory_with_space}'s Availability"

    user_id = availability_logic.get_user_id_by_subdirect(subdirectory, subdomain)

    avail = availability_logic.load_availability(user_id)
    hours_by_day = calendars_logic.process_availability(avail)

    cal, month_name, year = calendars_logic.current_calendar()

    processed_calendar = []
    for week in cal:
        processed_week = []
        for day in week:
            for weekday in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
                processed_week.append(hours_by_day.get(weekday, []))
        processed_calendar.append(processed_week)

    return render_template("customer/calendar.html", subdirectory=subdirectory,
    month_name=month_name, year=year, heading=heading, calendar=cal, processed_calendar=processed_calendar)

@customer_routes_bp.route("/<subdirectory>/start", subdomain="<subdomain>")
def start_appointment(subdomain, subdirectory):   

    return render_template("customer/start_appointment.html")

@customer_routes_bp.route("/<subdirectory>", subdomain="<subdomain>", methods=['POST'])
def post_subdirectory(subdomain, subdirectory):
    return render_template("customer/start_appointment.html")

