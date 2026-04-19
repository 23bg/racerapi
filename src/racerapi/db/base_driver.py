from abc import ABC, abstractmethod

from racerapi.cli.context import CLIContext


class BaseDriver(ABC):
    def __init__(self, context: CLIContext) -> None:
        self.context = context

    @abstractmethod
    def init(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def migrate(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def upgrade(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def seed(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def check_connection(self) -> None:
        raise NotImplementedError
