# Events API


# Private Deploy

```
python3 -m venv .env
source .env/bin/activate
export DATABASE_URL=postgresql+psycopg2://admin:YOUR_PASSWORD@localhost:5432/events_db

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
CREATE USER admin WITH ENCRYPTED PASSWORD 'YOUR_PASSWORD';
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

```
Copy [this code](https://github.com/eg-informatique/events-api/blob/main/app/SQL%20Tables)

```
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
adduser tm
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
CREATE USER admin WITH ENCRYPTED PASSWORD 'YOUR_PASSWORD';
\c events_db;

```
Copy [this code](app/SQL Tables)

```
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
Environment="DATABASE_URL=postgresql+psycopg2://admin:YOUR_PASSWORD@localhost:5432/events_db"
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
server {
        server_name events-api.org www.events-api.org;

        location / {
                include proxy_params;
                add_header 'Access-Control-Allow-Origin' '*';
                add_header 'Access-Control-Allow-Credentials' 'true';
                add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
                add_header 'Access-Control-Allow-Headers' 'DNT, User-Agent, X-Request-With, If-Modified-Since, Cache-Control, Content-Type, Range' always;
                add_header 'Access-Control-Allow-Expose-Headers' 'Content-Lenght, Content-Range';
                proxy_pass http://unix:home/tm/events-api/events-api.sock;
        }

        location /static/ {
                alias /var/www/;
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
