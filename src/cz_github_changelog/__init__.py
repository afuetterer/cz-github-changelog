"""TODO."""
import re
from typing import Optional

from commitizen import git
from commitizen.config.base_config import BaseConfig
from commitizen.cz.conventional_commits import ConventionalCommitsCz

from .helpers import GitHubRepo

# header levels
H1 = "#"
H2 = "##"


class GitHubChangelogCz(ConventionalCommitsCz):
    """Custom Commitizen class to generate more expressive GitHub changelogs.

    This class is based on the ConventionalCommitsCz class from commitizen.
    """

    # TODO:
    # Code Refactoring?
    # Breaking Changes?

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
        tags = re.findall(all_tags_pattern, full_changelog, re.MULTILINE)
        print("all tags found in full_changelog:", tags)
        for tag_position, tag in enumerate(tags):
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
            full_changelog = re.sub(
                this_tag_pattern, this_tag_replace_pattern, full_changelog, flags=re.MULTILINE
            )
        return full_changelog


discover_this = GitHubChangelogCz
