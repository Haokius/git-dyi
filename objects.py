class GitObject(object):
    def __init__(self, data=None):
        if data is not None:
            self.deserialize(data)
        else:
            self.init()

    def serialize(self, repo):
        """To be implemented by subclass"""
        raise Exception("Unimplemented!")

    def deserialize(self, data):
        raise Exception("Unimplemented!")

    def init(self):
        pass


class GitBlob(GitObject):
    fmt = b"blob"

    def serialize(self, repo=None):
        # repo is not used for GitBlob
        return self.blobdata

    def deserialize(self, data):
        self.blobdata = data
