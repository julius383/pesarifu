# Deployment Checklist

## Install

Make sure the following tools are installed in the deployment environment

- [ ] python3.10/poetry (python runtime and dependency manager)
- [ ] node/npm - nvm (javascript runtime and dependency manager)
- [ ] just (task runner)
- [ ] duckdb (OLAP engine)
- [ ] redis (message broker and result store for celery)
- [ ] poppler (for pdftotext)
- [ ] java (for tabula-py)


Optionally also install

- eza (better `ls`)
- ripgrep (better `grep`)
- bat (better cat)
- fzf (fuzzy finder)


## Server Configuration

- [ ] setup Let's Encrypt TLS Certificate for HTTPS
- [ ] setup firewall
- [ ] setup fail2ban
- [ ] setup ssh key only login
- [ ] setup sudo
- [ ] setup starship
- [ ] setup cron schedule for `exports` and `uploads` cleanup
- [ ] disable root login
- [ ] configure log report service
- [ ] update packages
- [ ] add to VPC with local computer


## App Configuration

- Check `../README.md`
- setup evidence config


## References

- https://wpjohnny.com/harden-linux-web-server/
- https://linuxhandbook.com/things-to-do-after-installing-linux-server/
- https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04
