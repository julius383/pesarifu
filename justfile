#!/usr/bin/env -S just --working-directory . --justfile

api-run:
    litestar --app pesarifu.api.app:app run
