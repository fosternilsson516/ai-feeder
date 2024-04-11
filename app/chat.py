import gradio as gr
#import os
#import pandas
#from docx import Document
#from qdrant import Qdrant
#from doc_store import DocumentStorage
from QA_pipeline import llama_pipe
import torch

#qdrant = Qdrant()
#doc_store = DocumentStorage()
"""
def process_file_contents(file_path):  # Change to accept a single file path
    _, file_extension = os.path.splitext(file_path)

    try:
        if file_extension.lower() == '.xlsx':
            df = pd.read_excel(file_path)
            text = df.to_string()
        elif file_extension.lower() == '.docx':
            doc = Document(file_path)
            text = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
        elif file_extension.lower() in ['.txt', '.md', '.rtf', '.csv', '.json', '.xml', '.html', '.py', '.js', '.css', '.log', '.html', '.java', '.sh', '.bat', '.ps1', '.yaml', '.yml', '.ini', '.env', '.cfg', '.doc']:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        else:
            print(f"Skipping non-supported file: {file_path}")
            return  # No need to continue processing

        #sentences = qdrant.sentence_seg(text)
        #qdrant.qdrant_input(sentences)
        doc_store.store_doc(text)

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_directory_contents(file_paths):
    # Get list of filenames in the directory
    for file_path in file_paths:
        _, file_extension = os.path.splitext(file_path)
        
        try:
            if file_extension.lower() == '.xlsx':
                df = pd.read_excel(file_path)
                text = df.to_string()
            elif file_extension.lower() == '.docx':
                doc = Document(file_path)
                text = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
            elif file_extension.lower() in ['.txt', '.md', '.rtf', '.csv', '.json', '.xml', '.html', '.py', '.js', '.css', '.log', '.html', '.java', '.sh', '.bat', '.ps1', '.yaml', '.yml', '.ini', '.env', '.cfg', '.doc']:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
            else:
                print(f"Skipping non-supported file: {file_path}")
                continue  # Move to the next file without calling qdrant_input
            #sentences = qdrant.sentence_seg(text)
            #qdrant.qdrant_input(sentences)  # Call after text is successfully extracted
            doc_store.store_doc(text)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")



    with gr.Row():
        with gr.Column(scale=2):  # This column takes up 1/4 of the space (since total scale is 8 by default)
            gr.Markdown("### Upload a directory or a single file")
            # Set up the directory uploader
            directory_uploader = gr.File(
                label="Select directory",
                file_count='directory',  # Allows the user to upload all files in a selected directory
                type='filepath',  # Files are passed to the function as bytes
            )
            file_uploader = gr.File(
                label="Select file",
                file_count='single',  # Allows the user to upload all files in a selected directory
                type='filepath',  # Files are passed to the function as bytes
            )    

            # Link the uploader to the processing function without specifying an output component
            directory_uploader.change(fn=process_directory_contents, inputs=directory_uploader)
            file_uploader.change(fn=process_file_contents, inputs=file_uploader)
"""   

def respond(message, chat_history):
    answers_with_scores = []
    query = message

    messages = [
        {
            "role": "system",
            "content": "You are a friendly chatbot who always responds to be informative.",
        },
        {"role": "user", "content": f"{query}"},
    ]

    prompt = llama_pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = llama_pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=30, top_p=0.9)
    whole_text = outputs[0]["generated_text"]
    bot_message = whole_text[len(prompt):].strip()
    chat_history.append((message, bot_message))
    return "", chat_history

with gr.Blocks() as app:
    with gr.Column():  
        gr.Markdown("### Chat")
        chatbot = gr.Chatbot(label="Chatbot", placeholder="Messages will appear here...")
        msg = gr.Textbox(label="Your Question", placeholder="Type your questions here...") 

        msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])    

app.launch()


