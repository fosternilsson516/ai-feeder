from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response, current_app
from app.business_handler import Business
import os

customer_routes_bp = Blueprint('customer_routes', __name__, subdomain='<subdomain>')
business_handler = Business()

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
    for employee_headshot, emp_f_name, emp_l_name, service_array in zip(employee_headshots, emp_f_names, emp_l_names, service_names):
        if employee_headshot:
            headshot_filename = os.path.basename(employee_headshot)
            headshot = url_for('static', filename=f'img/{headshot_filename}')
        else:
            # Provide a default headshot URL or handle it differently
            headshot = url_for('static', filename='img/no-image.jpg')
        employee = f"{headshot} {emp_f_name} {emp_l_name} {service_array}"
        employees.append(employee)
    print(employees)    

    return render_template("customer/customer_routes.html", styling=styling, business_name=business_name, address=business_address, logo_url=logo_url, bio=business_bio, employees=employees)


### each employee will get a subdirectory that a user can go straight to or they can start on the main page and the subdirectory will be filled dynamically.
#@customer_routes_bp.route("/<subdirectory>")
#def subdirectory():
 #   return 'This is a subdirectory'    