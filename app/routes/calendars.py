from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response
from app.user_handler import Users
import calendar
from datetime import datetime

calendar_bp = Blueprint('calendars', __name__)
user_handler = Users()

@calendar_bp.route('/', methods=['GET'])
def get_calendar(month=None, year=None):
    # Check if the user is logged in
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))

    # Get the current year and month if not provided
    if year is None or month is None:
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month  

    # Generate the calendar for the specified month and year
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]  

    return render_template('calendar.html', calendar=cal, current_month=month_name, current_year=year)  

@calendar_bp.route('/update_calendar', methods=['GET'])
def update_calendar(): 
    current_month = request.args.get('month', type=str)
    current_year = request.args.get('year', type=int)
    direction = request.args.get('direction', type=str)  

    
    
    month = list(calendar.month_name).index(current_month) 

    direction = request.args.get('direction')
    if direction == 'prev':
        # Go to previous month
        month -= 1
        if month == 0:
            month = 12
            current_year -= 1
    elif direction == 'next':
        # Go to next month
        month += 1
        if month == 13:
            month = 1
            current_year += 1    

    # Generate the calendar for the specified month and year
    cal = calendar.monthcalendar(current_year, month)
    updated_month = calendar.month_name[month]     

    return render_template('calendar.html', calendar=cal, current_month=updated_month, current_year=current_year)

@calendar_bp.route('/', methods=['POST'])
def calendar_post():
    # Check if the user is logged in
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
    
    return Response(status=204) 