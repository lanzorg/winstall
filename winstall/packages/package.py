import os
import re
from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path

from pkg_resources import parse_version


class Package(ABC):
    @abstractproperty
    def package_root(self) -> Path:
        pass

    @abstractproperty
    def package_type(self) -> str:
        pass

    @abstractproperty
    def curr_version(self) -> str:
        pass

    @abstractproperty
    async def last_version(self) -> str:
        pass

    @abstractmethod
    def download(self) -> str:
        pass

    @abstractmethod
    def install(self) -> None:
        pass

    @property
    def package_name(self) -> str:
        return "-".join([x.casefold() for x in re.findall("[A-Z0-9][^A-Z0-9]*", type(self).__name__)])

    @property
    def package_info(self) -> str:
        return self.__doc__ if self.__doc__ else "..."

    @property
    def is_checked(self):
        return False

    @property
    def is_installed(self) -> bool:
        return os.path.exists(self.package_root) and len(os.listdir(self.package_root)) > 0

    @property
    async def needs_update(self) -> bool:
        if not self.is_installed:
            return True
        return parse_version(str(await self.last_version)) > parse_version(str(self.curr_version))
