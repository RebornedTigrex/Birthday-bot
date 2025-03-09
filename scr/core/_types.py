from typing import Union, Tuple, Optional, Mapping

# По сути этот файл вообще нахуй не нужен. Возможно я его вырежу позже, если не найду как его можно использовать.

FileContent = Union[bytes, str]
FileTypes = Union[
    FileContent,
    Tuple[Optional[str], FileContent],
    Tuple[Optional[str], FileContent, Mapping[str, str]], # Имя файла, побитовое представление файла, dict представление файла
]