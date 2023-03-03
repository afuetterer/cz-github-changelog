"""TODO."""
import re
from dataclasses import dataclass
from typing import Optional

from commitizen import git
from commitizen.config.base_config import BaseConfig
from commitizen.cz.conventional_commits import ConventionalCommitsCz


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


class GitHubChangelogCz(ConventionalCommitsCz):
    """TODO."""

    # TODO

    # Code Refactoring?
    # Breakin Changes?

    # more?
    change_type_map = {
        "feat": "Features",
        "fix": "Bug Fixes",
    }

    # order alright?
    change_type_order = ["Features", "Bug Fixes"]

    def __init__(self, config: BaseConfig) -> None:
        super().__init__(config)

        # get this from env?
        # usage in action?
        github_repo_owner = config.settings["github_repo_owner"]
        github_repo_name = config.settings["github_repo_name"]
        self.repo = GitHubRepo(github_repo_owner, github_repo_name)

    def changelog_message_builder_hook(self, parsed_message: dict, commit: git.GitCommit) -> dict:
        """TODO."""
        short_hash = commit.rev[:7]
        commit_url = self.repo.get_commit_url(commit)
        msg = parsed_message["message"]
        parsed_message["message"] = f"{msg} ([{short_hash}]({commit_url}))"
        return parsed_message

    def changelog_hook(self, full_changelog: str, partial_changelog: Optional[str]) -> str:
        """TODO."""
        if partial_changelog:
            pass
        if full_changelog:
            pass

        # TODO:
        # sometimes setting "#" works
        # What is incremental doing?

        # Why is first minor tag not "#"?
        # Compare url tag2 always 0.1.0?

        all_tags_pattern = r"^#{1,2} \[?(\d+.\d+.\d+)\]?"
        tags = re.findall(all_tags_pattern, full_changelog, re.MULTILINE)
        print("tags:", tags)

        for tag_position, tag in enumerate(tags):
            major, minor, patch = tag.split(".")

            if patch == "0":
                print(tag)
                # make ## -> #

            this_tag_pattern = rf"## {tag}"

            try:
                this_tag = tags[tag_position]
                previous_tag = tags[tag_position + 1]
                compare_url = self.repo.get_compare_url(previous_tag, this_tag)
                print(this_tag, previous_tag, "->", compare_url)

                if patch == "0":
                    this_tag_replace_pattern = f"# [{tag}]({compare_url})"
                else:
                    this_tag_replace_pattern = f"## [{tag}]({compare_url})"

                full_changelog = re.sub(this_tag_pattern, this_tag_replace_pattern, full_changelog)
            except IndexError:
                # last tag
                pass
        return full_changelog


discover_this = GitHubChangelogCz
