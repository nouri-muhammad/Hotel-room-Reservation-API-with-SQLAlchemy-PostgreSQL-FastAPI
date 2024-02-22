from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from .db_info import url_object
from .models import hotels


engine = create_engine(url=url_object)

if not database_exists(engine.url):
    print("Database does not exist!\nCreating the database and tables.")
    create_database(engine.url)
    hotels.Base.metadata.create_all(bind=engine)
else:
    print("Databse already Exists!")

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
