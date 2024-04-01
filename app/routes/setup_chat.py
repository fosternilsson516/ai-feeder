from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response
from app.question_handler import Questions
import json

setup_chat_bp = Blueprint('setup_chat', __name__)
question_handler = Questions()

@setup_chat_bp.route('/', methods=['GET'])
def get_setup_chat():
    # Check if the user is logged in
    user_id = session.get('user_id')
    if user_id is None:
        # Redirect the user to the login page
        return redirect(url_for('users.login'))
        
    result = question_handler.get_next_question(user_id)
    if result:
        next_question = result[0]
        question_id = result[1]
    if question_id == 5:
        question_id = []    

    answered_questions = question_handler.get_answers(user_id)
    if answered_questions is None:
        answered_questions = []
    
    return render_template('owner/setup_chat.html', next_question=next_question, question_id=question_id, answered_questions=answered_questions)

@setup_chat_bp.route('/', methods=['POST'])
def submit_answer():
    user_id = session.get('user_id')
    if user_id:
        answer_text = request.form['answer']
        question_id = request.form['question_id']
            
        if question_id == "1":
            service_text = answer_text     

            question_handler.save_first_question(user_id, service_text)
            
            pass
        elif question_id == "2":
            special_instructions = answer_text       

            question_handler.save_second_question(user_id, special_instructions)
            
            pass
        elif question_id == "3":
            business_address = answer_text       

            question_handler.save_third_question(user_id, business_address)
            pass
        elif question_id == "4":
            subdomain = answer_text       

            result = question_handler.save_fourth_question(user_id, subdomain)

            if "error" in result:
                # If there was an error, flash the error message
                flash(result["error"])  # Second argument 'error' is an optional category
            elif "success" in result:
                # If successful, flash the success message
                flash(result["success"]) 
            
            return Response(status=409)
        elif question_id == "5":
         
            return redirect(url_for('dashboard.dashboard')) 
              
    else:
        flash('You need to be logged in to submit answers.', 'error')
    question_handler.save_text_answer(user_id, question_id, answer_text)    
    return Response(status=204)