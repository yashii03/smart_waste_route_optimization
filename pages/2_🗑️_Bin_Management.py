import streamlit as st
from datetime import datetime

from database.connection import engine
from database.models import Bin
from sqlalchemy.orm import sessionmaker


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Bin Management",
    page_icon="🗑️",
    layout="wide"
)

st.title("🗑️ Bin Management")
st.write("Add and manage waste collection bins.")


# -----------------------------
# Database Session
# -----------------------------

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


# -----------------------------
# Add New Bin
# -----------------------------

st.subheader("➕ Add New Waste Bin")

with st.form("add_bin_form"):

    col1, col2 = st.columns(2)

    with col1:
        bin_code = st.text_input(
            "Bin Code",
            placeholder="Example: BIN101"
        )

        location_name = st.text_input(
            "Location Name",
            placeholder="Example: Zone A"
        )

        latitude = st.number_input(
            "Latitude",
            format="%.7f"
        )

        longitude = st.number_input(
            "Longitude",
            format="%.7f"
        )

    with col2:
        capacity_kg = st.number_input(
            "Capacity (kg)",
            min_value=1.0,
            value=100.0
        )

        fill_level = st.number_input(
            "Fill Level (%)",
            min_value=0.0,
            max_value=100.0,
            value=50.0
        )

        waste_type = st.selectbox(
            "Waste Type",
            [
                "Mixed",
                "Wet",
                "Dry",
                "Plastic",
                "Paper",
                "Metal"
            ]
        )

        status = st.selectbox(
            "Status",
            [
                "Active",
                "Inactive",
                "Full",
                "Maintenance"
            ]
        )

    submitted = st.form_submit_button("➕ Add Bin")

    if submitted:

        if not bin_code or not location_name:
            st.error("Please enter Bin Code and Location Name.")

        else:

            existing_bin = session.query(Bin).filter(
                Bin.bin_code == bin_code
            ).first()

            if existing_bin:
                st.error("❌ This Bin Code already exists.")

            else:

                new_bin = Bin(
                    bin_code=bin_code,
                    location_name=location_name,
                    latitude=latitude,
                    longitude=longitude,
                    capacity_kg=capacity_kg,
                    fill_level=fill_level,
                    waste_type=waste_type,
                    last_collected=datetime.now(),
                    status=status,
                    created_at=datetime.now()
                )

                session.add(new_bin)
                session.commit()

                st.success(
                    f"✅ Bin {bin_code} added successfully!"
                )

                st.rerun()


# -----------------------------
# Bin Summary
# -----------------------------

st.divider()

st.subheader("📊 Bin Overview")

all_bins = session.query(Bin).all()

total_bins = len(all_bins)
active_bins = sum(1 for b in all_bins if b.status == "Active")
full_bins = sum(1 for b in all_bins if b.status == "Full")
high_fill_bins = sum(1 for b in all_bins if b.fill_level >= 80)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🗑️ Total Bins", total_bins)

with col2:
    st.metric("🟢 Active Bins", active_bins)

with col3:
    st.metric("🔴 Full Bins", full_bins)

with col4:
    st.metric("⚠️ High Fill", high_fill_bins)


# -----------------------------
# Search and Filters
# -----------------------------

st.subheader("🔎 Search & Filter Bins")

col1, col2, col3 = st.columns(3)

with col1:
    search_text = st.text_input(
        "Search",
        placeholder="Bin code or location..."
    )

with col2:
    status_filter = st.selectbox(
        "Filter by Status",
        [
            "All",
            "Active",
            "Inactive",
            "Full",
            "Maintenance"
        ]
    )

with col3:
    waste_filter = st.selectbox(
        "Filter by Waste Type",
        [
            "All",
            "Mixed",
            "Wet",
            "Dry",
            "Plastic",
            "Paper",
            "Metal",
            "Organic"
        ]
    )


# -----------------------------
# Apply Filters
# -----------------------------

filtered_bins = all_bins

if search_text:
    search_text = search_text.lower()

    filtered_bins = [
        b for b in filtered_bins
        if search_text in b.bin_code.lower()
        or search_text in b.location_name.lower()
    ]


if status_filter != "All":
    filtered_bins = [
        b for b in filtered_bins
        if b.status == status_filter
    ]


if waste_filter != "All":
    filtered_bins = [
        b for b in filtered_bins
        if b.waste_type == waste_filter
    ]


# -----------------------------
# Display Filtered Bins
# -----------------------------

st.subheader("📋 Existing Waste Bins")

st.write(
    f"Showing **{len(filtered_bins)}** of **{total_bins}** bins."
)


if filtered_bins:

    for bin in filtered_bins:

        with st.container(border=True):

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.write(f"**🗑️ {bin.bin_code}**")
                st.write(bin.location_name)

            with col2:
                st.write(f"📍 Latitude: {bin.latitude}")
                st.write(f"📍 Longitude: {bin.longitude}")

            with col3:
                st.write(f"📦 Capacity: {bin.capacity_kg} kg")
                st.write(f"🔋 Fill Level: {bin.fill_level}%")

            with col4:
                st.write(f"♻️ Type: {bin.waste_type}")
                st.write(f"🟢 Status: {bin.status}")

else:

    st.warning("No bins match your search/filter.")


# -----------------------------
# Close Database Session
# -----------------------------

session.close()