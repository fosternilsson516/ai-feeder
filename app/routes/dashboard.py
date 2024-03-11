from flask import Flask, render_template, session, Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    user_role = session.get('user_role')
    default_content = "Who What Where"
    if user_role == 'owner':
        return render_template('owner/dashboard.html', default_content=default_content)
    elif user_role == 'employee':
        return render_template('employee/dashboard.html', default_content=default_content)


    

  

    