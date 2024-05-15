# Checklist For Maintaining The Repo

Should be done at least 2 a month but ideally reviews
to decide if any action is necessary should be done
once a week.

- [ ] Update Python dependencies
    - [ ] local: `poetry update`
    - [ ] local: run tests
    - [ ] remote: `rm poetry.lock && poetry update`
- [ ] Reports (evidence)
    - [ ] check release notes and decide if update is worth it
    - [ ] local in src/reports :
        - `rm node_modules/`
        - `npm install @evidence-dev/evidence@latest @evidence-dev/core-components@latest`
        - `npm run sources & npm run build`
