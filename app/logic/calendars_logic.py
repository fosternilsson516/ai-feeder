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
            print(current_date)
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

    def switch_month(self):
        current_month = request.args.get('month', type=str)
        current_year = request.args.get('year', type=int)
        direction = request.args.get('direction', type=str)  
        month = list(calendar.month_name).index(current_month) 
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
        return cal, updated_month, current_year   