import streamlit as st
from datetime import datetime
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="TradeGuard", layout="wide")

# -----------------------------
# HIDE SIDEBAR
# -----------------------------
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none;}
section[data-testid="stSidebarNav"] {display: none;}

.badge {
    padding: 6px 12px;
    border-radius: 8px;
    color: white;
    font-weight: 600;
    font-size: 13px;
}

.critical { background-color: #e53935; }
.high { background-color: #fb8c00; }
.medium { background-color: #fdd835; color: black; }
.low { background-color: #43a047; }

.card {
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #eee;
    margin-bottom: 15px;
    background-color: white;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HELPERS
# -----------------------------
def get_badge(risk):
    if "CRITICAL" in risk:
        return "<span class='badge critical'>CRITICAL</span>"
    elif "HIGH" in risk:
        return "<span class='badge high'>HIGH</span>"
    elif "MEDIUM" in risk:
        return "<span class='badge medium'>MEDIUM</span>"
    else:
        return "<span class='badge low'>LOW</span>"

# -----------------------------
# HEADER
# -----------------------------
col1, col2 = st.columns([4,1])

with col1:
    st.title("TradeGuard")
    st.caption("Supply Chain Decision Intelligence")

with col2:
    now = datetime.now().strftime("%d %b %H:%M")
    st.markdown(f"**{now}**")
    st.caption("Live system")

st.divider()

# -----------------------------
# METRICS
# -----------------------------
m1, m2, m3, m4, m5 = st.columns(5)

m1.metric("Critical", "1")
m2.metric("High Risk", "2")
m3.metric("Exposure", "₹7.9L")
m4.metric("Avg Risk", "52")
m5.metric("Shipments", "6")

st.divider()

# -----------------------------
# TABS (INVESTOR UI)
# -----------------------------
tab1, tab2, tab3 = st.tabs(["Dashboard", "Shipment Intelligence", "Risk Trends"])

# =============================
# TAB 1 — DASHBOARD
# =============================
with tab1:
    st.subheader("Active Shipments")

    shipments = [
        {"id":"CNSH772341","risk":"CRITICAL 91","route":"Nhava Sheva → Rotterdam","delay":"7–12d","cost":"₹513K"},
        {"id":"INMU456789","risk":"HIGH 74","route":"Nhava Sheva → Jebel Ali","delay":"4–7d","cost":"₹111K"},
        {"id":"COCHN887234","risk":"HIGH 67","route":"Kochi → Miami","delay":"4–7d","cost":"₹140K"}
    ]

    selected = st.radio(
        "Select Shipment",
        [s["id"] for s in shipments],
        horizontal=True
    )

    for s in shipments:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        badge = get_badge(s["risk"])

        st.markdown(f"**{s['id']}** {badge}", unsafe_allow_html=True)
        st.write(s["route"])
        st.caption(f"Delay: {s['delay']} | Exposure: {s['cost']}")

        st.markdown("</div>", unsafe_allow_html=True)

# =============================
# TAB 2 — INTELLIGENCE
# =============================
with tab2:
    st.subheader("Shipment Analysis")

    st.markdown("<span class='badge critical'>CRITICAL</span>", unsafe_allow_html=True)

    st.markdown("""
    Route: Nhava Sheva → Rotterdam  
    Cargo: Pharmaceuticals  
    Deadline: 16 Apr  
    Value: ₹22L  
    """)

    st.warning("Major rerouting delays due to Red Sea disruption.")

    st.subheader("Recommended Action")

    st.success("Transship at Colombo")

    st.write("Reduce delay impact by switching vessel before disruption zone.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Notify Buyer**")
        st.caption("Send delay notice")

    with col2:
        st.markdown("**Request Extension**")
        st.caption("Extend delivery deadline")

# =============================
# TAB 3 — RISK TRENDS
# =============================
with tab3:
    st.subheader("Risk Trend (Last 7 Days)")

    data = pd.DataFrame({
        "Day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
        "Risk Score": [45, 52, 60, 72, 85, 91, 88]
    })

    st.line_chart(data.set_index("Day"))

    st.caption("Rising trend indicates increasing disruption probability")

# -----------------------------
# FOOTER
# -----------------------------
st.divider()
st.caption("TradeGuard — Proactive Decision Intelligence")