import os

from pypdf import PdfReader


class RAG:
    def __init__(
        self,
        embedding_model: str,
        prompt_suffix: str,
        documents_path: str = "../documents",
    ):
        self.model = self._load_model(embedding_model)
        self.documents = {}
        self.embeddings = {}
        self.prompt_suffix = prompt_suffix
        self.documents_path = documents_path

    def load_documents(self):
        pass

    def search(self, query: str, top_k: int = 3):
        pass

    def generate_suffix_prompt(self, query: str, top_k: int = 3) -> str:
        pass

    def add_document(self, filename: str, content: str):
        pass

    def add_pdf(self, pdf_location: str):
        pass

    def remove_document(self, filename: str):
        pass

    def _load_model(self, embedding_model: str):
        pass


class RAGDummy(RAG):
    def __init__(self, prompt_suffix: str = "", documents_path: str = "../documents"):
        super().__init__("dummy", prompt_suffix, documents_path)

    def load_documents(self):
        self.documents = {}
        # load all txts from directory
        for file in os.listdir(self.documents_path):
            if file.endswith(".txt"):
                with open(os.path.join(self.documents_path, file), "r") as f:
                    self.documents[file] = f.read()
    
    def generate_random_documents(self, n: int = 3):
        for i in range(n):
            self.add_document(f"random_{i}.txt", f"Random document {i}")

    def search(self, query: str, top_k: int = 3):
        return list(self.documents.values())[:top_k]

    def generate_suffix_prompt(self, query: str, top_k: int = 3) -> str:
        relevant_docs = self.search(query, top_k)
        prompt = ""
        if not relevant_docs:
            return prompt

        for doc in relevant_docs:
            prompt += f"{doc}\n"
        prompt = self.prompt_suffix + prompt
        return prompt

    def add_document(self, filename: str, content: str):
        with open(os.path.join(self.documents_path, filename), "w") as f:
            f.write(content)
        self.documents[filename] = content

    def add_pdf(self, pdf_location: str):
        reader = PdfReader(pdf_location)
        for i, page in enumerate(reader.pages):
            filename = f"{pdf_location.split('/')[-1].removesuffix('.pdf')}_{i}.txt"
            self.add_document(filename, page.extract_text()[:1000])

    def remove_document(self, filename: str):
        self.documents.pop(filename)

    def _load_model(self, embedding_model: str):
        return None
