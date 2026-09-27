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

st.title("📊 Waste Collection Analytics")

st.write(
    "Analyze bin fill levels, estimated waste generation "
    "and vehicle capacity using data from the MySQL database."
)

st.divider()


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

with col1:

    st.metric(
        "🗑️ Total Bins",
        len(bins_data)
    )

with col2:

    st.metric(
        "♻️ Estimated Waste",
        f"{bins_data['estimated_waste_kg'].sum():.0f} kg"
    )

with col3:

    st.metric(
        "📈 Average Fill Level",
        f"{bins_data['fill_level'].mean():.1f}%"
    )

with col4:

    high_fill = (
        bins_data["fill_level"] >= 80
    ).sum()

    st.metric(
        "⚠️ High Fill Bins",
        high_fill
    )


st.divider()


# ==================================================
# BIN FILL LEVEL CHART
# ==================================================

st.subheader("📊 Bin Fill Levels")

fig_fill = px.bar(
    bins_data,
    x="bin_code",
    y="fill_level",
    title="Fill Level of Each Waste Bin",
    labels={
        "bin_code": "Bin",
        "fill_level": "Fill Level (%)"
    },
    text="fill_level"
)

fig_fill.update_layout(
    yaxis_range=[0, 100]
)

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
    title="Estimated Waste Amount in Each Bin",
    labels={
        "bin_code": "Bin",
        "estimated_waste_kg": "Estimated Waste (kg)"
    },
    text="estimated_waste_kg"
)

st.plotly_chart(
    fig_waste,
    use_container_width=True
)


st.divider()


# ==================================================
# WASTE TYPE DISTRIBUTION
# ==================================================

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
    values="count",
    title="Distribution of Waste Types"
)

st.plotly_chart(
    fig_waste_type,
    use_container_width=True
)


st.divider()


# ==================================================
# STATUS DISTRIBUTION
# ==================================================

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
    values="count",
    title="Bin Status Distribution"
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