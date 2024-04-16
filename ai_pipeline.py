from transformers import pipeline, LlamaForCausalLM, LlamaTokenizerFast
import torch
from torch.profiler import profile, record_function, ProfilerActivity


def initialize_model():
    model = LlamaForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()  # Set the model to evaluation mode
    #model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
    tokenizer = LlamaTokenizerFast.from_pretrained("llama_tokenizer")


    return model, tokenizer, device
model, tokenizer, device = initialize_model()    

def generate_text(model, tokenizer, device, input_text):
    messages = [
    {"role": "system", "content": "You are a friendly chatbot who always responds to be informative"},
    {"role": "user", "content": input_text}
    ]    
    eos_token = tokenizer.eos_token
    prompt = ""
    for message in messages:
        prompt += f"{message['content']}{eos_token}\n"
    
    input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)

    #input_length = input_ids.size(-1)
    #max_length = input_length + 512
    
    with torch.no_grad():  # No gradient calculations for inference
        outputs = model.generate(
            input_ids,
            max_length=512,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            no_repeat_ngram_size=2
        )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    #trimmed_response = generated_text[len(prompt):].strip()
    return generated_text

#llama_pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)



    #return llama_pipe

"""
input_text = "Hello, how are you?"
input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    #qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
with profile(activities=[ProfilerActivity.CPU], record_shapes=True) as prof:
    with record_function("model_inference"):
        outputs = model(input_ids)  # ensure input_ids are correctly prepared

print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=10))



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

