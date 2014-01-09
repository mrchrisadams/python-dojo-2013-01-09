
# pull in our repo object
from git import Repo
from collections import deque
from datetime import datetime

# then fetch a repo from somewhere
# ./
PATH = "/Users/chrisadams/Code/python-dojo-2013-01-09/styles"
CURRENT_FILES = []

def _walk(tree):
    for b in tree.blobs:
        yield b.path
    for t in tree.trees:
        for p in _walk(t):
            yield p


def current_contents(commit):
    return list(_walk(commit.tree))


def repo2dict(head_commit, files):
    queue = deque([head_commit])
    latest = {}
    commits = set()

    while queue:
        commit = queue.popleft()
        if commit.binsha in commits:
            continue
        commits.add(commit.binsha)
        date = commit.committed_date

        files_modified = commit.stats.files.keys()

        for p in files_modified:
            try:
                c = latest[p]
            except KeyError:
                latest[p] = date
            else:
                if date > c:
                    latest[p] = date

        if set(latest.keys()) == files:
            break

        queue.extend(commit.parents)
    return latest

if __name__ == '__main__':
    repo = Repo(PATH)
    master_head_commit = repo.head.reference.commit
    contents = set(current_contents(master_head_commit))
    times = repo2dict(master_head_commit, contents)
    d = {k: datetime.fromtimestamp(v).isoformat(' ') for k, v in times.items() if k in contents}
    from pprint import pprint
    pprint(d)

