# kizzycode/git
A tiny git-over-ssh server.

## Security Notice
If you clone this repo, __DO NOT__ use the provided SSH keys for production; delete them and create your own secrets
instead!

Example:
```sh
rm "mount/.config/ssh_host_rsa_key*" \
    && ssh-keygen -t rsa -b 4096 -N "" -f "mount/.config/ssh_host_rsa_key" \
    && ssh-keygen -t ed25519 -N "" -f "mount/.config/ssh_host_ed25519_key"
```
