from transformers import pipeline
import torch

def init_qa_pipeline():

    
    # Initialize the pipeline for text generation
    qa_pipeline = pipeline("question-answering", model='distilbert-base-uncased-distilled-squad')
    return qa_pipeline

# Initialize the text generation pipeline
qa_pipeline = init_qa_pipeline()
