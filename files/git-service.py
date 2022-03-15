#!/usr/bin/env python3

import glob
import json
import os
import subprocess
from sys import stdout, stderr
from typing import List, NoReturn


class gituser:
    """A class representing a git user"""

    _name: str = ""
    """The username"""

    _uid: str = ""
    """The user ID"""

    def __init__(self, name: str, uid: str) -> None:
        """Creates a new user handle"""
        self._name = name
        self._uid = uid
    
    def _deluser(self) -> None:
        """Deletes the user if it exists"""
        if os.path.isdir(f"/home/{self._name}"):
            deluser = ["/usr/sbin/deluser", "--remove-home", self._name]
            subprocess.check_call(deluser)
    
    def _adduser(self) -> None:
        """Creates the user"""
        adduser = ["/usr/sbin/adduser", "-s", "/usr/bin/git-shell", "-D", "-u", self._uid, self._name]
        subprocess.check_call(adduser)

    def _unlock_user(self) -> None:
        """Unlocks the user account"""
        usermod = ["/usr/sbin/usermod", "-p", "*", self._name]
        subprocess.check_call(usermod)

    def _init_git(self) -> None:
        """Creates and symlinks the associated git directory"""
        os.makedirs(f"/srv/git/{self._name}", 0o700, exist_ok=True)
        os.chown(f"/srv/git/{self._name}", int(self._uid), int(self._uid))
        os.symlink(f"/srv/git/{self._name}", f"/home/{self._name}/git")

    def create(self) -> None:
        """Creates the user"""
        self._deluser()
        self._adduser()
        self._unlock_user()
        self._init_git()

    def init_ssh(self, pubkeys: List[str]) -> None:
        """Inits ssh for the client"""
        os.makedirs(f"/home/{self._name}/.ssh", 0o750)
        with open(f"/home/{self._name}/.ssh/authorized_keys", "x") as authorized_keys:
            authorized_keys.write("\n".join(pubkeys))
    
    def init_gitshell(self) -> None:
        """Allows interactive git shell access"""
        os.makedirs(f"/home/{self._name}/git-shell-commands")
        for path in glob.glob("/usr/libexec/git-shell-*"):
            command = os.path.basename(path).removeprefix("git-shell-").removesuffix(".py")
            os.symlink(path, f"/home/{self._name}/git-shell-commands/{command}")


class sshd:
    """An sshd interface"""

    @staticmethod
    def exec() -> NoReturn:
        """Configures sshd and calls `execve` to become sshd"""
        stdout.flush()
        stderr.flush()
        os.execl("/usr/sbin/sshd", "/usr/sbin/sshd", "-D", "-e", "-f", "/etc/ssh/sshd_config")


if __name__ == "__main__":
    # Create the user
    with open("/srv/git/.config/users.json", "r") as configfile:
        for config in json.load(configfile):
            # Configure user
            user = gituser(config["name"], config["uid"])
            user.create()

            # Setup SSH and interactive git access if configured
            if config["pubkeys"]:
                user.init_ssh(config["pubkeys"])
            if config["gitshell"]:
                user.init_gitshell()
    
    # Execute sshd
    sshd.exec()
