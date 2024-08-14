class RAG:
    def __init__(self, embedding_model: str, prompt_suffix: str):
        self.model = self._load_model(embedding_model)
        self.documents = {}
        self.embeddings = {}
        self.prompt_suffix = prompt_suffix

    def load_documents(self):
        pass

    def search(self, query: str, top_k: int = 3):
        pass

    def generate_suffix_prompt(self, query: str, top_k: int = 3) -> str:
        pass

    def add_document(self, filename: str, content: str):
        pass

    def remove_document(self, filename: str):
        pass

    def _load_model(self, embedding_model: str):
        pass


class RAGDummy(RAG):
    def __init__(self, prompt_suffix: str = ""):
        super().__init__("dummy", prompt_suffix)

    def load_documents(self):
        self.documents = {
            "doc1": "This is the first document",
            "doc2": "This is the second document",
            "doc3": "This is the third document",
        }

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
        self.documents[filename] = content

    def remove_document(self, filename: str):
        self.documents.pop(filename)

    def _load_model(self, embedding_model: str):
        return None
