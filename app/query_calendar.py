import re
from app.availability_handler import Availability
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

availability_handler = Availability()

class googleCalendar:
    def get_google_service(self, user_id):
        credentials_dict = availability_handler.get_user_credentials(user_id)
        credentials = Credentials(**credentials_dict)
        service = build('calendar', 'v3', credentials=credentials)
        return service

