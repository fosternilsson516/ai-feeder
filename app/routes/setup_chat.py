from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, jsonify, Response
#from app.t5_pipe import flan_t5_pipe, prompt_dict
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
    if question_id == 10:
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
            lines = answer_text.split("\n")

            service_names = []
            times = []
            prices = []

            # Step 3: Iterate over the lines
            for line in lines:
                # Step 4: Split by comma and strip to clean spaces
                parts = [part.strip() for part in line.split(",")]
                
                service_name = parts[0]
                time = parts[1]
                price = parts[2]
                
                # Append values to their respective lists
                service_names.append(service_name)
                times.append(time)
                prices.append(price)

                question_handler.save_first_question(user_id, service_names, times, prices)
            
            pass
        elif question_id == "2":
            #query to set reminders
            
            pass
        elif question_id == "3":
            #query to set name of business
            
            pass
        elif question_id == "4":
            #query to set street address
            
            pass
        elif question_id == "5":
            #query to set city
            
            pass
        elif question_id == "6":
            #query to set state
            
            pass
        elif question_id == "7":
            #query to set zip
            
            pass 
        elif question_id == "8":
            #query to set bio
            
            pass
        elif question_id == "9":
            #query to set subdomain
            
            pass
        elif question_id == "10":
            
            return redirect(url_for('dashboard.dashboard')) 
            
            
                  
    else:
        flash('You need to be logged in to submit answers.', 'error')
    question_handler.save_text_answer(user_id, question_id, answer_text)    
    return redirect(url_for('dashboard.dashboard'))