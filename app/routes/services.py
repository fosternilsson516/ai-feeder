from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response
from app.services_handler import Services

services_bp = Blueprint('services', __name__)
services_handler = Services()

@services_bp.route('/', methods=['GET'])
def services():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))

    price_type_mapping = {
            'per_hour': 'Hourly',
            'per_service': 'Per Service'
        }    

    services_data = services_handler.get_services(user_id)
    if services_data[0] == True:
        print(services_data[1])
        _, _, service_names, prices, price_types = services_data[1]

        formatted_service_list = []

        # Convert Decimal prices to string and strip the trailing zeroes
        price_strings = [str(price).rstrip('0').rstrip('.') for price in prices]
        price_types_list = price_types.strip("{}").split(",")
        
        # Construct string representations of each service
        service_strings = []
        for name, price, price_type in zip(service_names, price_strings, price_types_list):
            display_price_type = price_type_mapping.get(price_type, price_type)
            service_strings.append(f"{name}: {display_price_type} - ${price}")

        # Join the formatted service list with newline characters
        formatted_service_data = "\n".join(service_strings)
    else:
        formatted_service_data = ''    


    return render_template('owner/services.html', formatted_service_data=formatted_service_data)   

@services_bp.route('/', methods=['POST'])
def post_services():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
    service_list = request.form.get('service-list')
    rows = service_list.split('\n')

    service_names = []
    service_types = []
    prices = []
    type_mapping = {
    "Hourly": "per_hour",
    "Per Service": "per_service"
    }

    for row in rows:
        try:
            service_name, other_details = row.split(": ", 1)
            service_type, price = other_details.split(" - $")
            mapped_type = type_mapping.get(service_type, service_type)

            # Append the values to their respective lists
            service_names.append(service_name)
            service_types.append(mapped_type)
            prices.append(price)
        except ValueError as e:

            print("Not An Error:", e)
        # Assuming service_names is a list of strings
    service_n_array = "{" + ", ".join(f'"{name}"' for name in service_names) + "}"
    service_t_array = "{" + ",".join(service_types) + "}"
    price_literals = [str(price) for price in prices]
    postgresql_prices_array = "{" + ",".join(price_literals) + "}"

    services_data = services_handler.get_services(user_id)
    if services_data[0] == True:
        services_handler.update_services(user_id, service_n_array, service_t_array, postgresql_prices_array)
    else:    
        services_handler.save_services(user_id, service_n_array, service_t_array, postgresql_prices_array)

    return Response(status=204)