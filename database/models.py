from datetime import datetime, date

from sqlalchemy import (
    Column,
    Integer,   
    String,
    DECIMAL,
    DateTime,
    Date,
    ForeignKey,
    Text 
)
from sqlalchemy.orm import declarative_base
Base = declarative_base()


# -------------------------
# Users Table
# -------------------------
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.now)


# -------------------------
# Bins Table
# -------------------------
class Bin(Base):
    __tablename__ = "bins"

    bin_id = Column(Integer, primary_key=True, autoincrement=True)
    bin_code = Column(String(20), nullable=False, unique=True)
    location_name = Column(String(100), nullable=False)
    latitude = Column(DECIMAL(10, 7), nullable=False)
    longitude = Column(DECIMAL(10, 7), nullable=False)
    capacity_kg = Column(DECIMAL(10, 2), nullable=False)
    fill_level = Column(DECIMAL(5, 2), default=0)
    waste_type = Column(String(30))
    last_collected = Column(DateTime)
    status = Column(String(20), default="Active")
    created_at = Column(DateTime, default=datetime.now)


# -------------------------
# Vehicles Table
# -------------------------
class Vehicle(Base):
    __tablename__ = "vehicles"

    vehicle_id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_number = Column(String(20), nullable=False, unique=True)
    capacity_kg = Column(DECIMAL(10, 2), nullable=False)
    fuel_efficiency = Column(DECIMAL(10, 2))
    status = Column(String(20), default="Available")
    driver_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)


# -------------------------
# Routes Table
# -------------------------
class Route(Base):
    __tablename__ = "routes"

    route_id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id"))
    route_date = Column(Date, default=date.today)
    total_distance_km = Column(DECIMAL(10, 2), default=0)
    estimated_time_min = Column(DECIMAL(10, 2), default=0)
    estimated_fuel_l = Column(DECIMAL(10, 2), default=0)
    total_waste_kg = Column(DECIMAL(10, 2), default=0)
    status = Column(String(20), default="Planned")
    created_at = Column(DateTime, default=datetime.now)


# -------------------------
# Route Details Table
# -------------------------
class RouteDetail(Base):
    __tablename__ = "route_details"

    route_detail_id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey("routes.route_id"))
    bin_id = Column(Integer, ForeignKey("bins.bin_id"))
    sequence_no = Column(Integer)
    distance_from_previous_km = Column(DECIMAL(10, 2), default=0)
    estimated_arrival_min = Column(DECIMAL(10, 2), default=0)
    waste_collected_kg = Column(DECIMAL(10, 2), default=0)


# -------------------------
# Collections Table
# -------------------------
class Collection(Base):
    __tablename__ = "collections"

    collection_id = Column(Integer, primary_key=True, autoincrement=True)
    bin_id = Column(Integer, ForeignKey("bins.bin_id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id"))
    collection_date = Column(DateTime, default=datetime.now)
    waste_collected_kg = Column(DECIMAL(10, 2), default=0)
    fill_level_before = Column(DECIMAL(5, 2))
    fill_level_after = Column(DECIMAL(5, 2))
    notes = Column(Text)