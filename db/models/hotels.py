import enum
from typing import List, Set 
from datetime import datetime, date

from sqlalchemy import ForeignKey, Table, Column 
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.types import String, Integer, Date, DateTime, Boolean, Enum 
from sqlalchemy_utils import URLType, EmailType

from .mixins import Timestamp


class Base(DeclarativeBase):
    pass


class Country(Base):
    __tablename__="country"
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, primary_key=True)
    country_name: Mapped[str] = mapped_column("country_name", nullable=False) 
    states: Mapped[List["State"]] = relationship(back_populates="country")
    address: Mapped[List["Address"]] = relationship(back_populates="country")

    def __init__(self, country_name):
        self.country_name = country_name
    
    def __repr__(self) -> str:
        return f"id: {self.id}\t = country: {self.country_name}"


class State(Base):
    __tablename__="state"
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, primary_key=True)
    state_name: Mapped[str] = mapped_column("state_name", String(100), nullable=False)
    country_id: Mapped[int] = mapped_column(Integer(), ForeignKey("country.id"))
    country: Mapped["Country"] = relationship(back_populates="states")
    cities: Mapped[List["City"]] = relationship(back_populates="state")
    address: Mapped[List["Address"]] = relationship(back_populates="state")

    def __init__(self, statte_name, country_id):
        self.state_name = statte_name
        self.country_id = country_id
    
    def __repr__(self) -> str:
        return f"id: {self.id}\t = state: {self.state_name}"


class City(Base):
    __tablename__="city"
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, primary_key=True)
    city_name: Mapped[str] = mapped_column("city_name", String(150), nullable=False)
    state_id: Mapped[int] = mapped_column(Integer(), ForeignKey("state.id"))
    state: Mapped["State"] = relationship(back_populates="cities")
    address: Mapped[List["Address"]] = relationship(back_populates="city")

    def __init__(self, city_name, state_id):
        self.city_name = city_name
        self.state_id = state_id
    
    def __repr__(self):
        return f"City: {self.id}:\t{self.city_name}"


class Hotel(Timestamp, Base):
    __tablename__="hotel"
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, primary_key=True)
    city_id: Mapped[int] = mapped_column(Integer(), ForeignKey("city.id"), nullable=False)
    hotel_name: Mapped[int] = mapped_column("hotel_name", String(100), nullable=False)
    web_address: Mapped[URLType] = mapped_column("web_address", URLType(), nullable=False)
    stars: Mapped[int] = mapped_column("stars", Integer(), nullable=False)
    address: Mapped[str] = mapped_column("address", String(1000), nullable=False)
    description: Mapped[str] = mapped_column("description", String(2000))
    manager: Mapped[str] = mapped_column("manager", String(150))
    city: Mapped["City"] = relationship(back_populates= "hotels")
    rooms: Mapped[Set["Rooms"]] = relationship(back_populates="hotel")

    def __init__(self, city_id, hotel_name, stars, address, description, manager):
        self.city_id = city_id
        self.hotel_name = hotel_name
        self.stars = stars
        self.address = address
        self.description = description
        self.manager = manager
    
    def __repr__(self) -> str:
        return f"Hotel {self.hotel_name} is a {self.stars} star hotel located in {self.address}"


class Status(int, enum.Enum):
    available = 0
    not_available = 1


class RoomStatus(Timestamp, Base):
    __tablename__="room_status"
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, primary_key=True)
    status_name: Mapped[Status] = mapped_column("status_name", Enum(Status), nullable=False)
    rooms: Mapped["Rooms"] = relationship(back_populates="status")

    def __init__(self, status_name):
        self.status_name = status_name
    
    def __repr__(self) -> str:
        return f"Status {self.id}: {self.status_name}"


class Floor(Timestamp, Base):
    __tablename__="floor"
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, primary_key=True)
    floor_num: Mapped[int] = mapped_column("floor_num", Integer(), nullable=False)
    rooms: Mapped[Set["Rooms"]] = relationship(back_populates="floor")

    def __init__(self, floor_num):
        self.floor_num = floor_num
    
    def __repr__(self) -> str:
        return f"Floors {self.id}: {self.floor_num}"


# room_class and room_feature many-to-many relationship
room_class_feature = Table(
    "room_class_feature",
    Base.metadata,
    Column("room_class_id", ForeignKey("room_class.id")),
    Column("room_feature_id", ForeignKey("room_features.id"))
)


room_class_bed_type = Table(
    "room_class_bed_type",
    Base.metadata,
    Column("room_class_id", ForeignKey("room_class.id")),
    Column("bed_type_id", ForeignKey("bed_type.id"))
)


class ClassName(int, enum.Enum):
    standard = 1
    suite = 2
    deluxe = 3 


class RoomClass(Timestamp, Base):
    __tablename__="room_class"
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, primary_key=True)
    class_name: Mapped[ClassName] = mapped_column("class_name", Enum(ClassName), nullable=False)
    rooms: Mapped[List["Rooms"]] = relationship(back_populates="clas")
    features: Mapped[List["RoomFeature"]] = relationship(
        secondary=room_class_feature,
        back_populates="clas"
    )
    bedtype: Mapped[List["BedType"]] = relationship(
        secondary=room_class_bed_type,
        back_populates="clas"
    )

    def __init__(self, class_name):
        self.class_name = class_name
    
    def __repr__(self) -> str:
        return f"Classes: {self.id}: {self.class_name}"


class RoomFeature(Timestamp, Base):
    __tablename__="room_features"
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, primary_key=True)
    features: Mapped[str] = mapped_column("features", String(400))
    clas: Mapped[List["RoomClass"]] = relationship(
        secondary=room_class_feature,
        back_populates="features"
    )

    def __init__(self, features):
        self.features = features
    
    def __repr__(self) -> str:
        return f"Features: {self.features}"


class BedTypeName(int, enum.Enum):
    standard = 1
    queen = 2
    king = 3 


class BedType(Timestamp, Base):
    __tablename__="bed_type"
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, primary_key=True)
    bed_type_name: Mapped[BedTypeName] = mapped_column("bed_type_name", Enum(BedTypeName), nullable=False)
    num_beds: Mapped[int] = mapped_column("num_beds", Integer(), nullable=False)
    clas: Mapped[List["RoomClass"]] = relationship(
        secondary=room_class_bed_type,
        back_populates="bedtype"
    )
    
    def __init__(self, bed_type_name, num_beds):
        self.bed_type_name = bed_type_name
        self.num_beds = num_beds
    
    def __repr__(self):
        return f"{self.bed_type_name}: {self.num_beds}"
   

booking_room = Table(
    "room_booking",
    Base.metadata,
    Column("room_id", ForeignKey("rooms.id")),
    Column("booking_id", ForeignKey("booking.id"), unique=True)
)


class Rooms(Timestamp, Base):
    __tablename__="rooms"
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(Integer(), ForeignKey("hotel.id"))
    status_id: Mapped[int] = mapped_column(Integer(), ForeignKey("room_status.id"))
    floor_id: Mapped[int] = mapped_column(Integer(), ForeignKey("floor.id"))
    room_class_id: Mapped[int] = mapped_column(Integer(), ForeignKey("room_class.id"))
    room_number: Mapped[int] = mapped_column("room_number", String(15), nullable=False)
    capacity: Mapped[int] = mapped_column("capacity", Integer(), nullable=False)
    price: Mapped[int] = mapped_column("price", Integer(), nullable=False)

    hotel: Mapped["Hotel"] = relationship(back_populates="rooms")
    status: Mapped["RoomStatus"] = relationship(back_populates="rooms")
    floor: Mapped["Floor"] = relationship(back_populates="rooms")
    clas: Mapped["RoomClass"] = relationship(back_populates="rooms")
    bookings: Mapped[List["Booking"]] = relationship(
        secondary=booking_room,
        back_populates="room"
    )

    def __init__(self, hotel_id, status_id, floor_id, room_class_id, room_number, capacity, price):
        self.hotel_id = hotel_id
        self.status_id = status_id
        self.floor_id = floor_id
        self.room_class_id = room_class_id
        self.room_number = room_number
        self.capacity = capacity
        self.price = price

    def __repr__(self) -> str:
        return f"Room {self.room_number} with {self.capacity} capacity is ${self.price}"


class UserInfo(Timestamp, Base):
    __tablename__="user_info"
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column("first_name", String(70), nullable=False)
    last_name: Mapped[str] = mapped_column("last_name", String(100), nullable=False)
    social_security_num: Mapped[str] = mapped_column("social_security_num", String(10), nullable=False, unique=True)
    phone_num: Mapped[str] = mapped_column("phone_num", String(11), nullable=False, unique=True)
    email: Mapped[EmailType] = mapped_column("email", EmailType, nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="user_info")

    def __init__(self, first_name, last_name, social_security_num, phone_num, email):
        self.first_name = first_name
        self.last_name = last_name
        self.social_security_num = social_security_num
        self.phone_num = phone_num
        self.email = email
    
    def __repr__(self) -> str:
        return f"User {self.first_name} {self.last_name}: ssn: {self.social_security_num}, phone: {self.phone_num}, email: {self.email}"


address_user = Table(
    "address_user",
    Base.metadata,
    Column("users_id", ForeignKey("users.id")),
    Column("address_id", ForeignKey("address.id"))
)


class Address(Timestamp, Base):
    __tablename__="address"
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, primary_key=True)
    country_id: Mapped[int] = mapped_column(Integer(), ForeignKey("country.id"))
    state_id: Mapped[int] = mapped_column(Integer(), ForeignKey("state.id"))
    city_id: Mapped[int] = mapped_column(Integer(), ForeignKey("city.id"))
    address_line1: Mapped[str] = mapped_column("address_line1", String(200), nullable=False)
    address_line2: Mapped[str] = mapped_column("address_line2", String(200))
    street: Mapped[str] = mapped_column("street", String(100), nullable=False)
    unit_num: Mapped[int] = mapped_column("unit_num", Integer(), nullable=False)
    country: Mapped["Country"] = relationship(back_populates="address")
    state: Mapped["State"] = relationship(back_populates="address")
    city: Mapped["City"] = relationship(back_populates="address")
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey("users.id"))
    user: Mapped[List["User"]] = relationship(
        secondary=address_user,
        back_populates="address",
    )

    def __init__(self, country_id, state_id, city_id, address_line1, address_line2, street, unit_num):
        self.country_id = country_id
        self.state_id = state_id
        self.city_id = city_id
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.street = street
        self.unit_num = unit_num
    
    def __repr__(self) -> str:
        return f"Address: {self.address_line1} {self.address_line2}, {self.street}, {self.unit_num}"


class User(Timestamp, Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column("id", Integer(),autoincrement=True, primary_key=True)
    user_name: Mapped[str] = mapped_column("user_name", String(170), nullable=False, unique=True)
    password: Mapped[str] = mapped_column("password", String(100), nullable=False)
    user_info: Mapped["UserInfo"] = relationship(back_populates="user")
    booking: Mapped["Booking"] = relationship(back_populates="users")
    address: Mapped[List["Address"]] = relationship(
        secondary=address_user,
        back_populates="user",
    )

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password
    
    def __repr__(self) -> str:
        return f"Users: {self.user_name}"


class Booking(Timestamp, Base):
    __tablename__="booking"
    id: Mapped[int] = mapped_column("id", Integer(), autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey("users.id"))
    booking_price: Mapped[int] = mapped_column("booking_price", Integer(), nullable=False)
    room_id:Mapped[int] = mapped_column(Integer(), ForeignKey("rooms.id"), nullable=False)
    reverved_at: Mapped[datetime] = mapped_column("reserved_at", DateTime(), default=datetime.utcnow)
    checkin_date: Mapped[date] = mapped_column("checkin_date", Date(), nullable=False)
    checkout_date: Mapped[date] = mapped_column("checkout_date", Date(), nullable=False)
    adult_num: Mapped[int] = mapped_column("adult_num", Integer(), nullable=False)
    children_num: Mapped[int] = mapped_column("children_num", Integer(), nullable=False)
    paid_status: Mapped[bool] = mapped_column("paid_status", Boolean(), nullable=False)
    users: Mapped["User"] = relationship(back_populates="booking")
    room: Mapped[List["Rooms"]] = relationship(
        secondary=booking_room,
        back_populates="bookings"
    )

    def __init__(self, user_id, booking_price, room_id, checkin_date, checkout_date, adult_num, children_num, paid_status):
        self.user_id = user_id
        self.booking_price = booking_price
        self.room_id = room_id
        self.checkin_date = checkin_date
        self.checkout_date = checkout_date
        self.adult_num = adult_num
        self.children_num = children_num
        self.paid_status = paid_status
    
    def __repr__(self) -> str:
        return f"checking data: {self.checkin_date}, checkout date: {self.checkout_date}"

