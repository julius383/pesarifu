## Get Started using the CLI

```bash
npx degit evidence-dev/template my-project
cd my-project
npm install
npm run sources
npm run dev
```

Check out the docs for [alternative install methods](https://docs.evidence.dev/getting-started/install-evidence) including Docker, Github Codespaces, and alongside dbt.


## Connection Issues

If you see `✗ orders_by_month Missing database credentials`, you need to add the connection to the demo database:

1. Open the settings menu at [localhost:3000/settings](http://localhost:3000/settings)
2. select `DuckDB`
3. enter `needful_things`
4. select `.duckdb` and save

## Learning More

- [Docs](https://docs.evidence.dev/)
- [Github](https://github.com/evidence-dev/evidence)
- [Slack Community](https://slack.evidence.dev/)
- [Evidence Home Page](https://www.evidence.dev)

## Tasks

- TODO: figure out how to setup demo page, maybe use nginx rewrite to demo user
  info
- TODO: maybe create alternate table component
- TODO: change header, favicon
- TODO: add proxy for subscriptions
- TODO: design and add 404 pages
