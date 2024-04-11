from transformers import pipeline, LlamaForCausalLM, LlamaTokenizerFast
import torch
from torch.quantization import quantize_dynamic

def init_qa_pipeline():
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    model = LlamaForCausalLM.from_pretrained(model_name)
    quantized_model = quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)

    # Load the tokenizer
    tokenizer = LlamaTokenizerFast.from_pretrained(model_name)

    llama_pipe = pipeline("text-generation", model=quantized_model, tokenizer=tokenizer, torch_dtype=torch.bfloat16, device_map="auto")
    qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

    return llama_pipe, qa_pipeline
# Initialize the text generation pipeline
llama_pipe, qa_pipeline = init_qa_pipeline()

"""
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
model = LlamaForCausalLM.from_pretrained(model_name)
model.eval()
tokenizer = LlamaTokenizerFast.from_pretrained(model_name)

quantized_model = quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)

model_path = "quantized_model.pth"
torch.save(quantized_model.state_dict(), model_path)
"""


