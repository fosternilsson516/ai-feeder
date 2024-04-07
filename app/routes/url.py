from flask import Flask, render_template, redirect, url_for, session, Blueprint, request, jsonify, Response
from app.url_setup import URLSetup
import os


url_bp = Blueprint('url', __name__)

url_setup = URLSetup()

@url_bp.route('/', methods=['GET'])
def get_url():
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))     
    subdirectory = url_setup.get_subdirectory(user_id)
    if subdirectory:
        full_url = f"https://ployease.com/me/{subdirectory}"
    else:
        full_url = '' 

    return render_template('owner/url.html', full_url=full_url) 

@url_bp.route('/', methods=['POST'])
def post_subdirectory():

    user_id = session.get('user_id')
    subdirectory = request.form['answer']

    result = url_setup.save_subdirectory(user_id, subdirectory)
    if "error" in result:
        # Return a JSON response with the error message
        return jsonify({"error": result["error"]}), 400
    elif "success" in result:
        # Return a JSON response with the success message
        return Response(status=200)    


  