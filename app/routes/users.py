# app/routes/user.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from werkzeug.security import generate_password_hash
from app.user_handler import Users

users_bp = Blueprint('users', __name__)
user_handler = Users()

@users_bp.route('/')
def index():
    return redirect(url_for('users.login'))

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login form submission
        email = request.form['email']
        password = request.form['password']

        auth_result = user_handler.authenticate_user(email, password)
        print(auth_result)
        if auth_result == True:
            return redirect(url_for('dashboard.dashboard'))
        else:
            # Authentication failed, display appropriate error message
            flash(auth_result, "error")
            return redirect(url_for('users.login'))
        # Render the login page for GET requests
    return render_template('login.html')

@users_bp.route('/create-account', methods=['GET', 'POST'])
def create_account():
    email_exists_message = ''
    if request.method == 'POST':
        try:
            email = request.form['email']
            phone_number = request.form['phone_number']
            password = request.form['password']
            password_match = request.form['password_match']
        except BadRequestKeyError as e:
            print("Error accessing form data:", e)
            return "An error occurred while processing the form data.", 500

        session['email'] = email
        session['phone_number'] = phone_number

        # Check if the passwords match
        if password != password_match:
            flash("Passwords do not match", "error")
            return redirect(url_for('users.create_account'))

        password_hash = generate_password_hash(password)   

        if user_handler.email_exists(email):
            email_exists_message = "Email already exists"
            flash(email_exists_message, "error")
            return redirect(url_for('users.create_account'))    

        # Proceed with registration if passwords match
        user_handler.create_account(email, phone_number, password_hash)
        return redirect(url_for('users.successful_reg'))

    # Retrieve form data from session (if available)
    email = session.pop('email', '')
    phone_number = session.pop('phone_number', '')

    return render_template('create_account.html', email=email, phone_number=phone_number)   

@users_bp.route('/successful-reg')
def successful_reg():
    return render_template('successful_reg.html')

@users_bp.route('/forgot-password')
def forgot_password():
    # Render the password recovery page
    return 'Forgot Password page'