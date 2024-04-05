from flask import render_template, Blueprint, request, Response, jsonify
from app.QA_pipeline import qa_pipeline, t5_pipeline
from app.url_setup import URLSetup
import torch

customer_route_bp = Blueprint('customer_route', __name__)
url_setup = URLSetup()

@customer_route_bp.route('/<subdirectory>')
def customer_route_messages(subdirectory):
    if subdirectory:
        return render_template("customer/messages.html", subdirectory=subdirectory)
    else:
        return jsonify({"error": "Subdirectoy does not exist"}), 404    

def split_text_into_word_chunks(text, chunk_size=100):
    # Split the text into words
    words = text.split()
    
    # Split words into chunks of `chunk_size`
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    
    return chunks    

@customer_route_bp.route('/<subdirectory>', methods=['POST'])
def post_message(subdirectory):
    result = url_setup.get_owner_data(subdirectory)
    if result:
        answers_with_scores = []
        text = f"{result}"
        chunks = split_text_into_word_chunks(text, chunk_size=100)
        for chunk in chunks:

            question = request.form['text_question']

            # Correct usage of the question-answering pipeline
            result = qa_pipeline(question=question, context=chunk)
            if result['answer']:

                answers_with_scores.append({'answer': result['answer'], 'score': result['score']})
        answers_with_scores.sort(key=lambda x: x['score'], reverse=True) 
        top_5_answers = answers_with_scores[:5]
        prompt_intro = f"write a sentence for this question: {question} that use the following higher scoring keywords coherently:\n" 
        prompt_body = ""  
            #score_description = "High" if item['score'] > 0.6 else "High-Medium" if item['score'] > 0.4 else "Medium-Low" if item['score'] > 2 else "Low"
        for item in top_5_answers:
            prompt_body += f"keywords:{item['answer']}, score:{item['score']}\n"

        prompt = prompt_intro + prompt_body

        # Now, feed this concatenated text into the summarization pipeline
        generated_results = t5_pipeline(prompt, max_length=150, min_length=5)  # Adjust max_length as needed
        answer = generated_results[0]['generated_text']  

        return jsonify({"question": question, "answer": answer})

    return jsonify({"error": "No data found"}), 404  


