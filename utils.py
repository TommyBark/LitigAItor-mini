from dataclasses import dataclass, field
from typing import Optional
from transformers import (
    TrainingArguments,
)
from peft import LoraConfig


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
            save_total_limit=10
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