#!/usr/bin/env python3

from sys import argv


if __name__ == "__main__":
    # Import the library and setup context
    with open("/usr/libexec/git-shared.py") as library:
        exec(library.read())
        git_setup()
    
    # Delete the repo
    reponame = argv[1] if 1 < len(argv) else ""
    try:
        repo = gitrepo(reponame)
        repo.delete()
    except Exception as e:
        print(f"Fatal error: {e}")
        exit(1)
