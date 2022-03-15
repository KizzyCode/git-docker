#!/usr/bin/env python3

import os
import shutil
import string
import subprocess
from typing import Final


class gitrepo:
    """A git repository"""

    _name_valid: Final = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_-"
    """The valid git repo name characters"""

    _name: str = ""
    """The git repo name"""

    def __init__(self, name: str) -> None:
        """Creates a new gitrepo handle"""
        self._name = name
        self._assert_name_isvalid()

    def _assert_name_isvalid(self) -> None:
        """Asserts that the repository name is valid"""
        invalid = set(self._name) - set(gitrepo._name_valid)
        if not self._name:
            raise Exception("Invalid empty repository name")
        elif invalid:
            raise Exception(f"Invalid chars in repository name: {invalid}")
    
    def _assert_isrepo(self) -> None:
        """Asserts that the repo exists"""
        try:
            gitrevparse = ["/usr/bin/git", "rev-parse", "--git-dir"]
            subprocess.check_output(gitrevparse, cwd=self._name)
        except Exception as e:
            raise Exception(f"Failed to get repository status (not a git repo?): {e}")
    
    def _assert_notrepo(self) -> None:
        """Asserts that the repo does not exist"""
        if os.path.exists(self._name):
            raise Exception(f"Repository name is already in use: {self._name}")

    def name(self) -> str:
        """Returns the repo name if the repo exists"""
        self._assert_isrepo()
        return self._name

    def create(self) -> None:
        """Creates the repo"""
        self._assert_notrepo()
        adduser = ["/usr/bin/git", "init", "--bare", self._name]
        subprocess.check_call(adduser)
    
    def rename(self, newname: str) -> None:
        """Renames the repo"""
        new_repo = gitrepo(newname)
        new_repo._assert_notrepo()
        os.rename(self._name, newname)
    
    def delete(self) -> None:
        """Deletes the repo"""
        self._assert_isrepo()
        shutil.rmtree(self._name)


def git_setup() -> None:
    """Setups the git operation context"""
    # Operate within the users git directort by default
    gitdir = os.path.expanduser("~/git")
    os.chdir(gitdir)
