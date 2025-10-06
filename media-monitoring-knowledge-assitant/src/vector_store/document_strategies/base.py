from abc import ABC, abstractmethod


class DocumentLoaderStrategy(ABC):
    @abstractmethod
    def load_documents(self, document: str) -> dict:
        pass
