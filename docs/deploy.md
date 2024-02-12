# Deployment Checklist

## Install

Make sure the following tools are installed in the deployment environment

- [x] python3.10/poetry (python runtime and dependency manager)
- [x] node/npm - nvm (javascript runtime and dependency manager)
- [x] just (task runner)
- [ ] duckdb (OLAP engine)
- [ ] redis (message broker and result store for celery)


Optionally also install

- eza (better `ls`)
- ripgrep (better `grep`)
- bat (better cat)
- fzf (fuzzy finder)


## Server Configuration

- [ ] setup Let's Encrypt TLS Certificate for HTTPS
- [ ] setup firewall
- [ ] setup fail2ban
- [x] setup ssh key only login
- [x] setup sudo
- [x] setup starship
- [ ] setup cron schedule for `exports` and `uploads` cleanup
- [x] disable root login
- [ ] configure log report service
- [x] update packages
- [ ] add to VPC with local computer


## App Configuration

- Check `../README.md`


## References

- https://wpjohnny.com/harden-linux-web-server/
- https://linuxhandbook.com/things-to-do-after-installing-linux-server/
