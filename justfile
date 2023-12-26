#!/usr/bin/env -S just --working-directory . --justfile

api-run:
    litestar --app pesarifu.api.app:app run --reload

setup:
    poetry install
    touch .env
    mkdir statements

tasks:
    rg --pretty --max-depth 50 --glob '!justfile' 'FIXME|TODO'

lint:
    isort src/
    black src/
