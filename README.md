# Events API


# Deploy

```
python3 -m venv .env
source .env/bin/activate

pip install -r requirements.txt

```

# Setup

Creation of the virtual environment

```
python3 -m venv .env
source .env/bin/activate

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



```
