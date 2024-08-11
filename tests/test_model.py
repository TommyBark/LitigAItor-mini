import json

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)

from litigaitor_mini.utils import format_message_phi, load_config

with open("./tests/test_questions.json", "r") as f:
    questions = json.load(f)["Questions"]

### Model loading
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model_config = load_config("./configs/model_config.yml")

model_repo = model_config["FINETUNED_MODEL_REPO"]
original_model = model_config["ORIGINAL_MODEL_REPO"]
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)
model = AutoModelForCausalLM.from_pretrained(
    model_repo, quantization_config=bnb_config, adapter_kwargs={"revision": "main"}
)
tokenizer = AutoTokenizer.from_pretrained(original_model)
model.eval()

### Testing System prompt
system_prompt = "Answer following questions in the shortest possible way, e.g. for Yes/No questions answer with just Yes or No, for `What is 4+9?` answer with `13` etc."


def simple_qa(question:str, max_length:int=200)-> str:
    input_ids = tokenizer.encode(question, return_tensors="pt").to(device)
    output = model.generate(input_ids, max_length=max_length)
    answer = tokenizer.decode(output[0][input_ids.shape[1] :], skip_special_tokens=True)
    return answer


def test_questions():
    for question in questions:
        message = format_message_phi(question["question"], system_message=system_prompt)
        response = simple_qa(message)
        print(question)
        print(response)
        assert response == question["answer"]
