from transformers import pipeline, LlamaForCausalLM, LlamaTokenizerFast
import torch
from torch.quantization import quantize_dynamic
import optimum

def init_llama_pipeline():
    #quantization_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16)
    model = LlamaForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0", device_map="auto")


    # Load the state dictionary of the quantized model
    quantized_model_state_dict = torch.load("quantized_model.pth", map_location=torch.device('cpu'))
    model.load_state_dict(quantized_model_state_dict, strict=False)
    model = quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
    
    # Ensure the model is in evaluation mode
    model.eval()
    
    # Load the tokenizer
    tokenizer = LlamaTokenizerFast.from_pretrained("llama_tokenizer")

    llama_pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    #qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

    return llama_pipe

"""
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
model = LlamaForCausalLM.from_pretrained(model_name)
model.eval()
#tokenizer = LlamaTokenizerFast.from_pretrained(model_name)

quantized_model = quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
quantized_model.save_pretrained("quantized_model")

#model_path = "quantized_model.pth"
#torch.save(quantized_model.state_dict(), model_path)
#tokenizer.save_pretrained("llama_tokenizer")
"""

