from flask import Flask, render_template, session, Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', subdomain='<subdomain>')
def dashboard(subdomain):
    business_customization = query_database_for.business_main_page(subdomain)
    default_content = "Who What Where"
    return render_template("customer/dashboard.html", business_customization)

    ######create options for owner to customize a main page and show services and employees on the main page. 
    ######the employees should have the option to upload a bio and picture. get services ented by each employee and render them with their picture. 
    ######the user can then select an employee which will take them to their availability calendar and show their picture and bio at the top
    ######add a box for the user to select a service when selecting time for appointment.


### each employee will get a subdirectory that a user can go straight to or they can start on the main page and the subdirectory will be filled dynamically.
@app.route('/<subdirectory>/')
def subdirectory():
    return 'This is a subdirectory'    