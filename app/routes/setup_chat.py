from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response
from app.url_setup import URLSetup
import json

setup_chat_bp = Blueprint('setup_chat', __name__)
url_setup = URLSetup()

@setup_chat_bp.route('/', methods=['GET'])
def get_setup_chat():
    # Check if the user is logged in
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
        
    text = url_setup.get_response(user_id)
    if text is None:
        text = []
    
    return render_template('owner/setup_chat.html', text=text)

@setup_chat_bp.route('/', methods=['POST'])
def submit_answer():
    user_id = session.get('user_id')
    if user_id:
        text = request.form['answer']     
        url_setup.save_response(user_id, text) 
    else:
        redirect(url_for('users.login'))   
    return Response(status=200)        
