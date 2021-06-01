# Django + Docker Template
<img src=https://raw.githubusercontent.com/matacoder/matacoder/main/django-docker-sea.png>

This is a magic repository for everyone who wants to start developing and do not want to worry about initial django and docker setup.

## What is included

- Django
- Nginx
- PostgreSQL
- Gunicorn  
- Docker Compose for development
- Docker Compose for production
- Caddy config for fast SSL + domain deploy
- Poetry dependency manager
- Initial entrypoint to take care of django and postgres setup
- Black code formatter
- Basic Workflow for GitHub Actions
- Accounts app with all authorisation forms implemented on Bootstrap 5
- Basic template to test login/logout
- Sign up form
- Main app to immediately start writing your first business logic
- Django Crisp Forms installed and used in accounts app
- Django Debug Toolbar! Analyze SQL on-the-fly

## Why project is named _settings?

Do you know that frustration when you are looking for your setting file directory?

I know! So underscored `_settings` folder is always close to top and easy to find.

## What next step?

Export all your `.env` environment variables with command: 

`set -o allexport; source .env; set +o allexport`

Create your app using:

`python manage.py startapp my_new_app`

Or just use `main` app. It is already here and urls are included!

## What You Develop is What You Get

Just `docker compose up` and you will see your development version at `127.0.0.1:1111`

Restart your django container (using Docker GUI) everytime you make a change in app logic.

Django's templates engine is reloading without container needed to restart

## Fast Deploy Using Docker Context (Manually)

Docker context is a bridge to your remote server to run docker commands on your local pc or mac.

#### STEP 0: Create new context to remote control your server docker (once)

`docker context create new_ip --docker "host=ssh://username@ip"`

#### STEP 1: Switch to remote server docker

`docker context use new_ip`

#### STEP 2: Build image DIRECTLY on remote server (use variables in .env)

`docker build -t username/project:latest .`

#### STEP 3: Down your compose gracefully on remote server

`docker compose -f docker-compose-prod.yaml down`

Here consider deleting static volume if you have static files modified

#### STEP 4: Up your compose, force recreate containers using new image

`docker compose -f docker-compose-prod.yaml up -d --force-recreate`

#### STEP 5: Don't forget to switch back to your local docker

`docker context use default`

# Run your site with Caddy Server

Install [Caddy Server](https://caddyserver.com), replace `example.com` with your domain in `Caddyfile` and run command:

```bash
sudo caddy stop
sudo caddy run
```

Consider adding `caddy` to [linux start up sequence](https://caddy.community/t/want-caddy-to-run-automatically-on-boot/5240).

# Deploy using GitHub Actions (automatically)

You can not use experimental `docker compose` feature in GitHub Actions yet, but `docker-compose` works just fine.

Do not forget to add GitHub secrets for:

- SSH_KEY
- IP_HOST
- SSH_USER

For all other docker-related secrets you can use sole `ENV` secret. Run this command within project:

`base64 -i .env`

That will give you string array very alike SSH key. Save it to `ENV` secret. Now look at workflow.

`RollyPeres/base64-to-path@v1` action will extract this to `.env` file. That is fast and reliable way to export all your environment variable at once.

This is example workflow you need to implement:

```yaml
name: Django-Docker workflow

on:
  push:
    branches:
      - master

jobs:
  magic_deploy:
    name: Deploy to server with remote docker-compose
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - name: Install SSH key to github server
        uses: kielabokkie/ssh-key-and-known-hosts-action@v1.1.0
        with:
          ssh-private-key: ${{ secrets.SSH_KEY }}
          ssh-host: ${{ secrets.IP_HOST }}

      - name: Install latest version of docker with experimental compose support
        run: |
          pip install docker-compose

      - name: Generate env file from Base64 encoded string (base64 -i .env)
        uses: RollyPeres/base64-to-path@v1
        with:
          filePath: ${{ github.workspace }}/.env
          encodedString: ${{ secrets.ENV }}

      - name: Remote docker compose down/up using context (zero files)
        run: |
          docker context create remote --docker "host=ssh://${{ secrets.SSH_USER }}@${{ secrets.IP_HOST }}"
          docker context use remote
          docker image prune -f
          docker-compose --context remote -f docker-compose-prod.yaml down
          docker-compose --context remote -f docker-compose-prod.yaml up -d --build --force-recreate
```
