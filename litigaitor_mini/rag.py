class RAG:
    def __init__(self, embedding_model: str):
        self.model = self._load_model(embedding_model)
        self.documents = {}
        self.embeddings = {}

    def load_documents(self):
        pass

    def search(self, query: str, top_k: int = 3):
        pass

    def add_document(self, filename: str, content: str):
        pass

    def remove_document(self, filename: str):
        pass

    def _load_model(self, embedding_model: str):
        pass
