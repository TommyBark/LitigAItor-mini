import os
import re
from dataclasses import dataclass, field
from typing import Optional, Tuple, Any

import torch
import yaml
from peft import LoraConfig
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainerCallback,
    TrainingArguments,
)


def load_config(config_path: str) -> dict:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"The config file {config_path} does not exist.")
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def update_config(config_path: str, key: str, new_value: str) -> None:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    config[key] = new_value
    with open(config_path, "w") as f:
        yaml.safe_dump(config, f)
    print(f"Updated the {key} field in the config file.")


def format_message_phi(user_message: str, system_message: Optional[str] = None) -> str:
    if system_message is not None:
        return f"<|system|>\n{system_message}<|end|>\n<|user|>\n{user_message}<|end|>\n<|assistant|>\n"
    return f"\n<|user|>\n{user_message}<|end|>\n<|assistant|>\n"


def load_model_and_tokenizer(config_path: str = "./configs/model_config.yml") -> Tuple[Any, Any, str]:
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    config = load_config(config_path)

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
    return model, tokenizer, device


def get_latest_checkpoint(output_dir):

    checkpoints = [
        d
        for d in os.listdir(output_dir)
        if os.path.isdir(os.path.join(output_dir, d)) and re.match(r"checkpoint-\d+", d)
    ]

    if not checkpoints:
        return None  # No checkpoints found

    checkpoints.sort(key=lambda x: int(re.findall(r"\d+", x)[0]), reverse=True)

    # Return the path to the latest checkpoint
    return os.path.join(output_dir, checkpoints[0])


class ProfilerCallback(TrainerCallback):
    def __init__(self, profiler):
        self.profiler = profiler

    def on_step_end(self, *args, **kwargs):
        self.profiler.step()


@dataclass
class FinetuningArguments:
    model_name: Optional[str] = field(
        default="microsoft/Phi-3-mini-4k-instruct", metadata={"help": "the model name"}
    )

    dataset_name: Optional[str] = field(
        default="../stack-exchange-paired_micro", metadata={"help": "the dataset name"}
    )
    subset: Optional[str] = field(
        default="data/finetune", metadata={"help": "the subset to use"}
    )
    split: Optional[str] = field(default="train", metadata={"help": "the split to use"})
    size_valid_set: Optional[int] = field(
        default=1000, metadata={"help": "the size of the validation set"}
    )
    streaming: Optional[bool] = field(
        default=True, metadata={"help": "whether to stream the dataset"}
    )
    shuffle_buffer: Optional[int] = field(
        default=5000, metadata={"help": "the shuffle buffer size"}
    )
    seq_length: Optional[int] = field(
        default=1024, metadata={"help": "the sequence length"}
    )
    num_workers: Optional[int] = field(
        default=8, metadata={"help": "the number of workers"}
    )

    training_args: TrainingArguments = field(
        default_factory=lambda: TrainingArguments(
            output_dir="./results_ft",
            max_steps=10000,
            logging_steps=50,
            save_steps=100,
            per_device_train_batch_size=1,
            per_device_eval_batch_size=1,
            gradient_accumulation_steps=2,
            gradient_checkpointing=False,
            group_by_length=False,
            learning_rate=1e-4,
            lr_scheduler_type="cosine",
            warmup_steps=500,
            weight_decay=0.05,
            optim="paged_adamw_32bit",
            bf16=True,
            remove_unused_columns=False,
            run_name="sft_llama2",
            report_to="wandb",
            save_total_limit=10,
        )
    )

    packing: Optional[bool] = field(
        default=True, metadata={"help": "whether to use packing for SFTTrainer"}
    )

    peft_config: LoraConfig = field(
        default_factory=lambda: LoraConfig(
            r=8,
            lora_alpha=16,
            lora_dropout=0.05,
            target_modules=["q_proj", "v_proj"],
            bias="none",
            task_type="CAUSAL_LM",
        )
    )
