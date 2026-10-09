import streamlit as st
from datetime import datetime
from sqlalchemy.orm import sessionmaker

from database.connection import engine
from database.models import Bin


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Bin Management",
    page_icon="🗑️",
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

st.title("🗑️ Bin Management")
st.caption("Manage collection bins, monitor fill levels, and track bin status.")

st.markdown(
    '<div style="background:linear-gradient(135deg,#0A3D42,#07343A);'
    'border:1px solid #176B70;border-radius:16px;padding:16px 20px;'
    'margin:8px 0 20px 0;">'
    '<div style="color:#99F6E4;font-size:13px;font-weight:700;letter-spacing:.5px;">'
    '♻️ WASTE COLLECTION OPERATIONS'
    '</div>'
    '<div style="color:#CCFBF1;font-size:15px;margin-top:5px;">'
    'Add bins, monitor fill levels, and find bins that need collection.'
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
# ADD NEW BIN
# ==================================================

st.subheader("➕ Add New Waste Bin")

with st.form("add_bin_form", clear_on_submit=False):
    st.caption("Enter the bin details below. Bin Code must be unique.")

    form_col1, form_col2 = st.columns(2)

    with form_col1:
        bin_code = st.text_input(
            "Bin Code",
            placeholder="Example: BIN101",
        )

        location_name = st.text_input(
            "Location Name",
            placeholder="Example: Zone A",
        )

        latitude = st.number_input(
            "Latitude",
            format="%.7f",
        )

        longitude = st.number_input(
            "Longitude",
            format="%.7f",
        )

    with form_col2:
        capacity_kg = st.number_input(
            "Capacity (kg)",
            min_value=1.0,
            value=100.0,
            step=10.0,
        )

        fill_level = st.number_input(
            "Fill Level (%)",
            min_value=0.0,
            max_value=100.0,
            value=50.0,
            step=5.0,
        )

        waste_type = st.selectbox(
            "Waste Type",
            ["Mixed", "Wet", "Dry", "Plastic", "Paper", "Metal"],
        )

        status = st.selectbox(
            "Status",
            ["Active", "Inactive", "Full", "Maintenance"],
        )

    submitted = st.form_submit_button("➕ Add Bin", type="primary", use_container_width=True)

    if submitted:
        cleaned_bin_code = bin_code.strip()
        cleaned_location = location_name.strip()

        if not cleaned_bin_code or not cleaned_location:
            st.error("Please enter both Bin Code and Location Name.")
        else:
            existing_bin = session.query(Bin).filter(
                Bin.bin_code == cleaned_bin_code
            ).first()

            if existing_bin:
                st.error("❌ This Bin Code already exists.")
            else:
                now = datetime.now()
                new_bin = Bin(
                    bin_code=cleaned_bin_code,
                    location_name=cleaned_location,
                    latitude=latitude,
                    longitude=longitude,
                    capacity_kg=capacity_kg,
                    fill_level=fill_level,
                    waste_type=waste_type,
                    last_collected=now,
                    status=status,
                    created_at=now,
                )

                session.add(new_bin)
                session.commit()
                st.success(f"✅ Bin {cleaned_bin_code} added successfully!")
                st.rerun()


st.divider()


# ==================================================
# LOAD BINS AND SUMMARY
# ==================================================

st.subheader("📊 Bin Overview")
all_bins = session.query(Bin).order_by(Bin.bin_code).all()

total_bins = len(all_bins)
active_bins = sum(1 for bin_record in all_bins if bin_record.status == "Active")
full_bins = sum(1 for bin_record in all_bins if bin_record.status == "Full")
high_fill_bins = sum(1 for bin_record in all_bins if float(bin_record.fill_level or 0) >= 80)

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric("🗑️ Total Bins", total_bins)

with metric_col2:
    st.metric("🟢 Active Bins", active_bins)

with metric_col3:
    st.metric("🔴 Full Bins", full_bins)

with metric_col4:
    st.metric("⚠️ High Fill", high_fill_bins)


# ==================================================
# SEARCH AND FILTERS
# ==================================================

st.divider()
st.subheader("🔎 Search & Filter Bins")

filter_col1, filter_col2, filter_col3 = st.columns([1.5, 1, 1])

with filter_col1:
    search_text = st.text_input(
        "Search bins",
        placeholder="Search by bin code or location...",
    )

with filter_col2:
    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Active", "Inactive", "Full", "Maintenance"],
    )

with filter_col3:
    waste_filter = st.selectbox(
        "Filter by Waste Type",
        ["All", "Mixed", "Wet", "Dry", "Plastic", "Paper", "Metal", "Organic"],
    )

filtered_bins = all_bins

if search_text:
    search_value = search_text.strip().lower()
    filtered_bins = [
        bin_record for bin_record in filtered_bins
        if search_value in (bin_record.bin_code or "").lower()
        or search_value in (bin_record.location_name or "").lower()
    ]

if status_filter != "All":
    filtered_bins = [
        bin_record for bin_record in filtered_bins
        if bin_record.status == status_filter
    ]

if waste_filter != "All":
    filtered_bins = [
        bin_record for bin_record in filtered_bins
        if bin_record.waste_type == waste_filter
    ]


# ==================================================
# DISPLAY FILTERED BINS
# ==================================================

st.divider()
st.subheader("📋 Existing Waste Bins")
st.caption(f"Showing {len(filtered_bins)} of {total_bins} bins.")

if filtered_bins:
    for bin_record in filtered_bins:
        fill_value = max(0.0, min(100.0, float(bin_record.fill_level or 0)))

        with st.container(border=True):
            top_col1, top_col2 = st.columns([2.4, 1])

            with top_col1:
                st.markdown(f"### 🗑️ {bin_record.bin_code}")
                st.caption(f"📍 {bin_record.location_name}")

            with top_col2:
                if bin_record.status == "Active":
                    st.success("🟢 Active", icon="✅")
                elif bin_record.status == "Full":
                    st.error("🔴 Full", icon="⚠️")
                elif bin_record.status == "Maintenance":
                    st.warning("🛠️ Maintenance", icon="🔧")
                else:
                    st.info("⚪ Inactive", icon="ℹ️")

            detail_col1, detail_col2, detail_col3 = st.columns(3)

            with detail_col1:
                st.markdown("**📍 Coordinates**")
                st.caption(f"Latitude: {float(bin_record.latitude):.7f}")
                st.caption(f"Longitude: {float(bin_record.longitude):.7f}")

            with detail_col2:
                st.markdown("**📦 Bin Details**")
                st.write(f"Capacity: **{float(bin_record.capacity_kg):.1f} kg**")
                st.write(f"Waste type: **{bin_record.waste_type}**")

            with detail_col3:
                st.markdown("**🔋 Fill Level**")
                st.write(f"**{fill_value:.0f}%** filled")
                st.progress(fill_value / 100.0)
                if fill_value >= 80:
                    st.warning("High fill — collection recommended.")
                elif fill_value >= 50:
                    st.info("Fill level is moderate.")
                else:
                    st.success("Fill level is low.")
else:
    st.warning("No bins match your search/filter.")


# ==================================================
# FOOTER AND CLEANUP
# ==================================================

st.divider()
st.caption("Smart Waste Collection • Bin Management")
session.close()
