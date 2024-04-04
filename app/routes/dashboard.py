from flask import Flask, render_template, session, Blueprint, redirect

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))    
    return render_template('owner/dashboard.html')



    

  

    