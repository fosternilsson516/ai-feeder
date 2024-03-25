# This is your app/t5_pipe.py module or similar
"""
from transformers import pipeline
import json

def init_flan_t5():
  return pipeline("text2text-generation", model="google/flan-t5-base")


flan_t5_pipe = init_flan_t5()

prompt_dict = {
  "1": "Extract the service name, time and price from the following sentence. |",
  "2": "Extract either an 'A' or 'B'. | ",
  "3": "Extract {day, start-time, stop-time}. convert to military time. | ",
  "4": "Extract 'text' and/or 'email' and either 'A', 'B', 'C', or 'D'. | "
}
"""
