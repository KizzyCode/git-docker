#!/usr/bin/env python3

import os


if __name__ == "__main__":
    # Import the library and setup context
    with open("/usr/libexec/git-shared.py") as library:
        exec(library.read())
        git_setup()

    # List the repos, ignore non-repos
    for reponame in os.listdir("."):
        try:
            repo = gitrepo(reponame)
            print(f"{repo.name()}")
        except:
            pass
