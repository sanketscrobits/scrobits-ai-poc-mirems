import os
from llama_index.core import SimpleDirectoryReader
from document_strategies.base import DocumentLoaderStrategy


class LocalDocumentsLoader(DocumentLoaderStrategy):
    def __init__(self, folder_path: str):
        self._folder_path = folder_path

    def load_documents(self, document: str) -> dict:
        docs = []
        for file in os.listdir(self._folder_path):
            file_path = os.path.join(self._folder_path, file)
            loader = SimpleDirectoryReader(file_path)
            docs.extend(loader.load_data())
        return docs
