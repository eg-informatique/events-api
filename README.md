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

# create database events_db;
# create user admin with encrypted password 'StendeRmaten';
# grant all on database events_db to admin;

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
FLASK_ENV=development
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


```
