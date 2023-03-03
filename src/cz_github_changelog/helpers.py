"""TODO."""

from dataclasses import dataclass

from commitizen import git


@dataclass
class GitHubRepo:
    """TODO."""

    owner: str
    name: str

    @property
    def url(self) -> str:
        return f"https://github.com/{self.owner}/{self.name}"

    def get_commit_url(self, commit: git.GitCommit) -> str:
        return f"{self.url}/commit/{commit.rev}"

    def get_tag_url(self, tag: str) -> str:
        return f"{self.url}/releases/tag/{tag}"

    def get_compare_url(self, tag1: str, tag2: str) -> str:
        return f"{self.url}/compare/{tag1}...{tag2}"
