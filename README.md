## Hotel room Reservation API with SQLAlchemy, PostgreSQL, FastAPI

In this project I created a backend for a hotel reservation website using "SQLAlchemy", "PostgreSQL" and "FaseAPI".
There is an schematic image of database created by pgadmin that shows the dynamic of database (database was created by sqlalchemy and schematic was done by pgadmin)
I have not add all possibly needed routes for website and just added 10 different routers including searching for hotels, rooms, booking rooms etc.

NOTE: before running the project add a file to db directory: db_info.py  with the following format:

from sqlalchemy import URL
url_object = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres-username",
    password="user's password",
    host="localhost",
    port=5432,
    database="database name"
)

NOTE: you don't need to create the database beforehand, just give it a name and it will be created with all the tables and relations.

# To run the project
after adding the db_info.py file:
in the root directory, run: uvicorn main:app --reload
