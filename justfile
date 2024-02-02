#!/usr/bin/env -S just --working-directory . --justfile

app-run:
    # sudo systemctl start postgresql.service
    litestar --app pesarifu.api.app:app run --debug

app-run-debug:
    # sudo systemctl start postgresql.service
    litestar --app pesarifu.api.app:app run --debug

celery-run: app-setup
    # sudo systemctl start redis.service
    celery --app pesarifu.config.celery worker --loglevel INFO --pool=prefork --concurrency=4

[confirm("Are you sure want to delete everything?")]
clean: backup
    rm -r uploads/*
    rm -r exports/*

backup:
    tar cvJf uploads.tar.xz --directory=uploads .
    tar cvJf exports.tar.xz --directory=exports .

app-setup:
    poetry install
    npm install
    export APP_ROOT="$(pwd)"
    export DYNACONF_APP_ROOT="$(pwd)"
    export ROOT_PATH_FOR_DYNACONF="$(pwd)/src/pesarifu/config/"
    -mkdir uploads exports

overview:
    eza --hyperlink --tree --long --group-directories-first --ignore-glob __pycache__ --ignore-glob node_modules --git-ignore

tasks:
    rg --pretty --max-depth 50 --glob '!justfile' 'FIXME|TODO'

lint:
    isort src/
    black src/

setup: app-setup reports-setup
    echo "Running setup"

build-styles:
    npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css

website-serve: build-styles app-run
    echo "serving website"

reports-setup:
    cd src/reports && npm install

reports-build:
    cd src/reports && npm run sources
    cd src/reports && npm run build

reports-build-serve: reports-build
    cd src/reports/ && npm run preview

reports-serve:
    cd src/reports && npm run dev

build-duckdb:
    #!/usr/bin/env bash
    data_dir="src/reports/.evidence/template/static/data/pesarifu"
    db_file="src/reports/data.duckdb"
    for data_file in $(fd -e parquet . "$data_dir")
    do
        base=$(basename "$data_file")
        name="${base%.parquet}"
        echo $name
        echo $data_file
        echo
        duckdb "$db_file" "create table $name as select * from '$data_file'"
    done
