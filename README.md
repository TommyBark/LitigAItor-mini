# LitigAItor-mini

_LitigAItor_ is a fullstack app featuring a helpful chatbot model specialized in law (based on _Phi-3-mini_).

## Features

- Simple but functional chat interface using Gradio
- Finetuned on `HFforLegal/case-law` dataset
  - Model tracking and artifact storage using MLflow on AWS
  - Autotriggered finetuning with new dataset versions using Prefect
- RAG support with ability to upload documents - handled by Prefect
- Deployment
  - AWS using Terraform (most services)
  - Main chat interface and finetuning running on manually deployed Runpod (for the purposes of cheap GPU)


## Development progress

### App
| Feature         | State   | Comment                        |
|-----------------|---------|--------------------------------|
| Finetuning scripts      | ✅ Done | |
| Chat interface       | ✅ Done  | Using Gradio     |
|Dockerfile for deployment| ✅ Done | | 
| Experiment Tracking & Model Registry |  🚧 WIP | | 
| Grafana  | ❌ Not Started  |
| Benchmarking model | 🚧 WIP | Using LegalBench |
|Workflow orchestration| 🚧 WIP | Only examples of workflows |


### Deployment using Terraform
| Feature         | State   | Comment                        |
|-----------------|---------|--------------------------------|
| MLFlow on AWS     | ✅ Done | |
| Prefect Server | ✅ Done | |
| Prefect Workers       | 🚧 WIP   | Currently only simple EC2 worker   |
| Chat Interface | 🚧 WIP | Manually deployed on Runpod |
| Grafana | ❌ Not Started | | 


### Best practices
| Feature         | State   | Comment                        |
|-----------------|---------|--------------------------------|
|Unit Tests| 🚧 WIP | Simple chatbot tests |
| Integration Tests| ❌ Not Started  | |
| Linter and/or Code Formatter |🚧 WIP | |  
| Makefile| ❌ Not Started   | |
| pre-commit | 🚧 WIP | |
| CI/CD pipeline | ❌ Not Started | | 

## How to run

To run everything you need following:
- AWS Account
- Runpod.io Account
- Huggingface.co Account

Make sure that you setup AWS credentials by running `aws configure` and that Terraform is installed

### MLflow deployment

1. Set DB passowrd by running `export TF_VAR_mlflow_db_password=<password>`
2. Run `terraform init` and `terraform apply` in `/infrastructure/mlflow-setup/`

### Prefect deployment

1. Set your IP by running `export TF_VAR_prefect_ingress_cidr_blocks='["<your-ip>"]'`, this is for the security.
2. Run `terraform init` and `terraform apply` in `/infrastructure/prefect-setup/`

### Runpod deployment

1. Get a pod from Runpod.io with at least 8GB of GPU VRAM and 25GB of storage
2. Make sure it has public IP and exposed http port.
3. Set up the password for the app by setting envvar `GRADIO_PASSWORD`  
4. SSH into the pod and copy `/infrastructure/runpod/runpod_script.sh`
5. Run 
  ```bash
  chmod +x runpod_script.sh
  ./runpod_script.sh
  ```

Alternatively you can use `Dockerfile` to build and push the image to docker.io where you can reuse it in the Runpod.
