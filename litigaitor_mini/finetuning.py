import importlib.util
from contextlib import nullcontext

import torch
from dataset import create_datasets
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
from utils import ProfilerCallback, get_latest_checkpoint, load_config, update_config

from litigaitor_mini.config import DATASET_CONFIG_PATH, FINETUNE_CONFIG_PATH

config = load_config(FINETUNE_CONFIG_PATH)
data_config = load_config(DATASET_CONFIG_PATH)

DEBUG = config["DEBUG"]


def finetune(config: dict, data_config: dict) -> None:
    base_model_name = config["base_model_name"]
    output_dir = config["output_dir"]
    if config["resume_from_checkpoint"]:
        resume_from_checkpoint = get_latest_checkpoint(output_dir)
    else:
        resume_from_checkpoint = False

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

    attention = (
        "eager"
        if importlib.util.find_spec("flash_attn") is None
        else "flash_attention_2"
    )

    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        trust_remote_code=True,
        quantization_config=bnb_config,
        attn_implementation=attention,
        low_cpu_mem_usage=True,
    )
    if DEBUG > 0:
        print("Model loaded")

    model = prepare_model_for_kbit_training(model)
    model = get_peft_model(model, peft_config)
    model.gradient_checkpointing_enable()
    if DEBUG > 0:
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

    data_split = f"{data_config['dataset_split']}[{int(data_config['last_row_index'])}:{int(data_config['last_row_index']) + int(config['finetune_steps'])}]"
    print(data_split)
    train_ds, eval_ds = create_datasets(
        tokenizer,
        data_config["dataset_name"],
        data_split,
        streaming=False,
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
        "save_steps": config["finetune_steps"],
        "save_total_limit": 4,
        "seed": 0,
        "gradient_checkpointing": True,
        "gradient_checkpointing_kwargs": {"use_reentrant": False},
        "gradient_accumulation_steps": 1,
        "warmup_ratio": 0.2,
        #    "report_to": "wandb",
        "run_name": "ft-phi-3-mini-4k-instruct",
        "max_steps": config["max_steps"],
        "push_to_hub": True,
        "evaluation_strategy": "steps",
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

    # update configs
    update_config(
        data_config_path,
        "last_row_index",
        data_config["last_row_index"] + config["finetune_steps"],
    )
    update_config(
        finetuning_config_path,
        "max_steps",
        config["max_steps"] + config["finetune_steps"],
    )


if __name__ == "__main__":
    if DEBUG < 2:
        finetune(config, data_config)
    else:
        print("Debug mode > 2 is enabled, skipping finetuning")
