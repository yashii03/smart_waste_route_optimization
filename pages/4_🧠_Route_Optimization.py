import streamlit as st
import folium
from streamlit_folium import st_folium

from services.route_service import optimize_routes


st.set_page_config(
    page_title="Route Optimization",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Route Optimization")
st.write(
    "Generate an optimized waste collection route using "
    "vehicle capacity, bin priority and distance."
)

st.divider()


# --------------------------------------------------
# Generate Route
# --------------------------------------------------

if st.button("🚀 Generate Optimized Route", type="primary"):

    with st.spinner("Optimizing collection routes..."):

        try:
            routes = optimize_routes()

            if not routes:
                st.warning(
                    "No optimized route could be generated."
                )
                st.stop()

            st.session_state["optimized_routes"] = routes
            st.success("✅ Optimized route generated successfully!")

        except Exception as e:
            st.error(f"Route optimization error: {e}")


# --------------------------------------------------
# Display Route
# --------------------------------------------------

if "optimized_routes" in st.session_state:

    routes = st.session_state["optimized_routes"]

    for route_number, route_data in enumerate(routes, start=1):

        st.divider()

        st.subheader(
            f"🚛 Route {route_number} — "
            f"{route_data['vehicle_number']}"
        )

        # ------------------------------------------
        # Vehicle information
        # ------------------------------------------

        st.write(
            f"👨‍✈️ **Driver:** {route_data['driver_name']}"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "📍 Distance",
                f"{route_data['total_distance_km']} km"
            )

        with col2:
            st.metric(
                "⏱️ Time",
                f"{route_data['estimated_time_min']} min"
            )

        with col3:
            st.metric(
                "⛽ Fuel",
                f"{route_data['estimated_fuel_l']} L"
            )

        with col4:
            st.metric(
                "♻️ Waste",
                f"{route_data['total_waste_kg']} kg"
            )

        # ------------------------------------------
        # Route sequence
        # ------------------------------------------

        st.subheader("📍 Optimized Route Sequence")

        route_names = []

        for location in route_data["route"]:

            if location["bin_code"] == "DEPOT":
                route_names.append(
                    f"🏫 {location['location_name']}"
                )
            else:
                route_names.append(
                    f"🗑️ {location['bin_code']}"
                )

        st.write(
            " → ".join(route_names)
        )

        # ------------------------------------------
        # Map
        # ------------------------------------------

        st.subheader("🗺️ Route Map")

        route_locations = route_data["route"]

        depot = route_locations[0]

        route_map = folium.Map(
            location=[
                depot["latitude"],
                depot["longitude"]
            ],
            zoom_start=10
        )

        # Markers

        for index, location in enumerate(route_locations):

            if location["bin_code"] == "DEPOT":

                folium.Marker(
                    location=[
                        location["latitude"],
                        location["longitude"]
                    ],
                    popup=location["location_name"],
                    tooltip="🏫 Collection Depot",
                    icon=folium.Icon(
                        color="green",
                        icon="home"
                    )
                ).add_to(route_map)

            else:

                folium.Marker(
                    location=[
                        location["latitude"],
                        location["longitude"]
                    ],
                    popup=(
                        f"<b>{location['bin_code']}</b><br>"
                        f"Location: {location['location_name']}<br>"
                        f"Fill Level: {location['fill_level']}%<br>"
                        f"Priority: {location['priority']}"
                    ),
                    tooltip=(
                        f"{index}. {location['bin_code']}"
                    ),
                    icon=folium.Icon(
                        color="red",
                        icon="trash"
                    )
                ).add_to(route_map)

        # Route line

        route_coordinates = [
            [
                location["latitude"],
                location["longitude"]
            ]
            for location in route_locations
        ]

        folium.PolyLine(
            route_coordinates,
            weight=5,
            opacity=0.8
        ).add_to(route_map)

        st_folium(
            route_map,
            width=None,
            height=550
        )

else:

    st.info(
        "👆 Click **Generate Optimized Route** "
        "to create the collection route."
    )