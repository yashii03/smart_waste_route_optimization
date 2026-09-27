import streamlit as st

from database.connection import engine
from database.models import Vehicle
from sqlalchemy.orm import sessionmaker


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Vehicle Management",
    page_icon="🚛",
    layout="wide"
)

st.title("🚛 Vehicle Management")
st.write("Add and manage waste collection vehicles.")


# -----------------------------
# Database Session
# -----------------------------

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


# -----------------------------
# Add New Vehicle
# -----------------------------

st.subheader("➕ Add New Vehicle")

with st.form("add_vehicle_form"):

    col1, col2 = st.columns(2)

    with col1:

        vehicle_number = st.text_input(
            "Vehicle Number",
            placeholder="Example: GJ01AB1234"
        )

        driver_name = st.text_input(
            "Driver Name",
            placeholder="Example: Rahul Patel"
        )

        capacity_kg = st.number_input(
            "Capacity (kg)",
            min_value=1.0,
            value=500.0
        )

    with col2:

        fuel_efficiency = st.number_input(
            "Fuel Efficiency (km/l)",
            min_value=0.1,
            value=8.0,
            step=0.1
        )

        status = st.selectbox(
            "Status",
            [
                "Available",
                "On Route",
                "Maintenance",
                "Inactive"
            ]
        )

    submitted = st.form_submit_button("➕ Add Vehicle")

    if submitted:

        if not vehicle_number or not driver_name:
            st.error("Please enter Vehicle Number and Driver Name.")

        else:

            existing_vehicle = session.query(Vehicle).filter(
                Vehicle.vehicle_number == vehicle_number
            ).first()

            if existing_vehicle:

                st.error("❌ This Vehicle Number already exists.")

            else:

                new_vehicle = Vehicle(
                    vehicle_number=vehicle_number,
                    capacity_kg=capacity_kg,
                    fuel_efficiency=fuel_efficiency,
                    status=status,
                    driver_name=driver_name
                )

                session.add(new_vehicle)
                session.commit()

                st.success(
                    f"✅ Vehicle {vehicle_number} added successfully!"
                )

                st.rerun()


# -----------------------------
# Vehicle Overview
# -----------------------------

st.divider()

st.subheader("📊 Vehicle Overview")

all_vehicles = session.query(Vehicle).all()

total_vehicles = len(all_vehicles)

available_vehicles = sum(
    1 for v in all_vehicles
    if v.status == "Available"
)

on_route_vehicles = sum(
    1 for v in all_vehicles
    if v.status == "On Route"
)

maintenance_vehicles = sum(
    1 for v in all_vehicles
    if v.status == "Maintenance"
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🚛 Total Vehicles", total_vehicles)

with col2:
    st.metric("🟢 Available", available_vehicles)

with col3:
    st.metric("🔵 On Route", on_route_vehicles)

with col4:
    st.metric("🔧 Maintenance", maintenance_vehicles)


# -----------------------------
# Search & Filter
# -----------------------------

st.subheader("🔎 Search & Filter Vehicles")

col1, col2 = st.columns(2)

with col1:

    search_text = st.text_input(
        "Search",
        placeholder="Vehicle number or driver name..."
    )

with col2:

    status_filter = st.selectbox(
        "Filter by Status",
        [
            "All",
            "Available",
            "On Route",
            "Maintenance",
            "Inactive"
        ]
    )


# -----------------------------
# Apply Filters
# -----------------------------

filtered_vehicles = all_vehicles


if search_text:

    search_text = search_text.lower()

    filtered_vehicles = [
        v for v in filtered_vehicles
        if search_text in v.vehicle_number.lower()
        or search_text in v.driver_name.lower()
    ]


if status_filter != "All":

    filtered_vehicles = [
        v for v in filtered_vehicles
        if v.status == status_filter
    ]


# -----------------------------
# Display Vehicles
# -----------------------------

st.subheader("📋 Existing Vehicles")

st.write(
    f"Showing **{len(filtered_vehicles)}** of "
    f"**{total_vehicles}** vehicles."
)


if filtered_vehicles:

    for vehicle in filtered_vehicles:

        with st.container(border=True):

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.write(f"**🚛 {vehicle.vehicle_number}**")
                st.write(f"👤 Driver: {vehicle.driver_name}")

            with col2:
                st.write(
                    f"📦 Capacity: {vehicle.capacity_kg} kg"
                )

            with col3:
                st.write(
                    f"⛽ Fuel Efficiency: "
                    f"{vehicle.fuel_efficiency} km/l"
                )

            with col4:
                st.write(
                    f"📌 Status: {vehicle.status}"
                )

else:

    st.warning("No vehicles match your search/filter.")


# -----------------------------
# Close Database Session
# -----------------------------

session.close()