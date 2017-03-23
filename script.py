import os
import git
import requests
import json

CWD = os.getcwd()
PR_URL = 'https://api.github.com/repos/alexkarpovich/flow-test/pulls'
DEV_CONDIDATE = 'dev-condidate'
source_branches = ['one', 'two']

params = dict(
    state='open',
    base='dev'
)

#response = requests.get(url=PR_URL, params=params)
#data = json.loads(response.text)
data = 'n'

if isinstance(data, list):
    for pull in data:
        source_branches.append(pull['head']['ref'])

print 'Branches of unmerged Pull Requests', source_branches

repo = git.Repo(CWD)
origin = repo.remotes.origin
origin.fetch()

repo.heads.dev.checkout()

if DEV_CONDIDATE in repo.branches:
    repo.delete_head(DEV_CONDIDATE)

repo.create_head(DEV_CONDIDATE)
repo.branches[DEV_CONDIDATE].checkout()

repo.git.merge(source_branches)

print repo.git.status()
