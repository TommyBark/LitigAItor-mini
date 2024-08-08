import os
from contextlib import nullcontext

import torch
from huggingface_hub import HfApi
from peft import (
    LoraConfig,
    TaskType,
    get_peft_model,
    prepare_model_for_kbit_training,
)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from trl import SFTTrainer

from dataset import create_datasets
from utils import ProfilerCallback, load_config

config_path = "./configs/finetune_config.yml"

config = load_config(config_path)

DEBUG = config["DEBUG"]


base_model_name = config["base_model_name"]
output_dir = config["output_dir"]
resume_from_checkpoint = config["resume_from_checkpoint"] or None

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=False,
    r=8,
    lora_alpha=32,
    lora_dropout=0.1,
    target_modules="all-linear",
)

tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)
tokenizer.padding_side = "right"
model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    trust_remote_code=True,
    quantization_config=bnb_config,
    attn_implementation="flash_attention_2",
    low_cpu_mem_usage=True,
)
if DEBUG:
    print("Model loaded")


model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, peft_config)
model.gradient_checkpointing_enable()
if DEBUG:
    model.print_trainable_parameters()

# profiler
enable_profiler = True


# Set up profiler
if enable_profiler:
    wait, warmup, active, repeat = 1, 1, 2, 1
    total_steps = (wait + warmup + active) * (1 + repeat)
    schedule = torch.profiler.schedule(
        wait=wait, warmup=warmup, active=active, repeat=repeat
    )
    profiler = torch.profiler.profile(
        schedule=schedule,
        on_trace_ready=torch.profiler.tensorboard_trace_handler(
            f"{output_dir}/logs/tensorboard"
        ),
        record_shapes=True,
        profile_memory=True,
        with_stack=True,
    )

    profiler_callback = ProfilerCallback(profiler)
else:
    profiler = nullcontext()


train_ds, eval_ds = create_datasets(
    tokenizer,
    config["dataset_name"],
    config["dataset_split"],
    streaming=True,
    seq_length=config["seq_length"],
    size_valid_set=100,
)
if DEBUG:
    print("Datasets created")

training_config = {
    "bf16": True,
    "do_eval": False,
    "learning_rate": 1.0e-04,
    "log_level": "error",
    "logging_steps": 100,
    "logging_strategy": "steps",
    "lr_scheduler_type": "cosine",
    "num_train_epochs": 1,
    "output_dir": output_dir,
    "overwrite_output_dir": False,
    "per_device_eval_batch_size": 1,
    "per_device_train_batch_size": 1,
    "remove_unused_columns": False,
    "save_steps": 100,
    "save_total_limit": 4,
    "seed": 0,
    "gradient_checkpointing": True,
    "gradient_checkpointing_kwargs": {"use_reentrant": False},
    "gradient_accumulation_steps": 1,
    "warmup_ratio": 0.2,
    "report_to": "wandb",
    "run_name": "ft-phi-3-mini-4k-instruct",
    "max_steps": 1800,
    "push_to_hub": True,
    "evaluation_strategy":"step"
}


if DEBUG:
    training_config["logging_steps"] = 5
    training_config["max_steps"] = 10
    training_config["save_steps"] = 10
    training_config["output_dir"] = "./debug"
    training_config["report_to"] = "none"
    training_config["push_to_hub"] = False
    training_config["log_level"] = "debug"
    resume_from_checkpoint = None

training_args = TrainingArguments(**training_config)


with profiler:
    trainer = SFTTrainer(
        model=model,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        tokenizer=tokenizer,
        args=training_args,
        peft_config=peft_config,
        callbacks=[profiler_callback] if enable_profiler else [],
        max_seq_length=config["seq_length"],
    )
    train_result = trainer.train(resume_from_checkpoint=resume_from_checkpoint)

trainer.save_model(training_config["output_dir"])
