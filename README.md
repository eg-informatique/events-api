# Events API


# Private Deploy

```
python3 -m venv .env
source .env/bin/activate
export DATABASE_URL=admin:StendeRmqten@localhost:5423/events_db

pip install -r requirements.txt

vi .flaskenv

---
FLASK_APP=events-app.py
FLASK_ENV=development
---

flask run

```

## Tutorials

* https://blog.teclado.com/first-rest-api-flask-postgresql-python/
* https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application


# Private setup

Creation of the virtual environment

```
sudo apt install python3.10-venv
python3 -m venv .env
source .env/bin/activate
deactivate

```
Installation of Postgresql server

```
sudo apt install postgresql-14
sudo -u postgres psql

---
CREATE DATABASE events_db;
CREATE USER admin WITH ENCRYPTED PASSWORD 'StendeRmaten';
\c events_db;
\q
---

sudo nano /etc/postgresql/14/main/pg_hba.conf

---
host    all             all             127.0.0.1/32            trust
---

```
Database configuration

```
sudo -u postgres psql

---
\c events_db

CREATE TABLE venue (
    id uuid DEFAULT gen_random_uuid(),
    name VARCHAR(64) NOT NULL,
    url TEXT DEFAULT NULL,
    address VARCHAR(64) DEFAULT NULL,
    zipcode VARCHAR(64) NOT NULL,
    city VARCHAR(64) NOT NULL,  
    country VARCHAR(64) NOT NULL,
    email VARCHAR(64) NOT NULL,
    phone VARCHAR(16) NOT NULL,
    PRIMARY KEY (id) 
);

CREATE TABLE app_user (
    id uuid DEFAULT gen_random_uuid(),
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    username VARCHAR(16) NOT NULL,
    birth_date DATE NOT NULL,
    email VARCHAR(64) NOT NULL,
    mobile VARCHAR(16) NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE event (
    id uuid DEFAULT gen_random_uuid(),
    title VARCHAR(256) NOT NULL,
    img_url VARCHAR(256) DEFAULT NULL,  
    start_datetime TIMESTAMPTZ NOT NULL,
    end_datetime TIMESTAMPTZ NOT NULL,  
    created TIMESTAMPTZ NOT NULL,
    update TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    venue uuid NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (venue) REFERENCES venue (id)
);

CREATE TABLE event_details (
    id uuid DEFAULT gen_random_uuid(),
    event uuid NOT NULL,
    prices JSON DEFAULT NULL,
    description TEXT NOT NULL,
    organizer uuid NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (event) REFERENCES event (id),
    FOREIGN KEY (organizer) REFERENCES app_user (id)
);

GRANT insert, update, select, delete ON ALL tables IN schema public TO admin;
---

```

# Server setup

## Tutorials 

* https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04
* https://youtu.be/KWIIPKbdxD0?si=ehg_5wYzonSt17Pi
* https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-22-04

## Python setup

Creation of new user 

```
sudo usermod -aG sudo tm
su - tm

```
Instalation of different application

```
sudo apt install pip
sudo apt install python3.10-venv

```
Creation of the virtual environment

```
cd events-api
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
deactivate

```
## Postgres setup

Instalation of postgres 

```
sudo apt install postgresql-14
sudo -u postgres psql

```
Setup the database

```
CREATE DATABASE events_db;
CREATE USER admin WITH ENCRYPTED PASSWORD 'StendeRmaten';
\c events_db;
CREATE TABLE venue (
    id uuid DEFAULT gen_random_uuid(),
    name VARCHAR(64) NOT NULL,
    url TEXT DEFAULT NULL,
    address VARCHAR(64) DEFAULT NULL,
    zipcode VARCHAR(64) NOT NULL,
    city VARCHAR(64) NOT NULL,  
    country VARCHAR(64) NOT NULL,
    email VARCHAR(64) NOT NULL,
    phone VARCHAR(16) NOT NULL,
    PRIMARY KEY (id) 
);

CREATE TABLE app_user (
    id uuid DEFAULT gen_random_uuid(),
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    username VARCHAR(16) NOT NULL,
    birth_date DATE NOT NULL,
    email VARCHAR(64) NOT NULL,
    mobile VARCHAR(16) NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE event (
    id uuid DEFAULT gen_random_uuid(),
    title VARCHAR(256) NOT NULL,
    img_url VARCHAR(256) DEFAULT NULL,  
    start_datetime TIMESTAMPTZ NOT NULL,
    end_datetime TIMESTAMPTZ NOT NULL,  
    created TIMESTAMPTZ NOT NULL,
    update TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    venue uuid NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (venue) REFERENCES venue (id)
);

CREATE TABLE event_details (
    id uuid DEFAULT gen_random_uuid(),
    event uuid NOT NULL,
    prices JSON DEFAULT NULL,
    description TEXT NOT NULL,
    organizer uuid NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (event) REFERENCES event (id),
    FOREIGN KEY (organizer) REFERENCES app_user (id)
);
GRANT insert, update, select, delete ON ALL tables IN schema public TO admin;
\q

```
## Setup wsgi

```
nano wsgi.py

---
from app import app

if __name__ == '__main__':
  		 app.run()
---

```
## Setup gunicorn as systemd service 

```
sudo nano /etc/systemd/system/events-api.service

---
[Unit]
Description=Guinicorn instance to serve events-api Flask app
After=network.target

[Service]
User=tm
Group=www-data
WorkingDirectory=/home/tm/events-api
Environment="PATH=/home/tm/events-api/.env/bin"
Environment="DATABASE_URL=postgresql+psycopg2://admin:StendeRmaten@localhost:5432/events_db"
ExecStart=/home/tm/events-api/.env/bin/gunicorn --workers 3 --bind unix:events-api.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
---

sudo systemctl start events-api.service
sudo systemctl enable events-api.service

```
Instalation and configuration of nginx

```
sudo apt install nginx
sudo nano /etc/nginx/sites-available/events-api.conf

---
server{
    	listen 80;
    	server_name events-api.org www.events-api.org;

    	location / {
            	include proxy_params;
            	proxy_pass http://unix:home/tm/events-api/events-api.sock
    	}
}
---

sudo ln -s /etc/nginx/sites-available/events-api.conf /etc/nginx/sites-enabled/
sudo systemctl restart nginx.service

```
## Setup firewall

```
sudo ufw enable
sudo ufw allow "Nginx Full"
sudo ufw allow ssh
sudo chmod 775 /home/tm

```
## Setup SSL for https conections

Install certbot

```
sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot

```
Add a SSL certification to events-api.org

```
sudo certbot --nginx -d events-api.org -d www.events-api.org

```
Activate automatic SSL certification renew

```
sudo certbot renew --dry-run

```
