# This is your app/t5_pipe.py module or similar
from transformers import pipeline
import json

def init_flan_t5():
  return pipeline("text2text-generation", model="google/flan-t5-base")

flan_t5_pipe = init_flan_t5()

prompt_dict = {
  "1": "Extract the service name, time and price from the given sentence, put service name as is, if {time} is given in hours convert it to mins example: 1 hour = 60 mins and convert {price} to a dollar amount like this 150 = $150.00. |",
  "2": "Extract either an 'A' or 'B'. | ",
  "3": "Extract {day, start-time, stop-time}. convert to military time. | ",
  "4": "Extract 'text' and/or 'email' and either 'A', 'B', 'C', or 'D'. | "
}

