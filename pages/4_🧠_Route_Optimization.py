import streamlit as st
import folium
from streamlit_folium import st_folium

from services.route_service import optimize_routes


st.set_page_config(
    page_title="Route Optimization",
    page_icon="🧠",
    layout="wide",
)


# ==================================================
# DEEP TEAL THEME
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

    p {
        color: #B6D9D5;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #05282D, #041F23);
        border-right: 1px solid #155E63;
    }

    section[data-testid="stSidebar"] p {
        color: #99F6E4;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #CCFBF1 !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #14B8A6, #0D9488);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 9px 22px;
        font-weight: 700;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #2DD4BF, #14B8A6);
        box-shadow: 0 6px 20px rgba(45, 212, 191, 0.3);
        transform: translateY(-1px);
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

st.markdown(
    '<div style="'
    'background:linear-gradient(135deg,#062C30,#07383D,#041F23);'
    'border:1px solid #155E63;'
    'border-radius:18px;'
    'padding:24px 28px;'
    'margin-bottom:20px;'
    'box-shadow:0 6px 20px rgba(0,0,0,0.22);'
    '">'
    '<div style="'
    'color:#CCFBF1;'
    'font-size:32px;'
    'font-weight:800;'
    '">'
    '🧠 Route Optimization'
    '</div>'
    '<div style="'
    'color:#B6D9D5;'
    'font-size:15px;'
    'margin-top:7px;'
    '">'
    'Generate an efficient waste collection route using bin priority, vehicle capacity and distance.'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div style="'
    'color:#67E8F9;'
    'font-size:13px;'
    'font-weight:600;'
    'margin-bottom:8px;'
    '">'
    '🚛 SMART ROUTE PLANNING'
    '</div>',
    unsafe_allow_html=True,
)


# ==================================================
# GENERATE ROUTE
# ==================================================

if st.button("🚀 Generate Optimized Route", type="primary"):
    with st.spinner("Optimizing collection routes..."):
        try:
            routes = optimize_routes()

            if not routes:
                st.warning("No optimized route could be generated.")
                st.stop()

            st.session_state["optimized_routes"] = routes
            st.success("✅ Optimized route generated successfully!")

        except Exception as e:
            st.error(f"Route optimization error: {e}")


# ==================================================
# DISPLAY ROUTE
# ==================================================

if "optimized_routes" in st.session_state:
    routes = st.session_state["optimized_routes"]

    for route_number, route_data in enumerate(routes, start=1):
        st.divider()

        st.subheader(
            f"🚛 Route {route_number} — {route_data['vehicle_number']}"
        )

        st.write(f"👨‍✈️ **Driver:** {route_data['driver_name']}")

        # ==================================================
        # ROUTE STATISTICS
        # ==================================================

        col1, col2, col3, col4 = st.columns(4)

        distance_card = (
            '<div style="'
            'background:linear-gradient(135deg,#102A43,#123C5A);'
            'border:1px solid #22D3EE;'
            'border-radius:16px;'
            'padding:18px;'
            'height:115px;'
            'box-shadow:0 6px 20px rgba(0,0,0,0.22);'
            '">'
            '<div style="color:#67E8F9;font-size:13px;font-weight:600;">'
            '📍 DISTANCE'
            '</div>'
            '<div style="color:#F0FDFA;font-size:28px;font-weight:800;margin-top:8px;">'
            f"{route_data['total_distance_km']} km"
            '</div>'
            '</div>'
        )

        time_card = (
            '<div style="'
            'background:linear-gradient(135deg,#102E25,#123C32);'
            'border:1px solid #10B981;'
            'border-radius:16px;'
            'padding:18px;'
            'height:115px;'
            'box-shadow:0 6px 20px rgba(0,0,0,0.22);'
            '">'
            '<div style="color:#6EE7B7;font-size:13px;font-weight:600;">'
            '⏱️ ESTIMATED TIME'
            '</div>'
            '<div style="color:#F0FDFA;font-size:28px;font-weight:800;margin-top:8px;">'
            f"{route_data['estimated_time_min']} min"
            '</div>'
            '</div>'
        )

        fuel_card = (
            '<div style="'
            'background:linear-gradient(135deg,#3A2A0B,#49330B);'
            'border:1px solid #F59E0B;'
            'border-radius:16px;'
            'padding:18px;'
            'height:115px;'
            'box-shadow:0 6px 20px rgba(0,0,0,0.22);'
            '">'
            '<div style="color:#FCD34D;font-size:13px;font-weight:600;">'
            '⛽ FUEL'
            '</div>'
            '<div style="color:#F0FDFA;font-size:28px;font-weight:800;margin-top:8px;">'
            f"{route_data['estimated_fuel_l']} L"
            '</div>'
            '</div>'
        )

        waste_card = (
            '<div style="'
            'background:linear-gradient(135deg,#2B1F45,#362552);'
            'border:1px solid #A78BFA;'
            'border-radius:16px;'
            'padding:18px;'
            'height:115px;'
            'box-shadow:0 6px 20px rgba(0,0,0,0.22);'
            '">'
            '<div style="color:#C4B5FD;font-size:13px;font-weight:600;">'
            '♻️ WASTE'
            '</div>'
            '<div style="color:#F0FDFA;font-size:28px;font-weight:800;margin-top:8px;">'
            f"{route_data['total_waste_kg']} kg"
            '</div>'
            '</div>'
        )

        with col1:
            st.markdown(distance_card, unsafe_allow_html=True)

        with col2:
            st.markdown(time_card, unsafe_allow_html=True)

        with col3:
            st.markdown(fuel_card, unsafe_allow_html=True)

        with col4:
            st.markdown(waste_card, unsafe_allow_html=True)

        # ==================================================
        # ROUTE SEQUENCE
        # ==================================================

        st.subheader("📍 Optimized Route Sequence")

        route_names = []
        for location in route_data["route"]:
            if location["bin_code"] == "DEPOT":
                route_names.append(f"🏫 {location['location_name']}")
            else:
                route_names.append(f"🗑️ {location['bin_code']}")

        st.write(" → ".join(route_names))

        # ==================================================
        # ROUTE MAP - LOAD ONLY WHEN REQUESTED
        # ==================================================

        st.subheader("🗺️ Route Map")

        st.markdown(
            '<div style="'
            'background:linear-gradient(135deg,#0A3D42,#07343A);'
            'border:1px solid #176B70;'
            'border-radius:14px;'
            'padding:14px 18px;'
            'margin-bottom:12px;'
            'box-shadow:0 4px 14px rgba(0,0,0,0.16);'
            '">'
            '<span style="color:#99F6E4;font-weight:700;">🗺️ Interactive Route Map</span>'
            '<span style="color:#B6D9D5;margin-left:10px;font-size:13px;">'
            'Load it only when needed.'
            '</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div style="display:flex;gap:18px;margin:4px 0 10px 2px;">'
            '<span style="color:#6EE7B7;font-size:12px;font-weight:600;">🟢 DEPOT</span>'
            '<span style="color:#FCA5A5;font-size:12px;font-weight:600;">🔴 BIN</span>'
            '<span style="color:#B6D9D5;font-size:12px;">— Optimized route</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        button_key = f"load_route_map_{route_number}_{route_data['vehicle_number']}"
        map_state_key = f"route_map_loaded_{route_number}_{route_data['vehicle_number']}"

        if st.button("🗺️ Load Route Map", key=button_key):
            st.session_state[map_state_key] = True

        if st.session_state.get(map_state_key, False):
            route_locations = route_data["route"]
            depot = route_locations[0]

            route_map = folium.Map(
                location=[float(depot["latitude"]), float(depot["longitude"])],
                zoom_start=14,
                control_scale=True,
                tiles="OpenStreetMap",
            )

            route_coordinates = []

            for index, location in enumerate(route_locations):
                latitude = float(location["latitude"])
                longitude = float(location["longitude"])
                route_coordinates.append([latitude, longitude])

                if location["bin_code"] == "DEPOT":
                    folium.CircleMarker(
                        location=[latitude, longitude],
                        radius=9,
                        color="#10B981",
                        fill=True,
                        fill_color="#10B981",
                        fill_opacity=0.95,
                        popup=location["location_name"],
                        tooltip="🏫 Collection Depot",
                    ).add_to(route_map)
                else:
                    folium.CircleMarker(
                        location=[latitude, longitude],
                        radius=7,
                        color="#EF4444",
                        fill=True,
                        fill_color="#EF4444",
                        fill_opacity=0.9,
                        popup=(
                            f"<b>{location['bin_code']}</b><br>"
                            f"Location: {location['location_name']}<br>"
                            f"Fill Level: {location['fill_level']}%<br>"
                            f"Priority: {location['priority']}"
                        ),
                        tooltip=f"{index}. {location['bin_code']}",
                    ).add_to(route_map)

            folium.PolyLine(
                route_coordinates,
                weight=5,
                opacity=0.8,
            ).add_to(route_map)

            if len(route_coordinates) > 1:
                route_map.fit_bounds(route_coordinates, padding=(20, 20))

            st_folium(route_map, width=None, height=520)

else:
    st.info(
        "👆 Click **Generate Optimized Route** to create the collection route."
    )
