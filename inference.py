import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)

from utils import load_config

device = "cuda:0" if torch.cuda.is_available() else "cpu"
config = load_config("./configs/model_config.yml")

model_repo = config["FINETUNED_MODEL_REPO"]
original_model = config["ORIGINAL_MODEL_REPO"]


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

#model.disable_adapters()


def simple_completion(text, max_length=100):
    input_ids = tokenizer.encode(text, return_tensors="pt").to(device)
    output = model.generate(input_ids, max_length=max_length)
    return tokenizer.decode(output[0], skip_special_tokens=False)


print(
    simple_completion(
        "<|user|>The weather is nice today, I think I will go for a walk. Respond in one short sentence.<|end|><|assistant|>"
    )
)
print(
    simple_completion(
        "\n<|user|>The weather is nice today, I think I will go for a walk.<|end|>\n<|assistant|>"
    )
)
print(
    simple_completion(
        "\n<|user|>\nThe weather is nice today, I think I will go for a walk.<|end|>\n<|assistant|>\n"
    )
)

print(simple_completion("My wife is a"))
