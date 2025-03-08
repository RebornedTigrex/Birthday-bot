from typing import Union, Tuple, Optional, Mapping

FileContent = Union[bytes, str]
FileTypes = Union[
    FileContent,
    Tuple[Optional[str], FileContent],
    Tuple[Optional[str], FileContent, Mapping[str, str]], # Имя файла, побитовое представление файла, dict представление файла
]