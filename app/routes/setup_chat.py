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
        text = ''
    
    return render_template('owner/setup_chat.html', text=text)

@setup_chat_bp.route('/', methods=['POST'])
def submit_answer():
    user_id = session.get('user_id')
    if not user_id:
        # If user is not authenticated, redirect to login
        return redirect(url_for('users.login'))

    text = request.form.get('answer', '')  # Safely get 'answer' from form data; default to empty string if missing
    word_count = len(text.split())

    # Check if the word count exceeds the limit
    if word_count > 10000:
        # Handle the case where the word limit is exceeded
        # Return an error message to the user as a JSON response
        return jsonify({"error": f"Word limit of 10,000 exceeded, please delete some of the text. Total word count: {word_count}"}), 400
    
    # Proceed to save the response if the word limit is not exceeded
    url_setup.save_response(user_id, text)
    return Response(status=200)       
