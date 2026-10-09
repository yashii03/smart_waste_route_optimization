import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text

from database.connection import engine


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
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

    div[data-testid="stDataFrame"] {
        border: 1px solid #176B70;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 5px 18px rgba(0,0,0,0.18);
    }

    .stButton > button {
        background: linear-gradient(135deg,#14B8A6,#0D9488);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 9px 22px;
        font-weight: 700;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg,#2DD4BF,#14B8A6);
        box-shadow: 0 6px 20px rgba(45,212,191,0.3);
        transform: translateY(-1px);
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
    '📊 Waste Collection Analytics'
    '</div>'
    '<div style="color:#B6D9D5;font-size:15px;margin-top:7px;">'
    'Monitor bin fill levels, estimated waste generation and collection status '
    'using live data from the MySQL database.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div style="color:#67E8F9;font-size:13px;font-weight:600;margin-bottom:8px;">'
    '📈 DATA INSIGHTS & MONITORING'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# LOAD BIN DATA
# ==================================================

try:
    with engine.connect() as connection:
        bins_data = pd.read_sql(
            text(
                """
                SELECT
                    bin_code,
                    location_name,
                    capacity_kg,
                    fill_level,
                    waste_type,
                    status
                FROM bins
                ORDER BY bin_code
                """
            ),
            connection
        )
except Exception as e:
    st.error(f"Could not load bin data: {e}")
    st.stop()


if bins_data.empty:
    st.warning("No bin data is available for analytics.")
    st.stop()


# ==================================================
# CALCULATE ESTIMATED WASTE
# ==================================================

bins_data["estimated_waste_kg"] = (
    bins_data["capacity_kg"]
    * bins_data["fill_level"]
    / 100
)


# ==================================================
# SUMMARY METRICS
# ==================================================

st.subheader("📌 Current System Summary")

col1, col2, col3, col4 = st.columns(4)

total_bins = len(bins_data)
estimated_waste = bins_data["estimated_waste_kg"].sum()
average_fill = bins_data["fill_level"].mean()
high_fill = (bins_data["fill_level"] >= 80).sum()

total_bins_card = (
    '<div style="'
    'background:linear-gradient(135deg,#102A43,#123C5A);'
    'border:1px solid #22D3EE;border-radius:16px;padding:18px;'
    'height:110px;box-shadow:0 6px 20px rgba(0,0,0,0.22);">'
    '<div style="color:#67E8F9;font-size:13px;font-weight:600;">🗑️ TOTAL BINS</div>'
    f'<div style="color:#F0FDFA;font-size:28px;font-weight:800;margin-top:8px;">{total_bins}</div>'
    '</div>'
)

waste_card = (
    '<div style="'
    'background:linear-gradient(135deg,#2B1F45,#362552);'
    'border:1px solid #A78BFA;border-radius:16px;padding:18px;'
    'height:110px;box-shadow:0 6px 20px rgba(0,0,0,0.22);">'
    '<div style="color:#C4B5FD;font-size:13px;font-weight:600;">♻️ ESTIMATED WASTE</div>'
    f'<div style="color:#F0FDFA;font-size:28px;font-weight:800;margin-top:8px;">{estimated_waste:.0f} kg</div>'
    '</div>'
)

fill_card = (
    '<div style="'
    'background:linear-gradient(135deg,#102E25,#123C32);'
    'border:1px solid #10B981;border-radius:16px;padding:18px;'
    'height:110px;box-shadow:0 6px 20px rgba(0,0,0,0.22);">'
    '<div style="color:#6EE7B7;font-size:13px;font-weight:600;">📈 AVERAGE FILL</div>'
    f'<div style="color:#F0FDFA;font-size:28px;font-weight:800;margin-top:8px;">{average_fill:.1f}%</div>'
    '</div>'
)

high_fill_card = (
    '<div style="'
    'background:linear-gradient(135deg,#3A2A0B,#49330B);'
    'border:1px solid #F59E0B;border-radius:16px;padding:18px;'
    'height:110px;box-shadow:0 6px 20px rgba(0,0,0,0.22);">'
    '<div style="color:#FCD34D;font-size:13px;font-weight:600;">⚠️ HIGH FILL BINS</div>'
    f'<div style="color:#F0FDFA;font-size:28px;font-weight:800;margin-top:8px;">{high_fill}</div>'
    '</div>'
)

with col1:
    st.markdown(total_bins_card, unsafe_allow_html=True)

with col2:
    st.markdown(waste_card, unsafe_allow_html=True)

with col3:
    st.markdown(fill_card, unsafe_allow_html=True)

with col4:
    st.markdown(high_fill_card, unsafe_allow_html=True)


st.divider()


# ==================================================
# PLOTLY THEME HELPER
# ==================================================

def apply_chart_theme(fig, title):
    fig.update_layout(
        title={
            "text": title,
            "font": {
                "size": 19,
                "color": "#CCFBF1"
            }
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(6,44,48,0.35)",
        font={
            "color": "#D9F8F3",
            "size": 13
        },
        margin={
            "l": 50,
            "r": 30,
            "t": 65,
            "b": 45
        },
        legend={
            "font": {
                "color": "#D9F8F3"
            }
        },
        hoverlabel={
            "bgcolor": "#07383D",
            "font_color": "#F0FDFA",
            "bordercolor": "#2DD4BF"
        }
    )

    fig.update_xaxes(
        gridcolor="#155E63",
        zerolinecolor="#155E63",
        linecolor="#155E63",
        tickfont={
            "color": "#B6D9D5"
        }
    )

    fig.update_yaxes(
        gridcolor="#155E63",
        zerolinecolor="#155E63",
        linecolor="#155E63",
        tickfont={
            "color": "#B6D9D5"
        }
    )

    return fig


# ==================================================
# BIN FILL LEVEL CHART
# ==================================================

st.subheader("📊 Bin Fill Levels")

fig_fill = px.bar(
    bins_data,
    x="bin_code",
    y="fill_level",
    text="fill_level",
    labels={
        "bin_code": "Bin",
        "fill_level": "Fill Level (%)"
    }
)

fig_fill.update_traces(
    marker_color="#14B8A6",
    marker_line_color="#67E8F9",
    marker_line_width=1,
    texttemplate="%{text:.0f}%",
    textposition="outside"
)

fig_fill.update_layout(
    yaxis_range=[0, 100],
    showlegend=False
)

apply_chart_theme(fig_fill, "Fill Level of Each Waste Bin")

st.plotly_chart(
    fig_fill,
    use_container_width=True
)


st.divider()


# ==================================================
# ESTIMATED WASTE CHART
# ==================================================

st.subheader("♻️ Estimated Waste by Bin")

fig_waste = px.bar(
    bins_data,
    x="bin_code",
    y="estimated_waste_kg",
    text="estimated_waste_kg",
    labels={
        "bin_code": "Bin",
        "estimated_waste_kg": "Estimated Waste (kg)"
    }
)

fig_waste.update_traces(
    marker_color="#A78BFA",
    marker_line_color="#C4B5FD",
    marker_line_width=1,
    texttemplate="%{text:.0f} kg",
    textposition="outside"
)

fig_waste.update_layout(
    showlegend=False
)

apply_chart_theme(fig_waste, "Estimated Waste Amount in Each Bin")

st.plotly_chart(
    fig_waste,
    use_container_width=True
)


st.divider()


# ==================================================
# WASTE TYPE + STATUS
# ==================================================

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🗑️ Waste Type Distribution")

    waste_type_data = (
        bins_data["waste_type"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    waste_type_data.columns = [
        "waste_type",
        "count"
    ]

    fig_waste_type = px.pie(
        waste_type_data,
        names="waste_type",
        values="count"
    )

    fig_waste_type.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(
            line=dict(
                color="#062C30",
                width=2
            )
        )
    )

    apply_chart_theme(
        fig_waste_type,
        "Distribution of Waste Types"
    )

    st.plotly_chart(
        fig_waste_type,
        use_container_width=True
    )

with col_right:
    st.subheader("🟢 Bin Status")

    status_data = (
        bins_data["status"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    status_data.columns = [
        "status",
        "count"
    ]

    fig_status = px.pie(
        status_data,
        names="status",
        values="count"
    )

    fig_status.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(
            line=dict(
                color="#062C30",
                width=2
            )
        )
    )

    apply_chart_theme(
        fig_status,
        "Bin Status Distribution"
    )

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )


st.divider()


# ==================================================
# DETAILED BIN TABLE
# ==================================================

st.subheader("📋 Detailed Bin Analytics")

display_data = bins_data.copy()

display_data["fill_level"] = (
    display_data["fill_level"].round(1)
)

display_data["estimated_waste_kg"] = (
    display_data["estimated_waste_kg"].round(1)
)

st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True
)
