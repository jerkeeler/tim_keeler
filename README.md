# Tim Keeler's Website

Table of Contents:
- [Development](#development)
- [Deploying](#deploying)
- [Configs](#configs)

## Development

In order to begin development you must do the following:
1. If developing on a Mac make sure you have xcode command line tools installed. Use the following if they are not:
	```bash
	xcode-select --install
	``` 
	- Command line tools are used for access to the `make` command line tool. Make is currently being used solely as a proxy for running the scripts located in the `bin/` directory of this project. If you do not have `make` installed you can run the appropriate scripts in the `bin/` directory instead. 
1. Clone this repository
	```bash
	git clone git@github.com:jerkeeler/tim_keeler.git
	```
1. Create the logs directory and provide it correct permissions
	```bash
	mkdir /var/log/timkeeler
	chown youruser:yourgroup /var/log/timkeeler
	```
1. Install python >= 3.7 using installation method of your choice, I would suggest [pyenv](https://github.com/pyenv/pyenv)
1. Install [virtualenv](https://virtualenv.pypa.io/en/stable/) in your new python environment
1. Create a new virtualenv in this directory and activate it:
	```bash
	python -m virtualenv .venv
	source .venv/bin/activate
	```
1. Install [nodejs](https://nodejs.org/en/) and then install yarn using npm
	```bash
	npm install -g yarn
	```
1. Now install all requirements for this project by running the following:
	```bash
	make requirements
	# OR
	./bin/make_requirements
	```
1. Create a `tim_keeler/confg/settings.toml` file and fill in the settings with values (see configs section for requireed config values and example file structure)
1. Run the Django migrations
	```bash
	./manage.py migrate
	```
1. At this point you should be setup and able to run and develop the website locally. Run the following commands then visit [localhost:8000](localhost:8000) to view the site.
	```bash
	./manage.py runserver
	```

## Deploying

Luckily for you, deploying has been made easy using [Fabric](https://www.fabfile.org). All you need to do to deploy is to get an account on the host box, create `tim_keeler/conf/remote.toml` and fill it in with the required values (see [configs section](#configs) for example file). Once that is setup you can run the following commands whenever you want to deploy. Note that the remote box will always pull from the `master` branch so make sure you have committed any changes, merged to `master`, and pushed to `origin` before deploying.

All commands for deploying are located in the `fabfile.py` file. To run any of the commands prefix them with `fab`. If we want to run the "example" command we would run the following from our command line: `fab example`. Below is the list of commands that exist in the fabfile with brief descriptions of what each one does:

#### deploy

Usage: 
```bash
fab deploy
```

This command will deploy the master branch to the remote host. 

IMPORTANT: You must also be on the master branch locally(!) otherwise there is a chance that you will deploy static files (js, css) that are not on the master branch. There should eventually be a check in the fabfile that prevents this.

The command does the following:
1. Runs `make build` locally
1. Tarballs the `dist/` directory locally
1. On the remote host runs `git pull`, `pip install`, and `./manage.py migrate`
1. Copies over the tarball to the remote host and unpacks into the `dist/` directory there
1. Restarts all services
1. Cleans up tarball

#### download_log

Usage: 
```bash
fab download_log <log_name>
```

Downloads the requested log file to `/tmp/<log_name>.log`. log_name should be either "info" or "error"

#### logs

Usage: 
```bash
fab logs <log_name>
```

Downloads the request log file locally then runs `less` on the logs so that you can view them. After you exit less it will clean up the log files. In essence it's a way to view the log files without having to log into the box.

#### hostname

Usage: 
```bash
fab hostname
```

Runs the `hostname` command on the remote host. Used for testing.

## Configs

### settings.toml

```toml
[app]
allowed_hosts = [
    "*",
]
debug = true
environment = "DEV"
name = "timkeeler.net"
secret_key = "youmustchangethisvalue"

[db]
name = "db"

[email]
from = "example@example.com"
host = "smtp.example.com"
password = "examplepassword"
port = 587
tls = true
username = "example"

[captcha]
secret_key = "captcha_secret_key"
site_key = "captcha_site_key"

[[admins]]
email = "admin1@example.com"
name = "admin1"

[[admins]]
email = "admin2@example.com"
name = "admin2"
```

### remote.toml

```toml
app_location = '/path/to/app/on/server'
gunicorn_process_name = 'process_name'
host = 'example.com'
```
