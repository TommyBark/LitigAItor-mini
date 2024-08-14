import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)

from litigaitor_mini.utils import load_model_and_tokenizer

model, tokenizer, device = load_model_and_tokenizer(
    config_path="../configs/model_config.yml"
)
model.eval()

# model.disable_adapters()


def simple_completion(text: str, max_length: int = 100) -> str:
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
