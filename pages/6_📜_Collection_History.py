import streamlit as st
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database.connection import engine
from database.models import Bin, Vehicle, Collection


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Collection History",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Collection History")

st.write(
    "Record completed waste collections and "
    "view previous collection activity."
)

st.divider()


# ==================================================
# ADD COLLECTION
# ==================================================

st.subheader("➕ Record New Collection")

with Session(engine) as session:

    bins = (
        session.query(Bin)
        .filter(Bin.status == "Active")
        .order_by(Bin.bin_code)
        .all()
    )

    vehicles = (
        session.query(Vehicle)
        .filter(Vehicle.status != "Maintenance")
        .order_by(Vehicle.vehicle_number)
        .all()
    )


if not bins:
    st.warning("No active bins available.")
    st.stop()

if not vehicles:
    st.warning("No available vehicles.")
    st.stop()


with st.form("collection_form"):

    col1, col2 = st.columns(2)

    with col1:

        selected_bin = st.selectbox(
            "🗑️ Select Bin",
            bins,
            format_func=lambda b:
                f"{b.bin_code} - {b.location_name}"
        )

    with col2:

        selected_vehicle = st.selectbox(
            "🚛 Select Vehicle",
            vehicles,
            format_func=lambda v:
                f"{v.vehicle_number} - {v.driver_name}"
        )

    col3, col4 = st.columns(2)

    with col3:

        fill_before = st.number_input(
            "📊 Fill Level Before Collection (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(selected_bin.fill_level),
            step=1.0
        )

    with col4:

        waste_collected = st.number_input(
            "♻️ Waste Collected (kg)",
            min_value=0.0,
            max_value=float(selected_bin.capacity_kg),
            value=float(
                selected_bin.capacity_kg
                * selected_bin.fill_level
                / 100
            ),
            step=1.0
        )

    notes = st.text_area(
        "📝 Notes",
        placeholder="Optional collection notes..."
    )

    submitted = st.form_submit_button(
        "💾 Save Collection",
        type="primary"
    )


# ==================================================
# SAVE COLLECTION
# ==================================================

if submitted:

    try:

        with Session(engine) as session:

            bin_record = session.query(Bin).filter(
                Bin.bin_id == selected_bin.bin_id
            ).first()

            collection = Collection(
                bin_id=selected_bin.bin_id,
                vehicle_id=selected_vehicle.vehicle_id,
                waste_collected_kg=waste_collected,
                fill_level_before=fill_before,
                fill_level_after=0,
                notes=notes
            )

            session.add(collection)

            # Reset bin after collection
            bin_record.fill_level = 0

            session.commit()

        st.success(
            f"✅ Collection for {selected_bin.bin_code} "
            f"recorded successfully!"
        )

        st.rerun()

    except Exception as e:

        st.error(
            f"Could not save collection: {e}"
        )


st.divider()


# ==================================================
# COLLECTION STATISTICS
# ==================================================

st.subheader("📊 Collection Statistics")

with Session(engine) as session:

    total_collections = (
        session.query(Collection)
        .count()
    )

    total_waste = sum(
        float(c.waste_collected_kg or 0)
        for c in session.query(Collection).all()
    )


col1, col2 = st.columns(2)

with col1:

    st.metric(
        "📜 Total Collections",
        total_collections
    )

with col2:

    st.metric(
        "♻️ Total Waste Collected",
        f"{total_waste:.1f} kg"
    )


st.divider()


# ==================================================
# COLLECTION HISTORY TABLE
# ==================================================

st.subheader("📋 Previous Collections")

with Session(engine) as session:

    collections = (
        session.query(Collection, Bin, Vehicle)
        .join(
            Bin,
            Collection.bin_id == Bin.bin_id
        )
        .join(
            Vehicle,
            Collection.vehicle_id == Vehicle.vehicle_id
        )
        .order_by(
            desc(Collection.collection_date)
        )
        .all()
    )


if collections:

    history = []

    for collection, bin_record, vehicle in collections:

        history.append({
            "Date": collection.collection_date,
            "Bin": bin_record.bin_code,
            "Location": bin_record.location_name,
            "Vehicle": vehicle.vehicle_number,
            "Driver": vehicle.driver_name,
            "Waste Collected (kg)": float(
                collection.waste_collected_kg or 0
            ),
            "Fill Before (%)": float(
                collection.fill_level_before or 0
            ),
            "Fill After (%)": float(
                collection.fill_level_after or 0
            ),
            "Notes": collection.notes or ""
        })

    st.dataframe(
        history,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "📭 No collection records yet. "
        "Record your first collection above."
    )