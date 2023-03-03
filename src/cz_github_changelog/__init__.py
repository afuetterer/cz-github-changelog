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


# header levels
H1 = "#"
H2 = "##"


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

        all_tags_pattern = r"^#{1,2} \[?(\d+.\d+.\d+)\]?"
        tags = re.findall(all_tags_pattern, full_changelog, re.MULTILINE)  # , re.VERBOSE])
        print("----------------")
        print("all tags found in full_changelog:", tags)

        for tag_position, tag in enumerate(tags):
            print(f"processing: {tag}")
            print("--")

            _, _, patch = tag.split(".")

            heading = H2
            if patch == "0":
                heading = H1

            this_tag_pattern = f"^#{{1,2}} {tag}"

            try:
                this_tag = tags[tag_position]
                previous_tag = tags[tag_position + 1]
                compare_url = self.repo.get_compare_url(previous_tag, this_tag)
                this_tag_replace_pattern = f"{heading} [{tag}]({compare_url})"
            except IndexError:
                # earlist tag, has no previous tag -> no compare url possible
                this_tag_replace_pattern = f"{heading} {tag}"

            # print("--")
            # print(tag)
            # print("look for:", this_tag_pattern)
            # print("replace with:", this_tag_replace_pattern)
            # print()

            # print(re.search(this_tag_pattern, full_changelog, re.MULTILINE))

            # print("---")
            # print("changelog before replacing:")
            # print(full_changelog)
            full_changelog = re.sub(
                this_tag_pattern, this_tag_replace_pattern, full_changelog, flags=re.MULTILINE
            )

        # print()
        # print("##############################################")
        # print("--- output after replacing ---")
        # print(full_changelog)
        # print("##############################################")
        return full_changelog


discover_this = GitHubChangelogCz
