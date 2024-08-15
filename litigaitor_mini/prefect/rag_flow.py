from prefect import flow, task

from litigaitor_mini.rag import RAG, RAGDummy


@task
def add_pdf_to(rag: RAG, pdf_location: str) -> None:
    rag.add_pdf(pdf_location)


@flow
def rag_flow(pdf_location: str) -> None:
    rag = RAGDummy()
    add_pdf_to(rag, pdf_location)
