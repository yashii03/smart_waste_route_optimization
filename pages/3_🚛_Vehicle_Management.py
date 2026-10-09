import streamlit as st
from sqlalchemy.orm import sessionmaker

from database.connection import engine
from database.models import Vehicle


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Vehicle Management",
    page_icon="🚛",
    layout="wide",
)


# ==================================================
# DEEP TEAL THEME (MATCHES DASHBOARD)
# ==================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #062C30 0%, #07383D 45%, #041F23 100%);
        color: #E6FFFB;
    }

    .main {
        background: transparent;
    }

    h1 {
        color: #CCFBF1 !important;
        font-weight: 800;
    }

    h2 {
        color: #99F6E4 !important;
        font-weight: 700;
    }

    h3 {
        color: #A7F3D0 !important;
        font-weight: 650;
    }

    p, label, [data-testid="stCaptionContainer"] {
        color: #B6D9D5;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #05282D, #041F23);
        border-right: 1px solid #155E63;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #CCFBF1 !important;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #0A3D42, #07343A);
        border: 1px solid #176B70;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.18);
    }

    div[data-testid="stMetricLabel"] {
        color: #99F6E4 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #F0FDFA !important;
        font-weight: 800;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #14B8A6, #0D9488);
        color: white;
        border: 1px solid #2DD4BF;
        border-radius: 10px;
        padding: 9px 20px;
        font-weight: 700;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #2DD4BF, #14B8A6);
        color: #042F2E;
        border-color: #5EEAD4;
    }

    input, textarea {
        background-color: #0A3D42 !important;
        color: #E6FFFB !important;
        border-color: #176B70 !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #0A3D42 !important;
        border-color: #176B70 !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #176B70;
        border-radius: 14px;
        overflow: hidden;
    }

    div[data-testid="stForm"] {
        background: rgba(7, 52, 58, 0.62);
        border: 1px solid #176B70;
        border-radius: 16px;
        padding: 20px;
    }

    hr {
        border-color: #155E63;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# PAGE HEADER
# ==================================================

st.title("🚛 Vehicle Management")
st.caption("Manage collection vehicles, drivers, carrying capacity, and availability.")

st.markdown(
    '<div style="background:linear-gradient(135deg,#0A3D42,#07343A);'
    'border:1px solid #176B70;border-radius:16px;padding:16px 20px;'
    'margin:8px 0 20px 0;">'
    '<div style="color:#99F6E4;font-size:13px;font-weight:700;letter-spacing:.5px;">'
    '🚛 FLEET OPERATIONS'
    '</div>'
    '<div style="color:#CCFBF1;font-size:15px;margin-top:5px;">'
    'Register vehicles, monitor availability, and review capacity and fuel efficiency.'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)


# ==================================================
# DATABASE SESSION
# ==================================================

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


# ==================================================
# ADD NEW VEHICLE
# ==================================================

st.subheader("➕ Add New Vehicle")

with st.form("add_vehicle_form", clear_on_submit=False):
    st.caption("Enter vehicle details below. Vehicle Number must be unique.")

    form_col1, form_col2 = st.columns(2)

    with form_col1:
        vehicle_number = st.text_input(
            "Vehicle Number",
            placeholder="Example: GJ01AB1234",
        )

        driver_name = st.text_input(
            "Driver Name",
            placeholder="Example: Rahul Patel",
        )

        capacity_kg = st.number_input(
            "Capacity (kg)",
            min_value=1.0,
            value=500.0,
            step=100.0,
        )

    with form_col2:
        fuel_efficiency = st.number_input(
            "Fuel Efficiency (km/l)",
            min_value=0.1,
            value=8.0,
            step=0.1,
        )

        status = st.selectbox(
            "Status",
            ["Available", "On Route", "Maintenance", "Inactive"],
        )

    submitted = st.form_submit_button(
        "➕ Add Vehicle",
        type="primary",
        use_container_width=True,
    )

    if submitted:
        cleaned_vehicle_number = vehicle_number.strip().upper()
        cleaned_driver_name = driver_name.strip()

        if not cleaned_vehicle_number or not cleaned_driver_name:
            st.error("Please enter both Vehicle Number and Driver Name.")
        else:
            existing_vehicle = session.query(Vehicle).filter(
                Vehicle.vehicle_number == cleaned_vehicle_number
            ).first()

            if existing_vehicle:
                st.error("❌ This Vehicle Number already exists.")
            else:
                new_vehicle = Vehicle(
                    vehicle_number=cleaned_vehicle_number,
                    capacity_kg=capacity_kg,
                    fuel_efficiency=fuel_efficiency,
                    status=status,
                    driver_name=cleaned_driver_name,
                )

                try:
                    session.add(new_vehicle)
                    session.commit()
                    st.success(f"✅ Vehicle {cleaned_vehicle_number} added successfully!")
                    st.rerun()
                except Exception as exc:
                    session.rollback()
                    st.error(f"Could not add vehicle: {exc}")


st.divider()


# ==================================================
# LOAD VEHICLES AND SUMMARY
# ==================================================

st.subheader("📊 Fleet Overview")
all_vehicles = session.query(Vehicle).order_by(Vehicle.vehicle_number).all()

total_vehicles = len(all_vehicles)
available_vehicles = sum(1 for vehicle in all_vehicles if vehicle.status == "Available")
on_route_vehicles = sum(1 for vehicle in all_vehicles if vehicle.status == "On Route")
maintenance_vehicles = sum(1 for vehicle in all_vehicles if vehicle.status == "Maintenance")
inactive_vehicles = sum(1 for vehicle in all_vehicles if vehicle.status == "Inactive")

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric("🚛 Total Vehicles", total_vehicles)

with metric_col2:
    st.metric("🟢 Available", available_vehicles)

with metric_col3:
    st.metric("🔵 On Route", on_route_vehicles)

with metric_col4:
    st.metric("🛠️ Maintenance", maintenance_vehicles)

st.caption(f"Inactive vehicles: {inactive_vehicles}")


# ==================================================
# SEARCH AND FILTERS
# ==================================================

st.divider()
st.subheader("🔎 Search & Filter Vehicles")

filter_col1, filter_col2 = st.columns([1.5, 1])

with filter_col1:
    search_text = st.text_input(
        "Search vehicles",
        placeholder="Search by vehicle number or driver name...",
    )

with filter_col2:
    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Available", "On Route", "Maintenance", "Inactive"],
    )

filtered_vehicles = all_vehicles

if search_text:
    search_value = search_text.strip().lower()
    filtered_vehicles = [
        vehicle for vehicle in filtered_vehicles
        if search_value in (vehicle.vehicle_number or "").lower()
        or search_value in (vehicle.driver_name or "").lower()
    ]

if status_filter != "All":
    filtered_vehicles = [
        vehicle for vehicle in filtered_vehicles
        if vehicle.status == status_filter
    ]


# ==================================================
# DISPLAY FILTERED VEHICLES
# ==================================================

st.divider()
st.subheader("📋 Registered Vehicles")
st.caption(f"Showing {len(filtered_vehicles)} of {total_vehicles} vehicles.")

if filtered_vehicles:
    for vehicle in filtered_vehicles:
        with st.container(border=True):
            header_col, status_col = st.columns([2.4, 1])

            with header_col:
                st.markdown(f"### 🚛 {vehicle.vehicle_number}")
                st.caption(f"👤 Driver: {vehicle.driver_name or 'Not assigned'}")

            with status_col:
                if vehicle.status == "Available":
                    st.success("🟢 Available", icon="✅")
                elif vehicle.status == "On Route":
                    st.info("🔵 On Route", icon="🚛")
                elif vehicle.status == "Maintenance":
                    st.warning("🛠️ Maintenance", icon="🔧")
                else:
                    st.error("⚪ Inactive", icon="ℹ️")

            detail_col1, detail_col2, detail_col3 = st.columns(3)

            with detail_col1:
                st.markdown("**📦 Carrying Capacity**")
                st.write(f"**{float(vehicle.capacity_kg):,.1f} kg**")

            with detail_col2:
                st.markdown("**⛽ Fuel Efficiency**")
                fuel_value = float(vehicle.fuel_efficiency or 0)
                st.write(f"**{fuel_value:.1f} km/l**")

            with detail_col3:
                st.markdown("**🚦 Operational Status**")
                status_descriptions = {
                    "Available": "Ready for dispatch.",
                    "On Route": "Currently assigned to a route.",
                    "Maintenance": "Unavailable until maintenance is complete.",
                    "Inactive": "Not currently in operation.",
                }
                st.write(status_descriptions.get(vehicle.status, str(vehicle.status)))
else:
    st.warning("No vehicles match your search/filter.")


# ==================================================
# FOOTER AND CLEANUP
# ==================================================

st.divider()
st.caption("Smart Waste Collection • Vehicle Management")
session.close()
