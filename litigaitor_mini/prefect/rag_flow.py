import os

# import boto3
from prefect import flow, task

# from prefect.deployments.deployments import Deployment

# from litigaitor_mini.rag import RAG, RAGDummy


# @task
# def add_pdf_from_s3(rag: RAG, bucket: str, file_key: str) -> None:
#     s3_client = boto3.client("s3")
#     response = s3_client.get_object(Bucket=bucket, Key=file_key)
#     data = response.get("Body").read()
#     with open(f"./temp/{file_key}", "wb") as f:
#         f.write(data)
#     rag.add_pdf(f"./temp/{file_key}")


@flow(log_prints=True)
def rag_s3_flow(bucket: str, file_key: str) -> None:
    print(os.getcwd())
    # rag = RAGDummy()
    # add_pdf_from_s3(rag, bucket, file_key)


# Create the deployment
# deployment = Deployment.build_from_flow(
#     flow=rag_flow,
#     name="s3-triggered-rag-update",
#     parameters={"file_key": "example-file-key"},  # Default parameter
#     trigger="webhook",  # Indicate this deployment will be triggered via webhook
# )

# deployment.apply()
#rag_s3_flow.serve(name="s3-triggered-rag-update")
