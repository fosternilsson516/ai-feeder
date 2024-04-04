from transformers import pipeline
import torch


def init_qa_pipeline():

    qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
    t5_pipeline = pipeline("text2text-generation", model="google/flan-t5-small", framework="pt")

    return qa_pipeline, t5_pipeline
# Initialize the text generation pipeline
qa_pipeline, t5_pipeline = init_qa_pipeline()
