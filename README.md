# Installation

* `virtualenv -p python3 env`
* `source env/bin/activate`
* `pip install -r requirements`

Start the database,

* `docker run --name postgres -e POSTGRES_PASSWORD= -p 5432:5432 -d postgres`

Create the database, if needed, and tables. Then seed the tables with default
data.

* `python model.py`
* `python seed.py`

Now, run the app,

* `python server.py`
