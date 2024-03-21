import calendar
from datetime import datetime
from flask import request

class calendarLogic:
    def current_calendar(self):
        # Get the current year and month if not provided
        month = request.args.get('month', type=str)
        year = request.args.get('year', type=int)
        direction = request.args.get('direction', type=str)
        if year is None or month is None:
            current_date = datetime.now()
            year = current_date.year
            month = current_date.month  

        # Generate the calendar for the specified month and year
            cal = calendar.monthcalendar(year, month)
            month_name = calendar.month_name[month]
        if direction is not None: 
            month = list(calendar.month_name).index(month) 
            if direction == 'prev':
                # Go to previous month
                month -= 1
                if month == 0:
                    month = 12
                    year -= 1
            elif direction == 'next':
                # Go to next month
                month += 1
                if month == 13:
                    month = 1
                    year += 1    
            # Generate the calendar for the specified month and year
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month] 
        return cal, month_name, year

    def process_availability(self, avail):
        hours_by_day = {}

        for day, schedule in avail.items():
            if schedule == 'Not available':
                hours_by_day[day] = []
            else:
                start_time, end_time = schedule.split(' - ')
                start_hour, start_minute = map(int, start_time.split(':'))
                end_hour, end_minute = map(int, end_time.split(':'))
                
                hours = []
                for hour in range(start_hour, end_hour + 1):
                    if hour == 0:
                        hours.append(f"12:00 AM")
                    elif hour < 12:
                        hours.append(f"{hour:02d}:00 AM")
                    elif hour == 12:
                        hours.append(f"12:00 PM")
                    else:
                        hours.append(f"{hour - 12:02d}:00 PM")
                    
                hours_by_day[day] = hours

        return hours_by_day 
