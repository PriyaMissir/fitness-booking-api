

from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from datetime import datetime
from zoneinfo import ZoneInfo
import logging


logging.basicConfig(level=logging.INFO)

##### Database setup
DATABASE_URL = "sqlite:///./fitness.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI instance
app = FastAPI()

# Models
class FitnessClass(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date_time = Column(DateTime)
    instructor = Column(String)
    available_slots = Column(Integer)

    bookings = relationship("Booking", back_populates="fitness_class")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    client_name = Column(String)
    client_email = Column(String)

    fitness_class = relationship("FitnessClass", back_populates="bookings")

Base.metadata.create_all(bind=engine)

# Schemas
class FitnessClassOut(BaseModel):
    id: int
    name: str
    date_time: datetime
    instructor: str
    available_slots: int

    class Config:
        from_attributes = True

class BookingRequest(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr

class BookingOut(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: str

    class Config:
        from_attributes = True

# Dependency DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def convert_timezone(dt: datetime, tz: str) -> datetime:
    try:
        return dt.astimezone(ZoneInfo(tz))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid timezone: {tz}")

# API Endpoints
@app.get("/classes", response_model=list[FitnessClassOut])
def get_classes(timezone: str = "Asia/Kolkata", db: Session = Depends(get_db)):
    classes = db.query(FitnessClass).all()
    for c in classes:
        c.date_time = convert_timezone(c.date_time.replace(tzinfo=ZoneInfo("Asia/Kolkata")), timezone)
    return classes

@app.post("/book", response_model=BookingOut)
def book_class(booking: BookingRequest, db: Session = Depends(get_db)):
    fitness_class = db.query(FitnessClass).filter(FitnessClass.id == booking.class_id).first()
    if not fitness_class:
        raise HTTPException(status_code=404, detail="Class not found")
    if fitness_class.available_slots <= 0:
        raise HTTPException(status_code=400, detail="No available slots")

    fitness_class.available_slots -= 1
    new_booking = Booking(**booking.dict())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@app.get("/bookings", response_model=list[BookingOut])
def get_bookings(email: EmailStr = Query(...), db: Session = Depends(get_db)):
    return db.query(Booking).filter(Booking.client_email == email).all()
