# Database

Data model is defined in `src/pesarifu/model`. A few key things to take a note
of within the data model are:

- Datetime are saved as UTC Unix Epoch timestamps (`float`)
- Monetary values use (`double`) instead of the Postgres `money` type
- Database names are of large constellations e.g orion
- Some tables contain a `extra` column that is used to store additional data
  not part of the schema but may be useful to have in the future
- The different types of accounts are defined using `single table inheritance`
  in SQLAlchemy. Base is `TransactionalAccount`

## Migrations

- Alembic
