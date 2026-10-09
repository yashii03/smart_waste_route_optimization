import streamlit as st
from sqlalchemy import text
from database.connection import engine
from services.route_service import optimize_routes


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Smart Waste Collection",
    page_icon="🚛",
    layout="wide"
)


# ==================================================
# CUSTOM UI STYLING
# ==================================================

st.markdown(
    """
    <style>

    /* =========================================
       WHOLE WEBSITE
       ========================================= */

    .stApp {
        background:
            linear-gradient(
                135deg,
                #062C30 0%,
                #07383D 45%,
                #041F23 100%
            );

        color: #E6FFFB;
    }

    .main {
        background: transparent;
    }


    /* =========================================
       HEADINGS
       ========================================= */

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


    /* =========================================
       SIDEBAR
       ========================================= */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #05282D,
                #041F23
            );

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


    /* =========================================
       METRIC CARDS
       ========================================= */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #0A3D42,
                #07343A
            );

        border: 1px solid #176B70;
        border-radius: 16px;

        padding: 20px;

        box-shadow:
            0 6px 20px rgba(0, 0, 0, 0.22);

        transition: all 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        border-color: #2DD4BF;

        box-shadow:
            0 8px 25px rgba(45, 212, 191, 0.15);

        transform: translateY(-2px);
    }

    div[data-testid="stMetricLabel"] {
        color: #99F6E4 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #F0FDFA !important;
        font-weight: 800;
    }

    div[data-testid="stMetricDelta"] {
        color: #4ADE80 !important;
    }


    /* =========================================
       BUTTONS
       ========================================= */

    .stButton > button {
        background:
            linear-gradient(
                135deg,
                #14B8A6,
                #0D9488
            );

        color: white;

        border: none;
        border-radius: 10px;

        padding: 9px 22px;

        font-weight: 700;

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background:
            linear-gradient(
                135deg,
                #2DD4BF,
                #14B8A6
            );

        box-shadow:
            0 6px 20px rgba(45, 212, 191, 0.3);

        transform: translateY(-1px);
    }


    /* =========================================
       INPUTS
       ========================================= */

    input,
    textarea {
        background-color: #0A3D42 !important;
        color: #E6FFFB !important;

        border-color: #176B70 !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #0A3D42 !important;
        border-color: #176B70 !important;
    }


    /* =========================================
       DATA TABLE
       ========================================= */

    div[data-testid="stDataFrame"] {
        border: 1px solid #176B70;
        border-radius: 14px;
        overflow: hidden;

        box-shadow:
            0 5px 18px rgba(0, 0, 0, 0.18);
    }


    /* =========================================
       ALERTS
       ========================================= */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* =========================================
       DIVIDERS
       ========================================= */

    hr {
        border-color: #155E63;
    }


    /* =========================================
       LINKS
       ========================================= */

    a {
        color: #67E8F9 !important;
    }


    /* =========================================
       SCROLLBAR
       ========================================= */

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #041F23;
    }

    ::-webkit-scrollbar-thumb {
        background: #155E63;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #2DD4BF;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR BRANDING
# ==================================================

with st.sidebar:

    st.markdown("# 🚛 Smart Waste")

    st.caption("Collection & Route Optimization")

    st.divider()

    st.success("🟢 System Online")


# ==================================================
# HEADER
# ==================================================

st.title("🚛 Smart Waste Collection")

st.subheader(
    "Route Optimization & Management System"
)

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

    st.error(
        f"Database connection error: {e}"
    )

    st.stop()


# ==================================================
# KEY METRICS
# ==================================================

st.subheader("📊 System Overview")

col1, col2, col3, col4 = st.columns(4)


# ==================================================
# TOTAL BINS
# ==================================================

with col1:

    st.markdown(
        f'<div style="background:linear-gradient(135deg,#102A43,#123C5A);border:1px solid #22D3EE;border-radius:14px;padding:18px;box-shadow:0 0 15px rgba(34,211,238,0.12);">'
        f'<div style="color:#67E8F9;font-size:14px;">🗑️ TOTAL BINS</div>'
        f'<div style="color:#F1F5F9;font-size:32px;font-weight:700;">{total_bins}</div>'
        f'<div style="color:#22D3EE;font-size:13px;">↑ {active_bins} Active</div>'
        f'</div>',
        unsafe_allow_html=True
    )


# ==================================================
# VEHICLES
# ==================================================

with col2:

    st.markdown(
        f'<div style="background:linear-gradient(135deg,#102E25,#123C32);border:1px solid #10B981;border-radius:14px;padding:18px;box-shadow:0 0 15px rgba(16,185,129,0.12);">'
        f'<div style="color:#6EE7B7;font-size:14px;">🚛 VEHICLES</div>'
        f'<div style="color:#F1F5F9;font-size:32px;font-weight:700;">{total_vehicles}</div>'
        f'<div style="color:#10B981;font-size:13px;">↑ {available_vehicles} Available</div>'
        f'</div>',
        unsafe_allow_html=True
    )


# ==================================================
# HIGH PRIORITY
# ==================================================

with col3:

    st.markdown(
        f'<div style="background:linear-gradient(135deg,#3A2A0B,#49330B);border:1px solid #F59E0B;border-radius:14px;padding:18px;box-shadow:0 0 15px rgba(245,158,11,0.12);">'
        f'<div style="color:#FCD34D;font-size:14px;">⚠️ HIGH PRIORITY</div>'
        f'<div style="color:#F1F5F9;font-size:32px;font-weight:700;">{high_priority_bins}</div>'
        f'<div style="color:#F59E0B;font-size:13px;">Bins need attention</div>'
        f'</div>',
        unsafe_allow_html=True
    )


# ==================================================
# COLLECTIONS
# ==================================================

with col4:

    st.markdown(
        f'<div style="background:linear-gradient(135deg,#2B1F45,#362552);border:1px solid #A78BFA;border-radius:14px;padding:18px;box-shadow:0 0 15px rgba(167,139,250,0.12);">'
        f'<div style="color:#C4B5FD;font-size:14px;">♻️ COLLECTIONS</div>'
        f'<div style="color:#F1F5F9;font-size:32px;font-weight:700;">{total_collections}</div>'
        f'<div style="color:#A78BFA;font-size:13px;">Total completed</div>'
        f'</div>',
        unsafe_allow_html=True
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


        # ==================================================
        # VEHICLE INFORMATION
        # ==================================================

        vehicle_html = (
            f'<div style="background:linear-gradient(135deg,#0A3D42,#07343A);'
            f'border:1px solid #176B70;border-radius:16px;padding:20px;'
            f'margin-bottom:18px;box-shadow:0 6px 20px rgba(0,0,0,0.20);">'
            f'<div style="color:#99F6E4;font-size:13px;font-weight:600;'
            f'letter-spacing:0.5px;">🚛 ASSIGNED VEHICLE</div>'
            f'<div style="color:#F0FDFA;font-size:26px;font-weight:800;'
            f'margin-top:5px;">{route["vehicle_number"]}</div>'
            f'<div style="color:#A7F3D0;font-size:14px;margin-top:4px;">'
            f'👨‍✈️ Driver: {route["driver_name"]}</div>'
            f'</div>'
        )

        st.markdown(
            vehicle_html,
            unsafe_allow_html=True
        )


        # ==================================================
        # ROUTE STATISTICS
        # ==================================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "📍 Distance",
                f"{route['total_distance_km']} km"
            )

        with col2:

            st.metric(
                "⏱️ Estimated Time",
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


        # ==================================================
        # ROUTE SEQUENCE
        # ==================================================

        st.markdown("### 🧭 Route Sequence")

        route_sequence = "  →  ".join(
            [
                (
                    f"🏫 {location['location_name']}"
                    if location["bin_code"] == "DEPOT"
                    else f"🗑️ {location['bin_code']}"
                )
                for location in route["route"]
            ]
        )

        route_html = (
            f'<div style="background:#07343A;'
            f'border:1px solid #176B70;border-radius:14px;padding:18px;'
            f'color:#CCFBF1;font-size:16px;font-weight:600;line-height:1.8;'
            f'box-shadow:0 5px 18px rgba(0,0,0,0.18);">'
            f'{route_sequence}'
            f'</div>'
        )

        st.markdown(
            route_html,
            unsafe_allow_html=True
        )


        st.success(
            "✅ Optimized route generated successfully."
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

            bin_code = bin_data[0]
            location = bin_data[1]
            fill_level = float(bin_data[2])
            capacity = bin_data[3]
            waste_type = bin_data[4]
            status = bin_data[5]

            # ==========================================
            # PRIORITY CARD
            # ==========================================

            st.markdown(
                f'<div style="background:linear-gradient(135deg,#3A2A0B,#2B230F);'
                f'border:1px solid #F59E0B;border-left:5px solid #F59E0B;'
                f'border-radius:14px;padding:16px 20px;margin-bottom:12px;'
                f'box-shadow:0 4px 15px rgba(0,0,0,0.18);">'
                f'<div style="display:flex;justify-content:space-between;'
                f'align-items:center;">'
                f'<div>'
                f'<div style="color:#FCD34D;font-size:18px;font-weight:800;">'
                f'⚠️ 🗑️ {bin_code}'
                f'</div>'
                f'<div style="color:#B6D9D5;font-size:13px;margin-top:5px;">'
                f'📍 {location}'
                f'</div>'
                f'</div>'
                f'<div style="text-align:right;">'
                f'<div style="color:#FCD34D;font-size:28px;font-weight:800;">'
                f'{fill_level:.0f}%'
                f'</div>'
                f'<div style="color:#F59E0B;font-size:12px;">FILL LEVEL</div>'
                f'</div>'
                f'</div>'
                f'<div style="margin-top:14px;padding-top:12px;'
                f'border-top:1px solid #59451A;">'
                f'<span style="color:#B6D9D5;font-size:13px;">'
                f'⚖️ Capacity: <b style="color:#F0FDFA;">{capacity} kg</b>'
                f'&nbsp;&nbsp;&nbsp;'
                f'♻️ Waste: <b style="color:#F0FDFA;">{waste_type}</b>'
                f'&nbsp;&nbsp;&nbsp;'
                f'🟢 Status: <b style="color:#A7F3D0;">{status}</b>'
                f'</span>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    else:

        st.success(
            "✅ No high-priority bins currently."
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


# ==================================================
# DATABASE STATUS
# ==================================================

with col1:

    st.markdown(
        '<div style="background:linear-gradient(135deg,#0A3D42,#07343A);'
        'border:1px solid #176B70;border-radius:14px;padding:18px;'
        'box-shadow:0 4px 15px rgba(0,0,0,0.18);">'
        '<div style="color:#4ADE80;font-size:26px;">●</div>'
        '<div style="color:#CCFBF1;font-size:16px;font-weight:700;'
        'margin-top:5px;">MySQL Database</div>'
        '<div style="color:#4ADE80;font-size:13px;margin-top:5px;">'
        '✓ Connected & Running</div>'
        '</div>',
        unsafe_allow_html=True
    )


# ==================================================
# OPTIMIZER STATUS
# ==================================================

with col2:

    st.markdown(
        '<div style="background:linear-gradient(135deg,#0A3D42,#07343A);'
        'border:1px solid #176B70;border-radius:14px;padding:18px;'
        'box-shadow:0 4px 15px rgba(0,0,0,0.18);">'
        '<div style="color:#4ADE80;font-size:26px;">●</div>'
        '<div style="color:#CCFBF1;font-size:16px;font-weight:700;'
        'margin-top:5px;">OR-Tools Optimizer</div>'
        '<div style="color:#4ADE80;font-size:13px;margin-top:5px;">'
        '✓ Ready for Route Planning</div>'
        '</div>',
        unsafe_allow_html=True
    )


# ==================================================
# ROUTE MANAGEMENT STATUS
# ==================================================

with col3:

    st.markdown(
        '<div style="background:linear-gradient(135deg,#0A3D42,#07343A);'
        'border:1px solid #176B70;border-radius:14px;padding:18px;'
        'box-shadow:0 4px 15px rgba(0,0,0,0.18);">'
        '<div style="color:#4ADE80;font-size:26px;">●</div>'
        '<div style="color:#CCFBF1;font-size:16px;font-weight:700;'
        'margin-top:5px;">Route Management</div>'
        '<div style="color:#4ADE80;font-size:13px;margin-top:5px;">'
        '✓ System Active</div>'
        '</div>',
        unsafe_allow_html=True
    )


st.markdown(
    '<div style="text-align:center;color:#5FA8A5;font-size:12px;'
    'margin-top:20px;">'
    'Smart Waste Collection • Route Optimization System'
    '</div>',
    unsafe_allow_html=True
)