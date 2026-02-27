from abc import ABC, abstractmethod
from typing import Dict, Any

class ReviewEngine(ABC):

    @abstractmethod
    def review_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        pass