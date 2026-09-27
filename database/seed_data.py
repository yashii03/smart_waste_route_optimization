from datetime import datetime

from sqlalchemy.orm import sessionmaker

from database.connection import engine
from database.models import Base, User, Bin, Vehicle


# Create database tables if they don't exist
Base.metadata.create_all(engine)

# Create database session
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


# -------------------------
# Demo User
# -------------------------
user = User(
    username="admin",
    password_hash="demo123",
    role="admin"
)

session.add(user)


# -------------------------
# Sample Vehicles
# -------------------------
vehicles = [
    Vehicle(
        vehicle_number="GJ01AB1001",
        capacity_kg=5000,
        fuel_efficiency=4.5,
        status="Available",
        driver_name="Driver 1"
    ),
    Vehicle(
        vehicle_number="GJ01AB1002",
        capacity_kg=4000,
        fuel_efficiency=5.0,
        status="Available",
        driver_name="Driver 2"
    ),
    Vehicle(
        vehicle_number="GJ01AB1003",
        capacity_kg=6000,
        fuel_efficiency=4.0,
        status="Available",
        driver_name="Driver 3"
    )
]

session.add_all(vehicles)


# -------------------------
# Sample Waste Bins
# -------------------------
bins = [
    Bin(
        bin_code="BIN001",
        location_name="Zone A",
        latitude=23.0225,
        longitude=72.5714,
        capacity_kg=100,
        fill_level=85,
        waste_type="Mixed",
        last_collected=datetime.now(),
        status="Active"
    ),
    Bin(
        bin_code="BIN002",
        location_name="Zone B",
        latitude=23.0325,
        longitude=72.5814,
        capacity_kg=120,
        fill_level=65,
        waste_type="Organic",
        last_collected=datetime.now(),
        status="Active"
    ),
    Bin(
        bin_code="BIN003",
        location_name="Zone C",
        latitude=23.0125,
        longitude=72.5614,
        capacity_kg=150,
        fill_level=92,
        waste_type="Mixed",
        last_collected=datetime.now(),
        status="Active"
    ),
    Bin(
        bin_code="BIN004",
        location_name="Zone D",
        latitude=23.0425,
        longitude=72.5914,
        capacity_kg=100,
        fill_level=45,
        waste_type="Plastic",
        last_collected=datetime.now(),
        status="Active"
    ),
    Bin(
        bin_code="BIN005",
        location_name="Zone E",
        latitude=23.0525,
        longitude=72.6014,
        capacity_kg=200,
        fill_level=78,
        waste_type="Mixed",
        last_collected=datetime.now(),
        status="Active"
    ),
    Bin(
        bin_code="BIN006",
        location_name="Zone F",
        latitude=23.0025,
        longitude=72.5514,
        capacity_kg=120,
        fill_level=95,
        waste_type="Organic",
        last_collected=datetime.now(),
        status="Active"
    ),
    Bin(
        bin_code="BIN007",
        location_name="Zone G",
        latitude=23.0625,
        longitude=72.6114,
        capacity_kg=150,
        fill_level=30,
        waste_type="Plastic",
        last_collected=datetime.now(),
        status="Active"
    ),
    Bin(
        bin_code="BIN008",
        location_name="Zone H",
        latitude=23.0725,
        longitude=72.6214,
        capacity_kg=100,
        fill_level=88,
        waste_type="Mixed",
        last_collected=datetime.now(),
        status="Active"
    ),
    Bin(
        bin_code="BIN009",
        location_name="Zone I",
        latitude=22.9925,
        longitude=72.5414,
        capacity_kg=180,
        fill_level=55,
        waste_type="Organic",
        last_collected=datetime.now(),
        status="Active"
    ),
    Bin(
        bin_code="BIN010",
        location_name="Zone J",
        latitude=23.0825,
        longitude=72.6314,
        capacity_kg=100,
        fill_level=97,
        waste_type="Mixed",
        last_collected=datetime.now(),
        status="Active"
    )
]

session.add_all(bins)


# Save everything
session.commit()

print("Sample data inserted successfully! 🚛♻️")

session.close()