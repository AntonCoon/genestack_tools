from abc import ABC, abstractmethod
from typing import Any


class Assistant(ABC):
    """
    Abstract base class for an Assistant that can:
    - get data
    - normalize data
    - answer general questions
    """

    @abstractmethod
    def get_data(self, *args, **kwargs) -> Any:
        """
        Retrieve data from a source.
        """
        pass

    @abstractmethod
    def normalize_data(self, data: Any, *args, **kwargs) -> Any:
        """
        Normalize the given data.
        """
        pass

    @abstractmethod
    def answer_question(self, question: str, *args, **kwargs) -> str:
        """
        Answer a general question about the data.
        It's going to be just llm requested via API, ofc,
        but here might be a cool Genestack model finetuned for specific data.
        """
        pass
