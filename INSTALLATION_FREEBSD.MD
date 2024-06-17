# Install pre-requisite packages

# Install Python3

`pkg install python311-3.11.8`

# Install Poetry

Fetch the installation script.

`fetch https://install.python-poetry.org`

Execute the script to install poetry.

`python3.11 install.python-poetry.org`

Add poetry installation directory to path (exact command depends on your shell).

Check that poetry is working

`poetry --version`

Remove the script to install poetry.

`rm install.python-poetry.org`

# Install PostgreSQL

Install the client, server and associated packages.

`pkg install postgresql15-server-15.5_2 postgresql15-client-15.5`

Enable PostgreSQL

`sysrc postgresql_enable=YES`

Initialize database server

`/usr/local/etc/rc.d/postgresql initdb`

Start the database server

`/usr/local/bin/pg_ctl -D /var/db/postgres/data15 -l logfile start`

# Install Nginx

`pkg install nginx-full-1.24.0_4,3`

# Configure the firewall

## Start the NGinx service

`service nginx start`

`/usr/local/etc/nginx/nginx.conf` 

# Install GIT

`pkg install git`

# Clone the current build

`git clone https://gitlab.com/fdemian/reactive-bb-build.git`

