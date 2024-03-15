from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response
from app.logic.calendars_logic import calendarLogic

calendar_bp = Blueprint('calendars', __name__)
calendars_logic = calendarLogic()

@calendar_bp.route('/', methods=['GET'])
def get_calendar():
    # Check if the user is logged in
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
    user_role = session.get('user_role')    
    if user_role == 'owner':

        cal, month_name, year = calendars_logic.current_calendar() 

        return render_template('owner/calendar.html', calendar=cal, month_name=month_name, year=year)
    elif user_role == 'employee': 

        cal, month_name, year = calendars_logic.current_calendar()

        return render_template('employee/calendar.html', calendar=cal, month_name=month_name, year=year)

@calendar_bp.route('/', methods=['POST'])
def calendar_post():
    # Check if the user is logged in
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
    
    return Response(status=204) 