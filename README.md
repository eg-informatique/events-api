# Events API


# Deploy

```
python3 -m venv .env
source .env/bin/activate

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


# Setup

Creation of the virtual environment

```
python3 -m venv .env
source .env/bin/activate

sudo apt install postgresql-14

```

Installation of Postgresql server

```
sudo apt install postgresql-14

sudo -u postgres psql

# CREATE DATABASE events_db;
# CREATE USER admin WITH ENCRYPTED PASSWORD 'StendeRmaten';
# GRANT ALL PRIVILEGES ON DATABASE events_db TO admin;
# GRANT SELECT ON ALL TABLES IN schema public TO admin;
# SET timezone = 'posix/Europe/Zurich';
# \c

sudo vi /etc/postgresql/14/main/pg_hba.conf

---
host    all             all             127.0.0.1/32            trust
---

```

Part 1 (Flask configuration)

```
# install flask
pip install flask
mkdir app
cd app

vi __init__.py

--
from flask import Flask

app = Flask(__name__)

from app import routes
--

vi routes.py

--
from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
--

cd ..

vi events-app.py

--
from app import app
--

pip install python-dotenv

vi .flaskenv

--
FLASK_APP=events-app.py
DEV_DB_URL='postgresql+psycopg2://admin:StendeRmqten@localhost:5423/events_db'
FLASK_ENV=development
FLASK_DEBUG=True
--

# export FLASK_APP=myapp.py

flask run
```

Part 2 (Database configuration)

```
# create test table
sudo -u postgres psql

# \c events_db

CREATE TABLE test_user(
id INT PRIMARY KEY,
name VARCHAR(64),
email VARCHAR(64)
);

INSERT INTO test_user(id, name, email) VALUES (1, 'Jim', 'jim@vtn.ch');

# start flask 
# visit http://127.0.0.1:5000/test_users

```
