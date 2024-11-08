from pydantic import BaseModel


class GitHubContent(BaseModel):
    name: str
    path: str
    url: str
    type: str
