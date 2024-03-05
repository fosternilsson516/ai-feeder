    requested_month = request.args.get('month')
    requested_year = request.args.get('year')    

    # Get current month and year
    current_date = datetime.now()

    if requested_month and requested_year:
        # Convert month name to month number
        current_month = datetime.strptime(requested_month, "%B").month
        current_year = int(requested_year)
    else:
        current_month = current_date.month
        current_year = current_date.year    

    # Get the previous and next months
    prev_month_date = (current_date.replace(month=current_month, year=current_year) - timedelta(days=1)).replace(day=1)
    next_month_date = (current_date.replace(month=current_month, year=current_year) + timedelta(days=32)).replace(day=1) 

        # Get the current month and year
        # Get the previous and next months
    previous_month = prev_month_date.strftime('%B')
    next_month = next_month_date.strftime('%B')

    # Set the start date to the first day of the current month
    start_date = current_date.replace(month=current_month, year=current_year, day=1)

    # Get the number of days in the current month
    next_month = (start_date + timedelta(days=32)).replace(day=1)
    days_in_month = (next_month - start_date).days

    # Initialize an empty list to store the calendar structure
    calendar = []

    # Initialize variables to keep track of the current date and week
    current_date = start_date
    current_week = []

    # Calculate the offset for the first day of the month
    offset = (start_date.weekday() + 1) % 7  # Offset by one day

    # Add empty slots for the days before the first day of the month
    current_week.extend([''] * offset)

    # Loop through all days in March 2024
    while start_date.month == current_date.month:  # Loop until we reach the next month
        # Add the current date to the current week
        current_week.append(current_date.day)

        # Move to the next day
        current_date += timedelta(days=1)

        # If the current day is the last day of the week, add the current week to the calendar and start a new week
        if current_date.weekday() == 6:
            calendar.append(current_week)
            current_week = []
    if current_week:
        calendar.append(current_week)        
    print(calendar)   