from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .db_info import url_object
from db.models.hotels import (
    Floor,
    RoomClass,
    BedType
)


def injection():
    engine = create_engine(url=url_object, echo=True)
    with Session(bind=engine) as session:
        for i in range(1, 100):
            floor = Floor(floor_num=i)
            session.add(floor)
            session.flush()
        session.commit()

    with Session(bind=engine) as session:
        standard = RoomClass(class_name='standard')
        session.add(standard)
        session.flush()
        suite = RoomClass(class_name="suite")
        session.add(suite)
        session.flush()   
        deluxe = RoomClass(class_name="deluxe")
        session.add(deluxe)
        session.flush()
        session.commit()

    with Session(bind=engine) as session:
        standard = BedType(bed_type_name="standard")
        session.add(standard)
        session.flush()
        queen = BedType(bed_type_name="queen")
        session.add(queen)
        session.flush()   
        king = BedType(bed_type_name="king")
        session.add(king)
        session.flush()
        session.commit()
