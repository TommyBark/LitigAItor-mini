import os

from dotenv import load_dotenv

dirname = os.path.dirname(os.path.abspath(__file__))
dotenv_location = os.path.realpath(os.path.join(dirname, "..", ".env"))

load_dotenv(dotenv_location)
# Access environment variables

# If following environment variables are not set, the program will raise an error
if os.getenv("MODEL_CONFIG_PATH") is None:
    raise ValueError("MODEL_CONFIG_PATH is not set")
else:
    MODEL_CONFIG_PATH = os.getenv("MODEL_CONFIG_PATH")
FINETUNE_CONFIG_PATH = os.getenv("FINETUNE_CONFIG_PATH")
DATASET_CONFIG_PATH = os.getenv("DATASET_CONFIG_PATH")
GRADIO_PASSWORD = os.getenv("GRADIO_PASSWORD")