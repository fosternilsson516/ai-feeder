import gradio as gr
import torch

def setup_chat_interface(llama_pipe):
    def respond(message, chat_history):
        query = message
        messages = [
            {
                "role": "system",
                "content": "You are a friendly chatbot who always responds to be informative.",
            },
            {"role": "user", "content": f"{query}"},
        ]

        prompt = llama_pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        outputs = llama_pipe(prompt, max_new_tokens=300, do_sample=True, temperature=0.7, top_k=30, top_p=0.9)
        whole_text = outputs[0]["generated_text"]
        bot_message = whole_text[len(prompt):].strip()
        chat_history.append((message, bot_message))
        return "", chat_history

    with gr.Blocks() as app:
        with gr.Column():  
            gr.Markdown("### Chat")
            chatbot = gr.Chatbot(label="Chatbot", placeholder="Messages will appear here...", height=600)
            msg = gr.Textbox(label="Your Question", placeholder="Type your questions here...") 

            msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])    

    return app


