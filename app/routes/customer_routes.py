from flask import render_template, Blueprint, request, Response, jsonify
from app.availability_handler import Availability
from app.gpt_neo import qa_pipeline
from app.query_calendar import googleCalendar
import torch
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

customer_routes_bp = Blueprint('customer_routes', __name__, subdomain='<subdomain>')
availability_handler = Availability()
query_calendar = googleCalendar()


@customer_routes_bp.route('/', subdomain="<subdomain>")
def customer_route_messages(subdomain):

    
    return render_template("customer/messages.html", subdomain=subdomain)   

def parse_time_keywords(question):
    # Lowercase the question for easier matching
    question = question.lower()
    
    # Check for time-related keywords
    if "week" in question:
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=7)
    elif "month" in question:
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=30)
    elif any(month in question for month in ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]):
        current_year = datetime.now().year
        month_number = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
                        "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}
        for month, number in month_number.items():
            if month in question:
                start_date = datetime(current_year, number, 1)
                if number == 12:
                    end_date = datetime(current_year + 1, 1, 1) - timedelta(days=1)  # End of December
                else:
                    end_date = datetime(current_year, number + 1, 1) - timedelta(days=1)
                break
    else:
        # Default to week if no specific time frame is mentioned
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=7)
        
    return start_date, end_date  

def query_google_calendar_freebusy(calendar_ids, user_id, service, start_date, end_date):
    service = query_calendar.get_google_service(user_id)
    body = {
    "timeMin": start_date.isoformat() + 'Z',  # 'Z' indicates UTC time
    "timeMax": end_date.isoformat() + 'Z',
    "items": [{"id": calendar_id} for calendar_id in calendar_ids]
    }
    eventsResult = service.freebusy().query(body=body).execute()
    return eventsResult 

def format_freebusy_info(freebusy_info, time_zone):
    formatted_info = []

    # Convert user_time_zone to a ZoneInfo object
    user_tz = ZoneInfo(user_time_zone)

    for calendar_id, info in freebusy_info['calendars'].items():
        for busy_period in info.get('busy', []):
            start_utc = datetime.fromisoformat(busy_period['start'].rstrip('Z'))
            end_utc = datetime.fromisoformat(busy_period['end'].rstrip('Z'))

            # Convert start and end times to user's local time zone
            start_local = start_utc.replace(tzinfo=ZoneInfo('UTC')).astimezone(user_tz)
            end_local = end_utc.replace(tzinfo=ZoneInfo('UTC')).astimezone(user_tz)

            formatted_info.append({
                'calendar_id': calendar_id,
                'start': start_local.strftime('%Y-%m-%d %H:%M:%S'),
                'end': end_local.strftime('%Y-%m-%d %H:%M:%S')
            })

    return formatted_info          

@customer_routes_bp.route('/', subdomain="<subdomain>", methods=['POST'])
def post_message(subdomain):
    result = availability_handler.get_owner_data(subdomain)
    if result:
        user_id, time_zone, access_token, refresh_token, token_uri, client_id, client_secret, scopes, availability, calendar_ids, service_text, special_instructions, business_address = result
        context = f"service text:{service_text}. special instructions:{special_instructions}. address:{business_address}."
        question = request.form['answer']
        if question:
            start_date, end_date = parse_time_keywords(question)
            service = query_calendar.get_google_service(user_id)
            freebusy_info = query_google_calendar_freebusy(calendar_ids, user_id, service, start_date, end_date)
            formatted_freebusy_info = format_freebusy_info(freebusy_info, time_zone)
            return jsonify({"availability": formatted_freebusy_info})
        else:    
            prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"


            qa_input = {
                "question": question,
                "context": context
            }

            # Correct usage of the question-answering pipeline
            generated_results = qa_pipeline(qa_input)
            answer = generated_results['answer']

            return jsonify({"question": question, "answer": answer})

    return jsonify({"error": "No data found"}), 404  
