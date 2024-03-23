from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response, current_app
from app.business_handler import Business
import os

bio_bp = Blueprint('bio', __name__)
business_handler = Business()

@bio_bp.route('/', methods=['GET'])
def bio():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login')) 
    self_bio = business_handler.get_employee_bio(user_id) 
    if self_bio:
        return render_template('employee/bio.html', self_bio=self_bio) 
    else:      
        return render_template('employee/bio.html')

@bio_bp.route('/', methods=['POST'])
def post_bio():
    user_id = session.get('user_id')
    img_file = request.files['empFileInput']
    self_bio = request.form.get('self-bio')
    img_url = None

    if img_file and img_file.filename != '':
        # Determine file extension and format
        if img_file.filename.endswith('.png'):
            file_format = 'png'
        else:
            file_format = 'jpeg'

        img_path = os.path.join(current_app.static_folder, 'img', f'headshot_{user_id}.{file_format}')
        if os.path.exists(img_path):
            # Replace the existing file
            os.remove(img_path)
        img_file.save(img_path)
        
        # Use the file path as a reference to the image
        img_url = f'app/static/img/headshot_{user_id}.{file_format}' 

        business_handler.post_employee_bio(user_id, img_url, self_bio) 
    else:
        business_handler.update_employee_bio(user_id, img_url, self_bio) 

    return Response(status=204)  

    """
            business_name = request.form['business_name']
            street_address = request.form['street_address']
            city = request.form['city']
            state = request.form['state']
            zip_code = request.form['zip_code']
            subdomain_name = request.form['subdomain_name']

            HTML:

        <label for="business_name">Name of Business:</label>
        <input type="text" id="business_name" name="business_name" required><br>
        <label for="street_address">Business Street Address:</label>
        <input type="text" id="street_address" name="street_address" required><br>
        <label for="city">City:</label>
        <input type="text" id="city" name="city" required><br>
        <label for="state">State:</label>
        <input type="text" id="state" name="state" pattern="[A-Z]{2}" title="Please enter a valid 2-letter uppercase state abbreviation" required><br>
        <label for="zip_code">Zip Code:</label>
        <input type="number" id="zip_code" name="zip_code" minlength="5" maxlength="5" title="Please enter a valid 5-number zip code" required><br>
        <label for="subdomain_name">Subdomain Name:</label>
        <input type="text" id="subdomain_name" name="subdomain_name" required><br>
            """