import json

from utils import load_config

with open("test_questions.json", "r") as f:
    questions = json.load(f)["Questions"]
model_config = load_config("../configs/model_config.yml")


def inc(x):
    return x + 1


def test_questions():
    for question in questions:
        print(question)

    assert inc(1) == 1
