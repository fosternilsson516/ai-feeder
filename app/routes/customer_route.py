from flask import render_template, Blueprint, request, Response, jsonify
from app.QA_pipeline import llama_pipe
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
        text = f"{result}"

        question = request.form['text_question']
"""           
                document = doc_store.get_all_text()
                chunks = doc_store.split_text_into_word_chunks(document, chunk_size=250)
                for chunk in chunks:
                    result = qa_pipeline(question=query, context=chunk)
                    if result['answer']:
                        answers_with_scores.append({'answer': result['answer'], 'score': result['score']})
                answers_with_scores.sort(key=lambda x: x['score'], reverse=True)  
                top_3_answers = answers_with_scores[:3]
                print(top_3_answers)
                context = ""  
                for item in top_3_answers:
                    context += f"{item['answer']}, 
"""
        prompt_text = f"Please provide an answer to the following question:\n{question}\nAnswer:"

        # Generate text with the pipeline
        outputs = llama_pipe(prompt_text, max_new_tokens=250, do_sample=True, temperature=0.7, top_k=30, top_p=0.9)


        whole_text = outputs[0]["generated_text"]
        answer = whole_text[len(prompt_text):].strip()

        return jsonify({"question": question, "answer": answer})

    return jsonify({"error": "No data found"}), 404  
