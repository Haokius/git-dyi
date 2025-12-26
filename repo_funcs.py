import configparser
import os
from gitrepo import GitRepository
from repo_paths import repo_dir, repo_file


def repo_default_config():
    ret = configparser.ConfigParser()

    ret.add_section("core")
    ret.set(
        "core", "repositoryformatversion", "0"
    )  # the version of the gitdir format, 0 is initial format
    ret.set(
        "core", "filemode", "false"
    )  # disable tracking of file permission changes in the worktree
    ret.set("core", "bare", "false")  # indicates that this repo has a worktree

    return ret


def repo_create(path):
    """Create a new repository at the given path"""

    repo: GitRepository = GitRepository(path, True)

    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception(f"Path {path} is not a directory")
        if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
            raise Exception(f"Path {path} is a directory but is not empty")
    else:
        os.makedirs(repo.worktree)

    # make the following directories in the gitrepo
    assert repo_dir(repo, "branches", mkdir=True)
    assert repo_dir(repo, "objects", mkdir=True)
    assert repo_dir(repo, "refs", "tags", mkdir=True)
    assert repo_dir(repo, "refs", "heads", mkdir=True)

    # make the .git/description and .git/HEAD files
    with open(repo_file(repo, "description"), "w") as file:
        file.write(
            "Unnamed repository: edit this file 'description' to name the repository.\n"
        )
    with open(repo_file(repo, "HEAD"), "w") as file:
        file.write("ref: refs/head/master\n")
    with open(repo_file(repo, "config"), "w") as file:
        config = repo_default_config()
        config.write(file)

    return repo


def repo_find(path=".", required=True):
    path = os.path.realpath(path)

    # if current path is root
    if os.path.isdir(os.path.join(path, ".git")):
        return GitRepository(path)

    # otherwise check parent
    parent = os.path.realpath(os.path.join(path, ".."))

    if parent == path:
        if required:
            raise Exception("No git directory.")
        else:
            return None

    # recurse
    return repo_find(parent, required)
