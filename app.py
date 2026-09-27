import streamlit as st
from sqlalchemy import text

from database.connection import engine

# Page configuration
st.set_page_config(
    page_title="Smart Waste Collection",
    page_icon="🚛",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------

st.title("🚛 Smart Waste Collection Route Optimization")

st.write(
    "A smart system for managing waste bins and optimizing "
    "collection routes using Python, MySQL and OR-Tools."
)

st.divider()

# -----------------------------
# Database Statistics
# -----------------------------

try:
    with engine.connect() as connection:

        total_bins = connection.execute(
            text("SELECT COUNT(*) FROM bins")
        ).scalar()

        total_vehicles = connection.execute(
            text("SELECT COUNT(*) FROM vehicles")
        ).scalar()

        total_collections = connection.execute(
            text("SELECT COUNT(*) FROM collections")
        ).scalar()

except Exception as e:
    st.error(f"Database connection error: {e}")
    st.stop()

# -----------------------------
# Dashboard Metrics
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🗑️ Total Bins",
        value=total_bins
    )

with col2:
    st.metric(
        label="🚛 Total Vehicles",
        value=total_vehicles
    )

with col3:
    st.metric(
        label="♻️ Collections",
        value=total_collections
    )

st.divider()

# -----------------------------
# Project Status
# -----------------------------

st.subheader("📊 System Status")

st.success("🟢 Database connected successfully!")

st.info(
    "The dashboard is connected to MySQL and is ready "
    "for waste collection route optimization."
)