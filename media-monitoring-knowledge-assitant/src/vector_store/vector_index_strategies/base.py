from abc import ABC, abstractmethod
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List


class VectorIndexStrategy(ABC):
    @abstractmethod
    def create_or_load_vectorstore(self) -> "VectorIndexStrategy":
        """
        Create a new or load an existing vectorstore and return an object that
        can index and query. Implementations may return `self`.
        """
        raise NotImplementedError

    @abstractmethod
    def query(self, text: List[float], top_k: int) -> List[str]:
        raise NotImplementedError
