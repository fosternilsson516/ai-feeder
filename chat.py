import gradio as gr
from ai_pipeline import initialize_model, generate_text

def respond(message, chat_history):
    input_text = message

    bot_message = generate_text(model, tokenizer, device, input_text)
    chat_history.append((message, bot_message))
    return "", chat_history

with gr.Blocks() as app:
    with gr.Column():  
        gr.Markdown("### Chat")
        chatbot = gr.Chatbot(label="Chatbot", placeholder="Messages will appear here...", height=600)
        msg = gr.Textbox(label="Your Question", placeholder="Type your questions here...") 

        msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])    

app.launch()


