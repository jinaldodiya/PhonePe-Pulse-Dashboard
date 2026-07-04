import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# 👉 Page config
st.set_page_config(page_title="PhonePe Dashboard", layout="wide")

# 👉 COLORFUL UI
st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg, #89f7fe, #66a6ff, #c471f5);
    color: black;
}
[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #ff9a9e, #fad0c4);
}
h1, h2, h3 {
    color: black;
}
</style>
""", unsafe_allow_html=True)

# 👉 Title
st.markdown("<h1 style='text-align: center;'>📊 PhonePe Dashboard</h1>", unsafe_allow_html=True)

# 👉 DB connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jinaldodiya@15",   
    database="phonepe"
)

df = pd.read_sql("SELECT * FROM aggregated_transaction", conn)

# 👉 Sidebar filters
st.sidebar.markdown("## 🎛️ Controls")
state = st.sidebar.selectbox("📍 Select State", df['state'].unique())
year = st.sidebar.selectbox("📅 Select Year", df['year'].unique())

filtered_df = df[(df['state'] == state) & (df['year'] == year)]

# 👉 Metrics
total_amount = filtered_df['amount'].sum()
total_count = filtered_df['count'].sum()

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style="background: linear-gradient(45deg,#ff9a9e,#fad0c4);
    padding:20px;border-radius:12px">
    <h3>💰 Total Amount</h3>
    <h2>₹ {total_amount:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: linear-gradient(45deg,#a1c4fd,#c2e9fb);
    padding:20px;border-radius:12px">
    <h3>🔢 Total Transactions</h3>
    <h2>{total_count:,}</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 👉 Charts
col3, col4 = st.columns(2)

with col3:
    fig1 = px.bar(
        filtered_df,
        x="transaction_type",
        y="amount",
        color="transaction_type",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig1, use_container_width=True)

with col4:
    fig2 = px.pie(
        filtered_df,
        names="transaction_type",
        values="count",
        hole=0.5
    )
    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

# 👉 Top States
st.markdown("## 🏆 Top 10 States")

top_states = df.groupby("state")["amount"].sum().sort_values(ascending=False).head(10).reset_index()

fig3 = px.bar(
    top_states,
    x="state",
    y="amount",
    color="amount",
    color_continuous_scale="rainbow"
)

fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig3, use_container_width=True)

# 👉 🌍 INDIA MAP (NO GEOJSON - FINAL)
st.markdown("## 🌍 India Map")

state_data = df.groupby("state")["amount"].sum().reset_index()

# 👉 clean names
state_data["state"] = state_data["state"].str.replace("-", " ")
state_data["state"] = state_data["state"].str.replace("&", "and")
state_data["state"] = state_data["state"].str.title()

fig_map = px.scatter_geo(
    state_data,
    locations="state",
    locationmode="country names",
    size="amount",
    color="amount",
    color_continuous_scale="rainbow"
)

fig_map.update_layout(
    geo_scope="asia",
    paper_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig_map, use_container_width=True)

# 👉 Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>✨ Made by Jinal 🚀</p>", unsafe_allow_html=True)