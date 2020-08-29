import os
from abc import ABC, abstractmethod, abstractproperty

from pkg_resources import parse_version


class Program(ABC):
    @abstractproperty
    def install_dir(self) -> str:
        pass

    @abstractproperty
    def actual_version(self) -> str:
        pass

    @abstractproperty
    def latest_version(self) -> str:
        pass

    @property
    def is_installed(self) -> bool:
        return os.path.exists(self.install_dir) and len(os.listdir(self.install_dir)) > 0

    @property
    def is_updated(self) -> bool:
        actual_version = parse_version(str(self.actual_version))
        latest_version = parse_version(str(self.latest_version))
        return self.is_installed and latest_version <= actual_version

    @abstractmethod
    def download(self) -> str:
        pass

    @abstractmethod
    def install(self) -> None:
        pass
