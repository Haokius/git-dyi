import configparser
import os
from repo_paths import repo_file


class GitRepository(object):
    """A git repository object"""

    worktree: str
    gitdir: str
    conf: configparser.ConfigParser

    # A git repo is made up of two things: working tree (the working directory)
    # and the git directory, which is the hidden database where Git stores everything it knows
    # e.g. full commit history, branches & tags, the staging area (the index)
    # the HEAD (the branch you're on), and object database (blobs, trees, commits)

    # You edit files in the working tree, git add copies changes to the staging area (index)
    # git commit stores a snapshot in the directory, and git checkout/restore will write from
    # directory back into the working tree

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"Not a Git Repository {path}")

        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration File missing")

        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception(f"Unsupported repositoryformatversion: {vers}")
