#!/usr/bin/env python3

import inspect


if __name__ == "__main__":
    message = inspect.cleandoc("""
        -
        Interactive git-shell access
        
        Possible commands are:
          ls                        Lists all git repos
          
          mkrepo <name>             Initializes a git repository
            name                      The repository name
            
          mv <oldname> <newname>    Renames a git repository
            oldname                   The old/current repository name
            newname                   The new repository name
            
          rm <name>                 Destroys/deletes a git repository
            name                      The name of the repository to delete
          
          help                      Displays this help
        -
        """)
    print(message)
