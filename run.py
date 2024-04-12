# run.py
from ai_pipeline import init_llama_pipeline
from chat import setup_chat_interface
import webbrowser
import time
import threading

def launch_app(app):
    # Using threading to prevent blocking; waits 1 second before opening the URL
    def open_browser():
        time.sleep(1)
        webbrowser.open_new("http://127.0.0.1:7860")  # Default Gradio URL
    
    threading.Thread(target=open_browser).start()
    app.launch()

def main():
    # Initialize the AI model
    llama_pipe = init_llama_pipeline()
    
    # Setup and launch the Gradio interface
    app = setup_chat_interface(llama_pipe)
    launch_app(app)

if __name__ == "__main__":
    main()