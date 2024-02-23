#!/usr/bin/env -S just --working-directory . --justfile

DEPLOY_LOC := "linuxuser@horo"

app-run:
    # sudo systemctl start postgresql.service
    litestar --app pesarifu.api.app:app run --host 127.0.0.1 --port 3005

app-run-debug:
    # sudo systemctl start postgresql.service
    litestar --app pesarifu.api.app:app run --host 127.0.0.1 --port 3005 --debug

celery-run: app-setup
    #!/usr/bin/env bash
    source .env
    sudo systemctl restart redis.service
    celery --app $CELERY_APP worker --loglevel INFO --pool=prefork --concurrency=4 --without-mingle --without-heartbeat --logfile=$CELERY_LOG_FILE --pidfile=$CELERY_PID_FILE --task-events --detach

admin-run:
    sudo caddy reverse-proxy --from admin.pesarifu.com --to http://localhost:3000

[confirm("Are you sure want to delete everything?")]
clean: backup
    rm -r uploads/*
    rm -r exports/*

backup:
    tar cvJf uploads.tar.xz --directory=uploads .
    tar cvJf exports.tar.xz --directory=exports .

app-setup:
    #!/usr/bin/env bash
    env POETRY_VIRTUALENVS_IN_PROJECT=true poetry install
    npm install
    cat << EOF > .env
    #/usr/bin/env bash
    export PYTHONPATH=$PYTHONPATH:$(poetry env info --path)/lib/python3.10/site-packages
    export ENV_FOR_DYNACONF=production
    export APP_ROOT="$(pwd)"
    export DYNACONF_APP_ROOT="$(pwd)"
    export ROOT_PATH_FOR_DYNACONF="$(pwd)/src/pesarifu/config/"
    export CELERY_APP="pesarifu.config.celery"
    export CELERY_PID_FILE="$(pwd)/.celery.pid"
    export CELERY_LOG_FILE="$(pwd)/logs/celery.log"
    EOF
    source .env
    mkdir -p uploads exports logs static/dist || true

service-setup:
    -sudo ln -s "$(pwd)/services/app.service" /etc/systemd/system/
    -sudo ln -s "$(pwd)/services/tasks.service" /etc/systemd/system/
    sudo systemctl daemon-reload

overview:
    eza --tree --long --group-directories-first --ignore-glob __pycache__ --ignore-glob node_modules --git-ignore

db-stats database:
    #!/usr/bin/env bash
    cat << EOF | psql --dbname={{database}} --file -
    select
        distinct tx.owner_account_id,
        ta.account_name,
        ta.type, count(1) as transaction_count
    from transaction tx
    inner join transactional_account ta on tx.owner_account_id = ta.id
    group by
        tx.owner_account_id,
        ta.account_name,
        ta.type
    order by
        transaction_count;
    EOF

tasks:
    rg --ignore-vcs --trim --max-depth 50 --glob '!justfile' 'FIXME|TODO'

deploy:
    #!/usr/bin/env bash
    repo_dir=$(mktemp --directory)
    echo "cloning into $repo_dir"
    git clone https://github.com/julius383/pesarifu.git --depth 1 "$repo_dir"
    rsync --exclude-from=.gitignore --archive --compress --update --progress --cvs-exclude --verbose --perms "${repo_dir}/" {{DEPLOY_LOC}}:pesarifu
    scp -i ~/.ssh/id_ed25519 ./src/pesarifu/config/.secrets.toml {{DEPLOY_LOC}}:pesarifu/src/pesarifu/config/.secrets.toml
    scp -i ~/.ssh/id_ed25519 ./static/dist/pesarifu-logo.svg {{DEPLOY_LOC}}:pesarifu/static/dist/
    scp -i ~/.ssh/id_ed25519 ./src/reports/sources/pesarifu_prod/connection.yaml {{DEPLOY_LOC}}:pesarifu/src/reports/sources/pesarifu/
    scp -i ~/.ssh/id_ed25519 ./src/reports/sources/pesarifu_prod/connection.options.yaml {{DEPLOY_LOC}}:pesarifu/src/reports/sources/pesarifu/
    rm -rf "$repo_dir"

lint:
    isort src/
    black src/

setup: app-setup reports-setup service-setup website-setup build-styles
    echo "Running setup"

build-styles:
    npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css

app-serve: build-styles app-run
    echo "serving website"

reports-setup:
    cd src/reports && npm install

reports-build:
    cd src/reports && npm run sources
    cd src/reports && npm run build

reports-build-serve:
    cd src/reports/ && npm run preview

reports-serve:
    cd src/reports && npm run dev

website-setup:
    cd src/website && npm install

website-build:
    cd src/website && npm run build

website-serve:
    cd src/website && npm run start

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
