from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response
from app.user_handler import Users
from werkzeug.security import generate_password_hash


admin_center_bp = Blueprint('admin_center', __name__)
user_handler = Users()

@admin_center_bp.route('/')
def admin_center():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
    return render_template('admin_center.html') 

@admin_center_bp.route('/services', methods=['GET'])
def services():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))

    price_type_mapping = {
            'per_hour': 'Hourly',
            'per_service': 'Per Service'
        }    

    services_data = user_handler.get_services(user_id)
    if services_data[0] == True:
        print(services_data[1])
        _, _, service_names, prices, price_types = services_data[1]

        formatted_service_list = []

        # Convert Decimal prices to string and strip the trailing zeroes
        price_strings = [str(price).rstrip('0').rstrip('.') for price in prices]
        price_types_list = price_types.strip("{}").split(",")
        
        # Construct string representations of each service
        service_strings = []
        for name, price, price_type in zip(service_names, price_strings, price_types_list):
            display_price_type = price_type_mapping.get(price_type, price_type)
            service_strings.append(f"{name}: {display_price_type} - ${price}")

        # Join the formatted service list with newline characters
        formatted_service_data = "\n".join(service_strings)
    else:
        formatted_service_data = None    


    return render_template('services.html', formatted_service_data=formatted_service_data)   

@admin_center_bp.route('/services', methods=['POST'])
def post_services():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
    service_list = request.form.get('service-list')
    print(service_list)
    rows = service_list.split('\n')

    service_names = []
    service_types = []
    prices = []
    type_mapping = {
    "Hourly": "per_hour",
    "Per Service": "per_service"
    }

    for row in rows:
        try:
            service_name, other_details = row.split(": ", 1)
            service_type, price = other_details.split(" - $")
            mapped_type = type_mapping.get(service_type, service_type)

            # Append the values to their respective lists
            service_names.append(service_name)
            service_types.append(mapped_type)
            prices.append(price)
        except ValueError as e:

            print("Not An Error:", e)
        # Assuming service_names is a list of strings
    service_n_array = "{" + ", ".join(f'"{name}"' for name in service_names) + "}"
    service_t_array = "{" + ",".join(service_types) + "}"
    price_literals = [str(price) for price in prices]
    postgresql_prices_array = "{" + ",".join(price_literals) + "}"

    services_data = user_handler.get_services(user_id)
    if services_data[0] == True:
        user_handler.update_services(user_id, service_n_array, service_t_array, postgresql_prices_array)
    else:    
        user_handler.save_services(user_id, service_n_array, service_t_array, postgresql_prices_array)

    return Response(status=204)     

@admin_center_bp.route('/manage_employees', methods=['GET'])
def manage_employees():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))

    employee_data_list = user_handler.get_employees(user_id)


    visible_data = ""
    hidden_data = ""
    for employee_data in employee_data_list[1]:
        
        # Unpack the employee data
        _, email, phone_number, password_hash, f_name, l_name = employee_data
        visible_data += f"{f_name}, {l_name}\n"
        # Concatenate email, phone number, and password for hidden textarea
        hidden_data += f"{email}, {phone_number}, {password_hash}\n"

         
    return render_template('manage_employees.html', visible_data=visible_data, hidden_data=hidden_data)    

@admin_center_bp.route('/manage_employees', methods=['POST'])
def post_manage_employees():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))

    employees_names = [name.strip() for name in request.form.get('employee-list').split('\n')]
    employees_data = request.form.get('hidden-employee-list').split('\n')
    employees_data = [data.strip() for data in employees_data if data.strip()]

    emails = []
    phone_numbers = []
    passwords = []
    f_names = []
    l_names = []

    for name, data in zip(employees_names, employees_data):
        try:
            f_name, l_name = [item.strip() for item in name.split(", ")]
            f_names.append(f_name)
            l_names.append(l_name)

            email, phone_number, password = [item.strip() for item in data.split(", ")]
            emails.append(email)
            phone_numbers.append(phone_number)
            passwords.append(password)
        except ValueError as e:
            print("not an error:", e)

    phone_number_list = user_handler.get_employees(user_id)
    for _, _, phone, _, _, _ in phone_number_list[1]:
        if phone not in phone_numbers:
            user_handler.delete_employees(phone)

    for f_name, l_name, email, phone_number, password in zip(f_names, l_names, emails, phone_numbers, passwords):
        phone_number_list = user_handler.get_employees(user_id)
        db_phone_numbers = [employee[2] for employee in phone_number_list[1]]
        
        if phone_number in db_phone_numbers:
            # Phone number already exists, update user
            hashed_password = generate_password_hash(password)
            user_handler.update_employees(user_id, f_name, l_name, email, phone_number, hashed_password)
        else:
            # Phone number doesn't exist, add new user
            user_handler.add_employees(user_id, f_name, l_name, email, phone_number, hashed_password)
        

    

        #if user_handler.get_employees(user_id)[1]:
            # Update existing employee
        #    user_handler.update_employees(user_id, f_name, l_name, email, phone_number, password)
       # else:
        #    hashed_password = generate_password_hash(password)
            

    return Response(status=204)     

@admin_center_bp.route('/upload_files')
def upload_files():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
    return render_template('upload_files.html')

@admin_center_bp.route('/customer_info')
def customer_info():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
    return render_template('customer_info.html')

@admin_center_bp.route('/customer_portal')
def customer_portal():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
    return render_template('customer_portal.html')
               