from repo_paths import repo_file
import zlib
import hashlib
import os
from objects import GitBlob, GitCommit


def object_read(repo, sha):
    "Read object sha from Git repository repo - return GitObject whose exact type depends on the object"

    path = repo_file(repo, "objects", sha[:2], sha[2:])

    if not os.path.isfile(path):
        return None

    with open(path, "rb") as file:
        raw = zlib.decompress(f.read())

        x = raw.find(b" ")
        fmt = raw[:x]

        y = raw.find(b"\x00", x)
        size = int(raw[x:y].decode("ascii"))
        if size != len(raw) - y - 1:
            raise Exception(f"Malformed object {sha}: bad length")

        match fmt:
            case b"commit":
                c = GitCommit
            case b"tree":
                c = GitTree
            case b"tag":
                c = GitTag
            case b"blob":
                c = GitBlob
            case _:
                raise Exception(f"Unknown type {fmt.decode("ascii")} for object {sha}")

        # call constructor and return instance
        return c(raw[y + 1 :])


def object_write(obj, repo=None):
    data = obj.serialize()

    result = obj.fmt + b" " + str(len(data)).encode() + b"\x00" + data

    sha = hashlib.sha1(result).hexdigest()

    if repo:
        path = repo_file(repo, "objects", sha[:2], sha[2:], mkdir=True)

        if not os.path.exists(path):
            with open(path, "wb") as file:
                file.write(zlib.compress(result))

    return sha


def object_hash(fd, fmt, repo=None):
    """Hash object, writing it to repo if provided"""
    data = fd.read()

    match fmt:
        case b"commit":
            obj = GitCommit(data)
        case b"tree":
            obj = GitTree(data)
        case b"tag":
            obj = GitTag(data)
        case b"blob":
            obj = GitBlob(data)
        case _:
            raise Exception(f"Unknown type {fmt}")

    return object_write(obj, repo)


def object_find(repo, name, fmt=None, follow=True):
    return name  # temp placeholder