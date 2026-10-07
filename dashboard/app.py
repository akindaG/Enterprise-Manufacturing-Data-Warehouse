"""Interactive analytics layer for the Enterprise Manufacturing Data Platform."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine, text

from etl_pipeline.config import database_url_from_environment

st.set_page_config(page_title="Manufacturing Intelligence", page_icon="🏭", layout="wide")


@st.cache_resource
def get_engine():
    return create_engine(database_url_from_environment(), pool_pre_ping=True)


@st.cache_data(ttl=60)
def load_data() -> pd.DataFrame:
    query = text("SELECT * FROM vw_production_dashboard ORDER BY production_date, production_key")
    with get_engine().connect() as connection:
        frame = pd.read_sql(query, connection)
    frame["production_date"] = pd.to_datetime(frame["production_date"])
    return frame


st.title("🏭 Enterprise Manufacturing Intelligence")
st.caption("Production • Quality • Machine History • Cost • Factory Performance")

try:
    df = load_data()
except Exception as exc:
    st.error("Unable to load the warehouse semantic view.")
    st.code(str(exc))
    st.stop()

if df.empty:
    st.warning("The warehouse contains no production facts yet. Run the ETL demo first.")
    st.stop()

with st.sidebar:
    st.header("Filters")
    factories = ["All"] + sorted(df["factory_name"].dropna().unique().tolist())
    products = ["All"] + sorted(df["product_name"].dropna().unique().tolist())
    machines = ["All"] + sorted(df["machine_name"].dropna().unique().tolist())
    factory = st.selectbox("Factory", factories)
    product = st.selectbox("Product", products)
    machine = st.selectbox("Machine", machines)
    min_date = df["production_date"].min().date()
    max_date = df["production_date"].max().date()
    date_range = st.date_input("Production date", value=(min_date, max_date), min_value=min_date, max_value=max_date)

filtered = df.copy()
if factory != "All":
    filtered = filtered[filtered["factory_name"] == factory]
if product != "All":
    filtered = filtered[filtered["product_name"] == product]
if machine != "All":
    filtered = filtered[filtered["machine_name"] == machine]
if len(date_range) == 2:
    start, end = map(pd.Timestamp, date_range)
    filtered = filtered[(filtered["production_date"] >= start) & (filtered["production_date"] <= end)]

if filtered.empty:
    st.warning("No rows match the selected filters.")
    st.stop()

units = int(filtered["quantity_produced"].sum())
defects = int(filtered["defect_count"].sum())
good_units = int(filtered["good_quantity"].sum())
cost = float(filtered["production_cost"].sum())
minutes = int(filtered["production_time"].sum())
defect_rate = (defects / units * 100) if units else 0.0
cost_per_unit = (cost / units) if units else 0.0

cols = st.columns(6)
cols[0].metric("Units Produced", f"{units:,}")
cols[1].metric("Good Units", f"{good_units:,}")
cols[2].metric("Defects", f"{defects:,}")
cols[3].metric("Defect Rate", f"{defect_rate:.2f}%")
cols[4].metric("Production Cost", f"{cost:,.0f}")
cols[5].metric("Cost / Unit", f"{cost_per_unit:,.2f}")

st.divider()

daily = (
    filtered.groupby("production_date", as_index=False)
    .agg(quantity_produced=("quantity_produced", "sum"), defect_count=("defect_count", "sum"), production_cost=("production_cost", "sum"))
)
st.plotly_chart(
    px.line(daily, x="production_date", y="quantity_produced", markers=True, title="Production Trend"),
    use_container_width=True,
)

left, right = st.columns(2)
with left:
    factory_perf = filtered.groupby("factory_name", as_index=False).agg(
        units=("quantity_produced", "sum"), defects=("defect_count", "sum"), cost=("production_cost", "sum")
    )
    factory_perf["defect_rate"] = factory_perf["defects"] / factory_perf["units"].replace(0, pd.NA) * 100
    st.plotly_chart(
        px.bar(factory_perf, x="factory_name", y="units", text_auto=True, title="Production by Factory"),
        use_container_width=True,
    )
with right:
    product_perf = filtered.groupby("product_name", as_index=False).agg(
        units=("quantity_produced", "sum"), defects=("defect_count", "sum")
    )
    product_perf["defect_rate"] = product_perf["defects"] / product_perf["units"].replace(0, pd.NA) * 100
    st.plotly_chart(
        px.bar(product_perf, x="product_name", y="defect_rate", text_auto=".2f", title="Defect Rate by Product"),
        use_container_width=True,
    )

left, right = st.columns(2)
with left:
    machine_perf = filtered.groupby(["machine_id", "machine_name"], as_index=False).agg(
        units=("quantity_produced", "sum"), defects=("defect_count", "sum")
    )
    st.plotly_chart(
        px.bar(machine_perf, x="machine_name", y="units", hover_data=["machine_id", "defects"], title="Machine Throughput"),
        use_container_width=True,
    )
with right:
    cost_by_product = filtered.groupby("product_name", as_index=False)["production_cost"].sum()
    st.plotly_chart(
        px.pie(cost_by_product, names="product_name", values="production_cost", title="Production Cost Mix"),
        use_container_width=True,
    )

st.subheader("Operational Detail")
st.caption(f"Filtered production time: {minutes:,} minutes")
st.dataframe(
    filtered[[
        "production_id", "production_date", "factory_name", "product_name", "machine_name",
        "shift_name", "quantity_produced", "good_quantity", "defect_count", "defect_rate",
        "production_time", "production_cost", "cost_per_unit",
    ]],
    use_container_width=True,
    hide_index=True,
)

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered data", csv, "manufacturing_analytics.csv", "text/csv")
