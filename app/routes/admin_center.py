from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response
from app.employee_handler import Employee
from werkzeug.security import generate_password_hash


admin_center_bp = Blueprint('admin_center', __name__)
employee_handler = Employee()

@admin_center_bp.route('/')
def admin_center():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
    return render_template('owner/admin_center.html')      

@admin_center_bp.route('/manage_employees', methods=['GET'])
def manage_employees():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))

    employee_data_list = employee_handler.get_employees(user_id)


    visible_data = ""
    hidden_data = ""
    for employee_data in employee_data_list[1]:
        
        # Unpack the employee data
        _, email, phone_number, password_hash, f_name, l_name = employee_data
        visible_data += f"{f_name}, {l_name}\n"
        # Concatenate email, phone number, and password for hidden textarea
        hidden_data += f"{email}, {phone_number}, {password_hash}\n"

         
    return render_template('owner/manage_employees.html', visible_data=visible_data, hidden_data=hidden_data)    

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

    phone_number_list = employee_handler.get_employees(user_id)
    for _, _, phone, _, _, _ in phone_number_list[1]:
        if phone not in phone_numbers:
            employee_handler.delete_employees(phone)

    for f_name, l_name, email, phone_number, password in zip(f_names, l_names, emails, phone_numbers, passwords):
        phone_number_list = employee_handler.get_employees(user_id)
        db_phone_numbers = [employee[2] for employee in phone_number_list[1]]
        
        if phone_number in db_phone_numbers:
            # Phone number already exists, update user  
            employee_handler.update_employees(user_id, f_name, l_name, email, phone_number, password)
        else:
            hashed_password = generate_password_hash(password)
            employee_handler.add_employees(user_id, f_name, l_name, email, phone_number, hashed_password)
            
    return Response(status=204)     

@admin_center_bp.route('/upload_files')
def upload_files():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
    return render_template('owner/upload_files.html')

@admin_center_bp.route('/customer_info')
def customer_info():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
    return render_template('owner/customer_info.html')

@admin_center_bp.route('/customer_portal')
def customer_portal():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
    return render_template('owner/customer_portal.html')
               