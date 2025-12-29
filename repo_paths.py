import os

def repo_path(repo, *path):
    """Compute path under the repo's git directory"""
    # putting * in front of path makes the function variadic, so it can take multiple args
    # e.g. os.path.join("root/hello", "urmom", "bob") will return root/hello/urmom/bob
    return os.path.join(repo.gitdir, *path)


def repo_dir(repo, *path, mkdir=False):
    """Return and mkdir to path if absent"""
    path_ = repo_path(repo, *path)

    if os.path.exists(path_):
        if os.path.isdir(path_):
            return path_
        else:
            raise Exception(f"Path {path_} exists but is not a directory")

    if mkdir:
        os.makedirs(path_)
        return path_

    raise Exception(f"Directory {path_} does not exist")


def repo_file(repo, *path, mkdir=False):
    """Return and (optionally) create a path to a file"""
    if mkdir:
        repo_dir(repo, *path[:-1], mkdir=True)

    return repo_path(repo, *path)
