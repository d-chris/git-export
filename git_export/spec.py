from __future__ import annotations

import typing as t

import pathspec
from pathlibutil import Path

if t.TYPE_CHECKING:
    import os


class PathSpec(pathspec.PathSpec):
    @property
    def file(self) -> Path:
        try:
            return self._filename
        except AttributeError as e:
            raise AttributeError(
                f"{type(self)} has no file attribute, use `from_file()`."
            ) from e

    @classmethod
    def from_file(cls, filename: str | os.PathLike) -> PathSpec:
        """Create a PathSpec from a file."""

        file = Path(filename).resolve(True)

        with file.open("r") as f:
            obj = cls.from_lines("gitwildmatch", f)

        setattr(obj, "_filename", file)

        return obj

    def __iter__(self) -> t.Iterator[Path]:
        try:
            root = self.file.parent
        except AttributeError:
            root = Path.cwd()

        yield from map(
            lambda x: root.joinpath(x),
            self.match_tree_files(root),
        )

    def __repr__(self) -> str:
        try:
            return f"{self.__class__.__name__}('{self.file}')"
        except AttributeError:
            return super().__repr__()
