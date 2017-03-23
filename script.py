import os
import git
import requests
import json
from subprocess import call


REPO_DIR = os.getcwd()
PR_URL = 'https://api.github.com/repos/alexkarpovich/flow-test/pulls'
DEV_CONDIDATE = 'dev-condidate'
BASE_BRANCH = 'dev'
source_branches = []

params = dict(
    state='open',
    base=BASE_BRANCH
)

response = requests.get(url=PR_URL, params=params)
data = json.loads(response.text)
#data = 'n'

if isinstance(data, list):
    
    print 'Open Pull Requests to %s:' % BASE_BRANCH

    for pull in data:
        print "- '%s' [%s -> %s]" % (pull['title'], pull['head']['ref'], BASE_BRANCH)
        source_branches.append(pull['head']['ref'])

    print 'Branches to merge:'

    for branch in source_branches:
        print '-', branch

    repo = git.Repo(REPO_DIR)
    origin = repo.remotes.origin
    origin.fetch()

    repo.heads[BASE_BRANCH].checkout()

    if DEV_CONDIDATE in repo.branches:
        repo.git.branch('-D', DEV_CONDIDATE)

    repo.create_head(DEV_CONDIDATE)
    repo.branches[DEV_CONDIDATE].checkout()

    repo.git.merge(source_branches)

    found_a_conflict = False

    # This gets the dictionary discussed above 
    unmerged_blobs = repo.index.unmerged_blobs()

    print unmerged_blobs
    # We're really interested in the stage each blob is associated with.
    # So we'll iterate through all of the paths and the entries in each value
    # list, but we won't do anything with most of the values.
    for path in unmerged_blobs:
        list_of_blobs = unmerged_blobs[path]
        for (stage, blob) in list_of_blobs:
            # Now we can check each stage to see whether there were any conflicts
            if stage != 0:
                found_a_conflict = True


    if not found_a_conflict:
        call("restart uwsgi") 
        call("supervisorctl restart celery")
    
else:
    print 'There is nothing to deploy.'
