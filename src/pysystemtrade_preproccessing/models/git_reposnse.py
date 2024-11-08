from pathlib import Path

from pydantic import BaseModel


class GitHubContent(BaseModel):
    name: str
    path: Path
    url: str
    type: str
