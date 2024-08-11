import subprocess
from typing import Tuple

import yaml
from huggingface_hub import HfApi
from prefect import flow, task
from utils import update_config

dataset_config_path = "../configs/dataset_config.yml"


@task
def check_for_update(dataset_name: str, last_version: str) -> Tuple[bool, str]:
    api = HfApi()
    info = api.dataset_info(dataset_name)
    new_version = info.sha
    if new_version is None:
        raise ValueError("Dataset sha not found.")
    if new_version != last_version:
        return True, new_version
    return False, last_version


@task
def trigger_finetuning() -> None:
    subprocess.run(["python", "finetuning.py"], check=True)


@task
def update_config_task(yaml_file_path: str, key: str, new_value: str) -> None:
    update_config(yaml_file_path, key, new_value)


@flow(log_prints=True)
def fine_tuning_flow(config_path: str) -> None:
    with open(dataset_config_path, "r") as f:
        config = yaml.safe_load(f)
    updated, new_version = check_for_update(
        config["dataset_name"], config["dataset_sha"]
    )

    if updated:
        trigger_finetuning()
        update_config_task(config_path, "dataset_sha", new_version)


# Run the flow locally
if __name__ == "__main__":
    fine_tuning_flow(config_path=dataset_config_path)
