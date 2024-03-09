from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response
from app.logic.availability_logic import availabilityLogic

availability_bp = Blueprint('availability', __name__)
availability_logic = availabilityLogic()

@availability_bp.route('/', methods=['GET'])
def get_availability():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
    user_role = session.get('user_role')    
    if user_role == 'owner':

        full_name, employee_data = availability_logic.employee_availability(user_id)

        availability_by_day = availability_logic.load_availability(user_id)
        # Render the availability template with existing data if available
        return render_template('owner/availability.html', availability_by_day=availability_by_day, full_name=full_name, employee_data=employee_data)  
    elif user_role == 'employee':

        availability_by_day = availability_logic.load_availability(user_id)

        return render_template('employee/availability.html', availability_by_day=availability_by_day)

@availability_bp.route('/update_availability', methods=['GET'])
def update_availability():
    
    user_id = request.args.get('id')
    print(user_id)

    availability_by_day = availability_logic.load_availability(user_id)

    full_name, employee_data = availability_logic.employee_availability(user_id)

    return render_template('owner/availability.html', availability_by_day=availability_by_day, full_name=full_name, employee_data=employee_data)                 

@availability_bp.route('/', methods=['POST'])
def availability():
    user_id = session.get('user_id')   
    availability_logic.send_availability(user_id)

    return Response(status=204)