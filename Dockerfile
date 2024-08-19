FROM python:3.10-slim

RUN pip install -U pip
RUN pip install pipenv
RUN apt-get update && apt-get install -y git

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

ENV GRADIO_SERVER_NAME="0.0.0.0"
EXPOSE 7860
# Clone the whole repository
RUN git clone https://github.com/TommyBark/LitigAItor-mini

WORKDIR /app/LitigAItor-mini

RUN pip install -e .

CMD [ "python", "litigaitor_mini/interface.py" ]