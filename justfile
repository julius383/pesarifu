#!/usr/bin/env -S just --working-directory . --justfile

api-run:
    # sudo systemctl start postgresql.service
    litestar --app pesarifu.api.app:app run --reload

celery-run:
    # sudo systemctl start redis.service
    celery --app pesarifu.config.celery worker --loglevel INFO --pool=prefork --concurrency=4

clean: backup
    gum confirm "Remove uploaded files" && rmdir uploads/*
    gum confirm "Remove exported files" && rmdir exports/*

backup:
    tar cvJf uploads.tar.xz --directory=uploads .
    tar cvJf exports.tar.xz --directory=exports .

setup:
    poetry install
    touch .env
    mkdir uploads exports

overview:
    eza --hyperlink --tree --long --group-directories-first --ignore-glob __pycache__ --ignore-glob node_modules --git-ignore

tasks:
    rg --pretty --max-depth 50 --glob '!justfile' 'FIXME|TODO'

lint:
    isort src/
    black src/

build-styles:
    npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css

website-serve: build-styles api-run
    echo "serving website"

reports-serve:
    cd src/reports && npm run dev
