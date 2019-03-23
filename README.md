# Installation

* `virtualenv -p python3 env`
* `source env/bin/activate`
* `pip install -r requirements`

Create the database, if needed, and tables. Then seed the tables with default
data.

* `python model.py`
* `python seed.py`

Now, run the app,

* `python server.py`
