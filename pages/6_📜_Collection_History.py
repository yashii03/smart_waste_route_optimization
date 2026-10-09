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


# ==================================================
# DEEP TEAL THEME
# ==================================================

st.markdown(
    """
    <style>
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
        background: linear-gradient(180deg,#05282D,#041F23);
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

    div[data-testid="stTextInput"],
    div[data-testid="stNumberInput"],
    div[data-testid="stTextArea"],
    div[data-testid="stSelectbox"] {
        margin-bottom: 8px;
    }

    .stButton > button,
    button[kind="primaryFormSubmit"] {
        background: linear-gradient(135deg,#14B8A6,#0D9488);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 9px 22px;
        font-weight: 700;
    }

    .stButton > button:hover,
    button[kind="primaryFormSubmit"]:hover {
        background: linear-gradient(135deg,#2DD4BF,#14B8A6);
        box-shadow: 0 6px 20px rgba(45,212,191,0.30);
        transform: translateY(-1px);
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #176B70;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 5px 18px rgba(0,0,0,0.18);
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    hr {
        border-color: #155E63;
    }

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
# SIDEBAR
# ==================================================

with st.sidebar:
    st.markdown("# 🚛 Smart Waste")
    st.caption("Collection & Route Optimization")
    st.divider()
    st.success("🟢 System Online")


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
    '<div style="color:#CCFBF1;font-size:32px;font-weight:800;">'
    '📜 Collection History'
    '</div>'
    '<div style="color:#B6D9D5;font-size:15px;margin-top:7px;">'
    'Record completed waste collections and monitor previous collection activity.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div style="color:#67E8F9;font-size:13px;font-weight:600;margin-bottom:8px;">'
    '📝 COLLECTION RECORDS & ACTIVITY'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# LOAD BINS AND VEHICLES
# ==================================================

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


# ==================================================
# RECORD NEW COLLECTION
# ==================================================

st.subheader("➕ Record New Collection")

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

            bin_record = (
                session.query(Bin)
                .filter(Bin.bin_id == selected_bin.bin_id)
                .first()
            )

            if bin_record is None:
                st.error("Selected bin could not be found.")
                st.stop()

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

collections_card = (
    '<div style="'
    'background:linear-gradient(135deg,#102A43,#123C5A);'
    'border:1px solid #22D3EE;'
    'border-radius:16px;'
    'padding:18px;'
    'height:105px;'
    'box-shadow:0 6px 20px rgba(0,0,0,0.22);'
    '">'
    '<div style="color:#67E8F9;font-size:13px;font-weight:600;">📜 TOTAL COLLECTIONS</div>'
    f'<div style="color:#F0FDFA;font-size:28px;font-weight:800;margin-top:8px;">'
    f'{total_collections}'
    f'</div>'
    '</div>'
)

waste_collected_card = (
    '<div style="'
    'background:linear-gradient(135deg,#2B1F45,#362552);'
    'border:1px solid #A78BFA;'
    'border-radius:16px;'
    'padding:18px;'
    'height:105px;'
    'box-shadow:0 6px 20px rgba(0,0,0,0.22);'
    '">'
    '<div style="color:#C4B5FD;font-size:13px;font-weight:600;">♻️ TOTAL WASTE COLLECTED</div>'
    f'<div style="color:#F0FDFA;font-size:28px;font-weight:800;margin-top:8px;">'
    f'{total_waste:.1f} kg'
    f'</div>'
    '</div>'
)

with col1:
    st.markdown(
        collections_card,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        waste_collected_card,
        unsafe_allow_html=True
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
