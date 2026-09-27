import streamlit as st
from sqlalchemy import text
from database.connection import engine
from services.route_service import optimize_routes


st.set_page_config(
    page_title="Smart Waste Collection",
    page_icon="🚛",
    layout="wide"
)


# ==================================================
# HEADER
# ==================================================

st.title("🚛 Smart Waste Collection")
st.subheader("Route Optimization & Management System")

st.write(
    "A smart waste collection system that uses "
    "bin priority, vehicle capacity and route optimization "
    "to plan efficient collection routes."
)

st.divider()


# ==================================================
# DATABASE
# ==================================================

try:

    with engine.connect() as connection:

        total_bins = connection.execute(
            text("SELECT COUNT(*) FROM bins")
        ).scalar()

        active_bins = connection.execute(
            text(
                "SELECT COUNT(*) FROM bins "
                "WHERE status = 'Active'"
            )
        ).scalar()

        total_vehicles = connection.execute(
            text("SELECT COUNT(*) FROM vehicles")
        ).scalar()

        available_vehicles = connection.execute(
            text(
                "SELECT COUNT(*) FROM vehicles "
                "WHERE status = 'Available'"
            )
        ).scalar()

        total_collections = connection.execute(
            text("SELECT COUNT(*) FROM collections")
        ).scalar()

        high_priority_bins = connection.execute(
            text(
                "SELECT COUNT(*) FROM bins "
                "WHERE fill_level >= 80"
            )
        ).scalar()

except Exception as e:

    st.error(f"Database connection error: {e}")
    st.stop()


# ==================================================
# KEY METRICS
# ==================================================

st.subheader("📊 System Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🗑️ Total Bins",
        total_bins,
        f"{active_bins} Active"
    )

with col2:
    st.metric(
        "🚛 Vehicles",
        total_vehicles,
        f"{available_vehicles} Available"
    )

with col3:
    st.metric(
        "⚠️ High Priority Bins",
        high_priority_bins
    )

with col4:
    st.metric(
        "♻️ Collections",
        total_collections
    )


st.divider()


# ==================================================
# ROUTE SUMMARY
# ==================================================

st.subheader("🧠 Latest Optimized Route")

try:

    routes = optimize_routes()

    if routes:

        route = routes[0]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "📍 Distance",
                f"{route['total_distance_km']} km"
            )

        with col2:
            st.metric(
                "⏱️ Time",
                f"{route['estimated_time_min']} min"
            )

        with col3:
            st.metric(
                "⛽ Fuel",
                f"{route['estimated_fuel_l']} L"
            )

        with col4:
            st.metric(
                "♻️ Waste",
                f"{route['total_waste_kg']} kg"
            )

        st.success(
            f"🚛 Vehicle **{route['vehicle_number']}** "
            f"assigned to the optimized route."
        )

        st.write(
            " → ".join(
                [
                    location["bin_code"]
                    for location in route["route"]
                ]
            )
        )

    else:

        st.info(
            "No optimized route available."
        )

except Exception as e:

    st.warning(
        f"Route information unavailable: {e}"
    )


st.divider()


# ==================================================
# HIGH PRIORITY BINS
# ==================================================

st.subheader("⚠️ High Priority Bins")

try:

    with engine.connect() as connection:

        high_priority = connection.execute(
            text(
                """
                SELECT
                    bin_code,
                    location_name,
                    fill_level,
                    capacity_kg,
                    waste_type,
                    status
                FROM bins
                WHERE fill_level >= 80
                ORDER BY fill_level DESC
                """
            )
        ).fetchall()

    if high_priority:

        for bin_data in high_priority:

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.write(
                    f"🗑️ **{bin_data[0]}**"
                )

            with col2:
                st.write(
                    bin_data[1]
                )

            with col3:
                st.write(
                    f"Fill: **{bin_data[2]}%**"
                )

            with col4:
                st.write(
                    f"Capacity: **{bin_data[3]} kg**"
                )

    else:

        st.success(
            "No high-priority bins currently."
        )

except Exception as e:

    st.error(
        f"Could not load bin information: {e}"
    )


st.divider()


# ==================================================
# SYSTEM STATUS
# ==================================================

st.subheader("🟢 System Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("🟢 MySQL Database Connected")

with col2:
    st.success("🟢 OR-Tools Optimizer Ready")

with col3:
    st.success("🟢 Route Management Active")