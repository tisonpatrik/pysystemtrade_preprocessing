from pathlib import Path

from pydantic import BaseModel


class RawDataFile(BaseModel):
    name: str
    directory: str
    local_path: Path
