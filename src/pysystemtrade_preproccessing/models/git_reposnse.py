from pydantic import BaseModel


class GitHubLinks(BaseModel):
    self: str
    git: str
    html: str


class GitHubContent(BaseModel):
    name: str
    path: str
    sha: str
    size: int
    url: str
    html_url: str
    git_url: str
    download_url: str | None
    type: str
    _links: GitHubLinks
