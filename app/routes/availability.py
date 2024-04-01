from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response, current_app
from app.logic.availability_logic import availabilityLogic
from app.availability_handler import Availability
from google_auth_oauthlib.flow import Flow
from app.db import client_config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.query_calendar import googleCalendar
import os

# Allow OAuthlib to utilize insecure transport (HTTP) for development purposes
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

availability_bp = Blueprint('availability', __name__)
availability_logic = availabilityLogic()
availability_handler = Availability()
query_calendar = googleCalendar()

@availability_bp.route('/', methods=['GET'])
def get_availability():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))   

    availability_by_day = availability_logic.load_availability(user_id)

    return render_template('owner/availability.html', availability_by_day=availability_by_day)                 

@availability_bp.route('/', methods=['POST'])
def availability():
    user_id = session.get('user_id')   
    availability_logic.send_availability(user_id)

    return Response(status=204)
def get_google_oauth_flow():
    redirect_uri = url_for('availability.oauth2callback', _external=True)
    flow = Flow.from_client_config(
        client_config=client_config,
        scopes=['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar.readonly'],
        # Make sure the redirect_uri is dynamically assigned based on your Flask app routing
        redirect_uri=redirect_uri
    )
    return flow         

@availability_bp.route('/authorize')
def authorize():
    flow = get_google_oauth_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    session['state'] = state
    return redirect(authorization_url)

@availability_bp.route('/oauth2callback')
def oauth2callback():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
    flow = get_google_oauth_flow()
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    availability_handler.save_user_credentials(
        user_id=user_id,
        access_token=flow.credentials.token,
        refresh_token=flow.credentials.refresh_token,
        token_uri=flow.credentials.token_uri,
        client_id=client_config['installed']['client_id'],  # Adjust based on your actual config structure
        client_secret=client_config['installed']['client_secret'],  # Ditto
        scopes= ' '.join(flow.credentials.scopes)
    )

    return redirect(url_for('availability.view_calendars')) 

@availability_bp.route('/view_calendars')
def view_calendars():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('users.login'))  # Redirect to login if not authenticated


    service = query_calendar.get_google_service(user_id)
    calendars = list_user_calendars(service)
   

    # Render a template, passing the calendars for display
    return render_template('owner/successful_conn.html', calendars=calendars)

@availability_bp.route('/post_calendar_selection', methods=['POST'])
def post_calendar_selection():
    user_id = session.get('user_id')
    calendar_id = request.form.getlist('calendar_ids')
    service = query_calendar.get_google_service(user_id) 
    time_zone = get_user_calendar_timezone(service, calendar_id) 
    print(time_zone)
    availability_handler.save_cal_info(user_id, calendar_ids, time_zone)
    return redirect(url_for('dashboard.dashboard'))

def get_user_calendar_timezone(service, calendar_id):
    calendar = service.calendars().get(calendarId=calendar_id).execute()
    return calendar['timeZone']    

def list_user_calendars(service):
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])
    return calendars                  
     