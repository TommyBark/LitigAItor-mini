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

from litigaitor_mini.rag import RAGDummy
from litigaitor_mini.utils import load_config, load_model_and_tokenizer

config_path = "../configs/model_config.yml"
config = load_config(config_path)

system_message = config["SYSTEM_MESSAGE"]

model, tokenizer, device = load_model_and_tokenizer(config_path)
model.eval()
# model.disable_adapters()

rag = RAGDummy(config["RAG_SUFFIX"])
rag.generate_random_documents()


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
    if not history:
        rag_suffix = rag.generate_suffix_prompt(message, top_k=3)
    else:
        rag_suffix = ""
    history_transformer_format = history + [[message + rag_suffix, ""]]
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
