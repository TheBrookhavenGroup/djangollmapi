# Setting up a web Server for Django LLM API

This document describes how to set up an Ubuntu server to host the Django 
LLM API server.

***

# Setting up an Ubuntu Server for Django

Great Reference: [How to Setup Django](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)

We'll use Nginx, Gunicorn, and Django.

Python 3.9.5 with torch 2.0.1 worked for us.

## Notation: 

Angle brackets indicate where you need to use an appropriate value.  i.e. 
`<ip address>`, or `<domain name>` should be replaced with your ip address 
or domain name.

In shell snippets shown throughout this document the `#` command line 
prompt implies sudo or root access.  The `$` command line prompt implies a 
typical user login, say for user "ubuntu".

### Pre-requisite Knowlege

1. SSH is configured
2. The login username is "ubuntu"

Add this line to the end of /etc/sudoers. You'll have to temporarily change 
the permissions with chmod +w /etc/sudoers and then after editing change it 
back with chmod -w /etc/sudoers.

`ubuntu ALL=(ALL) NOPASSWD:ALL`

You may want to put your public ssh key in `/home/django/ssh/authorized_keys`
so you can login without a password.

In many of the config files the assumed Ubuntu user is "ubuntu".  That may 
be different for your account.  For example Paperspace conifgures the default 
user for their Ubuntu CPUs to be "paperspace", go figure.

## Copy this repo using git clone

```bash
$ cd
$ git clone https://github.com/TheBrookhavenGroup/djangollmapi.git
```

## Create config file

Create a `~/.djangollmapi` file with the appropriate settings.  It could 
look like this:

```text
[DJANGO]
DEBUG=True
PROJECT_NAME=Binoculars Live
SECRET_KEY="django-insecure-dt@hl9)ewrj!wdwrmar$c%&yx(g-*yp*ke*kcpdf8+x&*or1^="
ADMIN_URL=36126112845a9778035lecf20e06faa087bcb6d2
DOMAIN=binoculars.live


[POSTGRES]
DB=djangollmapi
USER=postgres
PASS=postgres

[LLM]
MODEL_PACKAGE=binoculars_algo
MODEL1=EleutherAI/pythia-410m
MODEL2=EleutherAI/pythia-410m
```

You may want to set `DEBUG=False`.

## Basic Ubuntu Configuration

Login with root access and upgrade ubuntu and install git. Then login is as 
the "django" user and clone the repo.  Then as root, again, install all 
needed packages as shown in the session below.

  ```shell
  # sudo su -
  # apt update
  # apt upgrade
  # sudo su -
  # xargs -a ~/djangollmapi/server_files/packages.txt sudo apt-get 
  install
  # exit
  ```

Restart the server.

## UFW (Uncomplicated Firewall)

AWS provides a firewall for EC2 instances so it is not recommended to set 
one up there.  If deploying elsewhere, say Digital Ocean then it may be a 
good idea to configure UFW as follows. 

```
$ sudo su -
# ufw default deny incoming
# ufw default allow outgoing
# ufw allow ssh
# ufw allow OpenSSH
# ufw enable
# ufw allow "Nginx Full"
# ufw allow https
# ufw status
# exit
```

The output of that status should look like this:

```
$ sudo ufw status
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere                  
OpenSSH                    ALLOW       Anywhere                  
Nginx Full                 ALLOW       Anywhere                  
443/tcp                    ALLOW       Anywhere                  
22/tcp (v6)                ALLOW       Anywhere (v6)             
OpenSSH (v6)               ALLOW       Anywhere (v6)             
Nginx Full (v6)            ALLOW       Anywhere (v6)             
443/tcp (v6)               ALLOW       Anywhere (v6)

```

## DNS

You can visit your server with a web browser using the default URL assigned 
by your hosting provider.  You should see a generic "Welcome to nginx!" page.
Don't worry yet that it isn't secure.  We'll get an ssl certificate soon to 
secure it.

You can setup your DNS "A" record now if you have registered a domain name.

`A @ <your server ip address>`

That may take some time, hours, to take effect.  Once it does then 
`http://<your domain name>` should resolve to the page displayed by Nginx on 
this server.

## Postgres

 
### Create a database:

  ```
  $ sudo -u postgres psql
  
  postgres=# CREATE DATABASE djangollmapi;
  postgres=# CREATE USER postgres with password 'postgres';
  postgres=# ALTER ROLE postgres SET client_encoding TO 'utf8';
  postgres=# ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
  postgres=# ALTER ROLE postgres SET timezone TO 'UTC';
  postgres=# GRANT ALL PRIVILEGES ON DATABASE djangollmapi TO postgres;
  postgres=# alter user postgres PASSWORD 'postgres';
  postgres=# alter user postgres createdb;
  postgres=# 
  postgres=# \q
  ```

It is ok to use "postgres" for the username and password.  It is presumed 
that the server is behind a firewall with postgres ports blocked.  Only 
users on this server should have access to postgres.  If that makes you 
uncomfortable then change it to anything you like and update the `~/.djangollmapi` config file.

## Set up pyenv

Follow the instructions at [pyenv-installer](https://github.
com/pyenv/pyenv-installer) to get pyenv.

Then install a late version of python with it and create a virtual 
environment for djangollcapi as follows:

```
  $ pyenv install 3.12.3
  $ pyenv shell 3.12.3
  $ pyenv virtualenv djangollmapi
  $ pyenv global djangollmapi
  $ pip install --upgrade pip
```

## Install Required Packages and Migrate Django Models

```
$ cd
$ pyenv shell djangollmapi
$ cd ~/djangollmapi
$ pip install -r requirements.txt
$ python manage.py collectstatic --noinput
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
```

In the last step when creating superuser just answer the questions and it 
will create the first django user with admin rights.

## Redis

This was installed earlier when Ubuntu packages were installed.  There 
shouldn't  be anything else to do.  You may have to add user ubuntu to 
the redis group in /etc/group.

## Celery

Configure the Celery service as follows:

```
$ sudo su -
# cp /home/ubuntu/djangollmapi/server_files/etc/systemd/system/celery.service /etc/systemd/system/
# cp /home/ubuntu/djangollmapi/server_files/etc/systemd/system/celeryserial.service /etc/systemd/system/
# mkdir /etc/conf.d
# cp /home/ubuntu/djangollmapi/server_files/etc/conf.d/celery /etc/conf.d/
# cp /home/ubuntu/djangollmapi/server_files/etc/tmpfiles.d/celery.conf /etc/tmpfiles.d/ 
# mkdir /var/log/celery
# chown ubuntu:ubuntu /var/log/celery
# systemctl enable celery
# systemctl enable celeryserial
# sudo systemctl daemon-reload
```

Note: you can use wildcards with systemctl like this `sudo systemctl restart 'celery*'`.

## GUnicorn

```shell
$ sudo su -
# cd /etc/systemd/system/
# cp /home/ubuntu/djangollmapi/server_files/etc/systemd/system/gunicorn.service ./
# cp /home/ubuntu/djangollmapi/server_files/gunicorn_conf.py ~/
# mkdir /var/log/gunicorn
# chown ubuntu /var/log/gunicorn
# sudo systemctl daemon-reload
# systemctl enable gunicorn
# systemctl start gunicorn
# exit
$ cd
$ cd djangollmapi
$ ls
```

At this point you should see the `djangollmapi.sock` file in the ls listing.

## Get https certificates

We'll use [letsencrypt](http://letsencrypt.org)
because it is free and works well.

Reference: [certbot install directions](https://certbot.eff.org/lets-encrypt/ubuntufocal-nginx)

Before we start we need to make sure the server is answering for our domain.
Make sure to start nginx with default values.  Later we'll change them for Django.

```shell
$ sudo su 
# ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
# systemctl restart nginx
```


Install and run letsencrypt certbot:

```shell
$ sudo snap install core
$ sudo snap refresh core
$ sudo apt update
$ sudo snap install --classic certbot
$ sudo certbot certonly --nginx
```

For some reason this command sometimes adds the appropriate references to
the end of each config file in `/etc/nginx/sites-available/`.  I copied the records
from the ones in our repo.  We should not have to do this.

## Nginx

Copy site config files from repo.

```shell
$ sudo su
# cp /home/ubuntu/djangollmapi/server_files/etc/nginx/sites-available/djangollmapi.nginx /etc/nginx/sites-available/
# ln -s /etc/nginx/sites-available/djangollmapi.nginx /etc/nginx/sites-enabled/
# rm /etc/nginx/sites-enabled/default
```

Don't forget to set the host domain name in the `server` `if` block in 
`djangollmapi.nginx`. 

```shell
# systemctl restart nginx
# systemctl restart gunicorn.service 
```

## Install Dependent LLM Algorithm Package

For documentation purposes we'll use the `tbg_llm_example` package.  You can 
replace that with your own package.

```shell
$ cd
$ git clone git@github.com:TheBrookhavenGroup/tbg_llm_example.git
$ pyenv shell djangollmapi
$ pip install ./tbg_llm_example/
```

## Configure Django LLM API

Copy django `djangollmapi/djangollmapi/example_djangollmapi.config` to 
`/home/ubuntu/.djangollmapi` and edit it.  Set the parameters appropriately. 
The `LLM MODEL_PACKAGE` parameter would be "tbg_llm_example" or whatever 
algortihm package you are using.


### Nginx-ulitimate-bad-bot-blocker

Ref: `https://github.com/mitchellkrogza/nginx-ultimate-bad-bot-blocker`

This uses databases that are frequently updated to block traffic from known bad actors.

```bash
$ sudo su -
# wget https://raw.githubusercontent.com/mitchellkrogza/nginx-ultimate-bad-bot-blocker/master/install-ngxblocker -O /usr/local/sbin/install-ngxblocker
# cd /usr/local/sbin
# chmod +x install-ngxblocker
# ./install-ngxblocker
# ./install-ngxblocker -x
# chmod +x setup-ngxblocker
# chmod +x update-ngxblocker
# ./setup-ngxblocker -x -e nginx
# nginx -t
# nginx -s reload
# service nginx reload
# service nginx restart
```

Note: used `-e nginx` arg with `setup-ngxblocker` because that is the extension we use on our nginx config files.

Add this line to the crontab:

`13 22 * * * root /usr/local/sbin/update-ngxblocker -e <your email address>`

Try tests suggested at the end of the github home page.

If you don't have email you can use this not as good approach:

`13 22 * * * root /usr/local/sbin/update-ngxblocker -n`


## Add a few housekeeping items to /etc/crontab

### Crontab

These three lines should be added to /etc/crontab.  That file is in the repo.

```shell
0 21 * * * ubuntu /home/ubuntu/djangollmapi/scripts/pg_backup.bash
55 15 * * * root /usr/bin/certbot renew --renew-hook 'service nginx reload'
39 22 * * * root /usr/local/sbin/update-ngxblocker
```

Sometimes certbot is installed in `/snap/bin` so you may need to do this:
```shell
$ sudo su -
# cd /usr/bin
# ln -s /snap/bin/certbot
```

### pg_dumps

Need a pg_dumps dir for the cron'd `pg_backup.bash` script.

```shell
$ mkdir /home/ubuntu/pg_dumps/
```

### redis_dumps

Redis seems to dump automatically and frequently.  So, backing
it up just means copying the dump file.  You can download the 
`/var/lib/redis/dumps.rdb` as needed.


## Log Files

The `/var/log/celery/serial.log` is where you can see logging done by the 
celery tasks running the algorithm.

The `/var/log/nginx/access.log` is where you can see server requests.

## Algorithm Update Workflow

Suggestion: write a bash script for these steps with the given algorithm 
package name and put it in `~/update_algo.bash` and `chmod +x ~/update_algo.
bash`.  Then from your localhost you can run `ssh ubuntu@<hostname> update_algo.bash`.

```bash
#!/usr/bin/env bash
source ~/.bash_profile
source ~/.bashrc
pyenv shell djangollmapi
pip uninstall -y tbg_llm_example
pip install git+ssh://git@github.com/TheBrookhavenGroup/tbg_llm_example.git
sudo systemctl restart gunicorn.service
sudo systemctl restart celery.service
sudo systemctl restart celeryserial.service
```

If you use a different algorithm package package replace 
`tbg_llm_example` with the alternative package repo url in steps above.

REMEMBER: set the algorithm parameters in `~/.djangollmapi`.

You can watch log output from the algorithm in the serial celery log:

```bash
ssh ubuntu@<hostname> tail -f /var/log/celery/serial.log
```

# Try it!
