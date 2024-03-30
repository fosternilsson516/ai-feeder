from flask import render_template, Blueprint, request, Response
from app.availability_handler import Availability
from app.gpt_neo import qa_pipeline
import torch

customer_routes_bp = Blueprint('customer_routes', __name__, subdomain='<subdomain>')
availability_handler = Availability()


@customer_routes_bp.route('/', subdomain="<subdomain>")
def customer_route_messages(subdomain):

    
    return render_template("customer/messages.html", subdomain=subdomain)

@customer_routes_bp.route('/', subdomain="<subdomain>", methods=['POST'])
def post_message(subdomain):
    result = availability_handler.get_owner_data(subdomain)
    if result:
        owner_id, availability, calendar_ids, service_text, special_instructions, business_address = result
        context = f"service text:{service_text}. special instructions:{special_instructions}. address:{business_address}."
        question = request.form['answer']
        prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"


        qa_input = {
            "question": question,
            "context": context
        }

        # Correct usage of the question-answering pipeline
        generated_results = qa_pipeline(qa_input)
        print(generated_results['answer'])

    
    return Response(status=204)  
