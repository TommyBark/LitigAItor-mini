import torch
from transformers import BitsAndBytesConfig, LlamaForCausalLM, LlamaTokenizer, 
import os
from trl import SFTTrainer
from contextlib import nullcontext
from dataset import create_datasets
from utils import FinetuningArguments

import yaml

def load_config(config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"The config file {config_path} does not exist.")
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

config_path = "../configs/finetune_config.yml"

config = load_config(config_path)

model_path = config["base_model_path"]
output_dir = config["output_dir"]
resume_from_checkpoint = config["resume_from_checkpoint"]

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

if os.path.isdir(model_path):
    tokenizer = LlamaTokenizer.from_pretrained(model_path)
    model = LlamaForCausalLM.from_pretrained(
        model_path,
        device_map="auto",
        torch_dtype=torch.float16,
        quantization_config=bnb_config,
    )
else:
    base_model_name = config["base_model_name"]
    tokenizer = LlamaTokenizer.from_pretrained(
        base_model_name, token=os.environ.get("HF_TOKEN")
    )
    model = LlamaForCausalLM.from_pretrained(
        base_model_name,
        token=os.environ.get("HF_TOKEN"),
        device_map="auto",
        torch_dtype=torch.float16,
        quantization_config=bnb_config,
    )

tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"  # Fix weird overflow issue with fp16 training
model.config.use_cache = False

# profiler
enable_profiler = False


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


script_args = FinetuningArguments(model_name = config["base_model_name"])
peft_config = script_args.peft_config
training_args = script_args.training_args


train_dataset, eval_dataset = create_datasets(tokenizer, script_args)
#ds = build_finetune_dataset(tokenizer)


def get_latest_checkpoint_path(output_dir):
    checkpoint_paths = [
        os.path.join(output_dir, f)
        for f in os.listdir(output_dir)
        if f.startswith("checkpoint")
    ]
    latest_checkpoint_path = max(checkpoint_paths, key=os.path.getctime)
    return latest_checkpoint_path


with profiler:
    trainer = SFTTrainer(
        model=model,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        peft_config=peft_config,
        packing=script_args.packing,
        max_seq_length=None,
        tokenizer=tokenizer,
        args=training_args,
        callbacks=[profiler_callback] if enable_profiler else [],
    )
    trainer.train(resume_from_checkpoint=resume_from_checkpoint)

trainer.save_model(script_args.training_args.output_dir)