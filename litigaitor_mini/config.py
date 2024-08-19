import os

from dotenv import dotenv_values, load_dotenv

dirname = os.path.dirname(os.path.abspath(__file__))
dotenv_location = os.path.realpath(os.path.join(dirname, "..", ".env"))
# dotenv_config = dotenv_values(dotenv_location)
load_dotenv(dotenv_location)
# Access environment variables

# If following environment variables are not set, the program will raise an error
if os.getenv("MODEL_CONFIG_PATH") is None:
    raise ValueError("MODEL_CONFIG_PATH is not set")
else:
    MODEL_CONFIG_PATH = os.getenv("MODEL_CONFIG_PATH")
FINETUNE_CONFIG_PATH = os.getenv("FINETUNE_CONFIG_PATH")
DATASET_CONFIG_PATH = os.getenv("DATASET_CONFIG_PATH")


import os
from prefect import flow, task


@flow(log_prints=True)
def rag_s3_flow(bucket: str, file_key: str) -> None:
    print(os.getcwd())

#rag_s3_flow.serve(name="s3-triggered-rag-update")