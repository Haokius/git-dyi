import argparse  # used to parse cmd line arguments
import configparser  # used to parse git's config file format
from datetime import datetime
import grp, pwd
from fnmatch import fnmatch
import hashlib
from math import ceil
import os
import re
import sys
import zlib
from repo_funcs import repo_create, repo_find
from object_funcs import object_read, object_write, object_find, object_hash

argparser = argparse.ArgumentParser(description="THe stupidest content tracker")

argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

# INIT
argsp = argsubparsers.add_parser("init", help="Initialize a new empty repository.")
argsp.add_argument(
    "path",
    metavar="directory",
    nargs="?",
    default=".",
    help="Where to create the repository",
)

# CAT-FILE
argsp = argsubparsers.add_parser(
    "cat-file", help="Provide content of repository objects"
)
argsp.add_argument(
    "type",
    metavar="type",
    choices=["blob", "commit", "tag", "tree"],
    help="Specify the type",
)
argsp.add_argument("object", metavar="object", help="The object to display")

# HASH-OBJECT
argsp = argsubparsers.add_parser(
    "hash-object",
    help="Compute object ID and optionally creates a blob from a file")
argsp.add_argument("-t",
                   metavar="type",
                   dest="type",
                   choices=["blob", "commit", "tag", "tree"],
                   default="blob",
                   help="Specify the type")
argsp.add_argument("-w",
                   dest="write",
                   action="store_true",
                   help="Actually write the object into the database")
argsp.add_argument("path",
                   help="Read object from <file>")

# LOG
argsp = argsubparsers.add_parser("log", help="Display history of a given commit.")
argsp.add_argument("commit",
                   default="HEAD",
                   nargs="?",
                   help="Commit to start at.")

def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        case "add":
            cmd_add(args)
        case "cat-file":
            cmd_cat_file(args)
        case "check-ignore":
            cmd_check_ignore(args)
        case "checkout":
            cmd_checkout(args)
        case "commit":
            cmd_commit(args)
        case "hash-object":
            cmd_hash_object(args)
        case "init":
            cmd_init(args)
        case "log":
            cmd_log(args)
        case "ls-files":
            cmd_ls_files(args)
        case "ls-tree":
            cmd_ls_tree(args)
        case "rev-parse":
            cmd_rev_parse(args)
        case "rm":
            cmd_rm(args)
        case "show-ref":
            cmd_show_ref(args)
        case "status":
            cmd_status(args)
        case "tag":
            cmd_tag(args)
        case _:
            print("Bad command.")

def cmd_add(args):
    ...

def cmd_cat_file(args):
    repo = repo_find()
    obj = object_read(repo, object_find(repo, args.object, fmt=args.type.encode()))
    sys.stdout.buffer.write(obj.serialize())

def cmd_check_ignore(args):
    ...

def cmd_checkout(args):
    ...

def cmd_commit(args):
    ...

def cmd_hash_object(args):
    repo = repo_find() if args.write else None

    with open(args.path, "rb") as fd:
        sha = object_hash(fd, args.type.encode(), repo)
        print(sha)

def cmd_init(args):
    repo_create(args.path)

def cmd_log(args):
    ...

def cmd_ls_files(args):
    ...

def cmd_ls_tree(args):
    ...

def cmd_rev_parse(args):
    ...

def cmd_rm(args):
    ...

def cmd_show_ref(args):
    ...

def cmd_status(args):
    ...

def cmd_tag(args):
    ...