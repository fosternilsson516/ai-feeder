from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response
from app.t5_pipe import flan_t5_pipe, prompt_dict
from app.question_handler import Questions

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
    
    #answered_questions = question_handler(user_id)
    
    return render_template('owner/setup_chat.html', next_question=next_question, question_id=question_id)

@setup_chat_bp.route('/', methods=['POST'])
def submit_answer():
    user_id = session.get('user_id')
    if user_id:
        answer_text = request.form['answer']
        question_id = request.form['question_id']

        question_handler.save_text_answer(user_id, question_id, answer_text)

        if question_id in prompt_dict:
            prompt = prompt_dict[question_id] + answer_text
            response = flan_t5_pipe(prompt, max_length=200)[0]['generated_text']
            
            if question_id == "1":
                print(response)
                
                pass
            elif question_id == "2":
                
                pass
            elif question_id == "3":
                
                pass
            elif question_id == "4":
                
                pass

        
    else:
        flash('You need to be logged in to submit answers.', 'error')
    return redirect(url_for('setup_chat.get_setup_chat'))