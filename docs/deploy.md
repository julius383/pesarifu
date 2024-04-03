# Deployment Checklist

## Install

Make sure the following tools are installed in the deployment environment

- [x] python3.10/poetry (python runtime and dependency manager)
- [x] node/npm - nvm (javascript runtime and dependency manager)
- [x] just (task runner)
- [ ] duckdb (OLAP engine)
- [x] redis (message broker and result store for celery)
- [x] poppler-utils (for pdftotext)
- [x] java (for tabula-py)
- [x] caddy (web server)
- [x] postgresql-devel (libpq-dev)


Optionally also install

- eza (better `ls`)
- ripgrep (better `grep`)
- bat (better cat)
- fzf (fuzzy finder) - install script


## Server Configuration

- [ ] setup Let's Encrypt TLS Certificate for HTTPS
- [x] setup firewall
- [ ] setup fail2ban
- [x] setup ssh key only login
- [x] setup sudo
- [x] setup starship
- [ ] setup cron schedule for `exports` and `uploads` cleanup
- [ ] disable root login
- [ ] configure log report service
- [x] update packages
- [ ] add to VPC with local computer
- [x] create .demo file with url for report demo


## App Configuration

- Check `../README.md`
- setup evidence config


## References

- https://wpjohnny.com/harden-linux-web-server/
- https://linuxhandbook.com/things-to-do-after-installing-linux-server/
- https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04
