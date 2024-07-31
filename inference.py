import os

import torch
import yaml
from huggingface_hub import HfApi
from peft import AutoPeftModelForCausalLM
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainerCallback,
    TrainingArguments,
)
from utils import load_config

device = "cuda:0" if torch.cuda.is_available() else "cpu"
config = load_config("./configs/model_config.yml")

model_repo = config["FINETUNED_MODEL_REPO"]
original_model = config["ORIGINAL_MODEL_REPO"]

model = AutoPeftModelForCausalLM.from_pretrained(model_repo).to(device)
tokenizer = AutoTokenizer.from_pretrained(original_model)
model.eval()

def simple_completion(text, max_length=100):
    input_ids = tokenizer.encode(text, return_tensors="pt").to(device)
    output = model.generate(input_ids, max_length=max_length)
    return tokenizer.decode(output[0], skip_special_tokens=True)


print(simple_completion("The weather is nice today, I think I will go for a walk."))
print(simple_completion("My wife is a"))
