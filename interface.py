from threading import Thread

import gradio as gr
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    StoppingCriteria,
    StoppingCriteriaList,
    TextIteratorStreamer,
)

from utils import load_config

device = "cuda:0" if torch.cuda.is_available() else "cpu"
config = load_config("./configs/model_config.yml")

model_repo = config["FINETUNED_MODEL_REPO"]
original_model = config["ORIGINAL_MODEL_REPO"]
system_message = config["SYSTEM_MESSAGE"]

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
# model.disable_adapters()


class StopOnTokens(StoppingCriteria):
    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
    ) -> bool:
        stop_ids = [29, 0, 32007]
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False


def predict(message, history):
    print(history)
    history_transformer_format = history + [[message, ""]]
    stop = StopOnTokens()

    messages = "".join(
        [
            "".join(
                ["\n<|user|>\n" + item[0] + "<|end|>", "\n<|assistant|>\n" + item[1]]
            )
            for item in history_transformer_format
        ]
    )
    messages = f"<|system|>\n{system_message}<|end|>" + messages

    with open("messages.txt", "w") as f:
        f.write(messages)

    model_inputs = tokenizer([messages], return_tensors="pt").to(device)
    streamer = TextIteratorStreamer(
        tokenizer, timeout=10.0, skip_prompt=True, skip_special_tokens=True
    )
    generate_kwargs = dict(
        model_inputs,
        streamer=streamer,
        max_new_tokens=1024,
        do_sample=True,
        top_p=0.95,
        top_k=1000,
        temperature=1.0,
        num_beams=1,
        stopping_criteria=StoppingCriteriaList([stop]),
    )
    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()

    partial_message = ""
    for new_token in streamer:
        if new_token != "<":
            partial_message += new_token
            yield partial_message


gr.ChatInterface(predict).launch(share=True)