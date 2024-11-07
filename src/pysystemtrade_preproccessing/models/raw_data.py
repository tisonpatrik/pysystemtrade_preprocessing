from pathlib import Path

from pydantic import BaseModel


class RawDataFile(BaseModel):
    name: str
    local_path: Path


class LoadedDirectory(BaseModel):
    files: list[RawDataFile]
