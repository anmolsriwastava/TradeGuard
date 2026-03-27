import streamlit as st
from datetime import datetime
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -----------------------------
# AI FUNCTIONS - REAL NEWS ANALYSIS
# -----------------------------
def get_live_news():
    """Fetch real supply chain news from API"""
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    if not NEWS_API_KEY:
        return []
    
    query = "port congestion OR shipping disruption OR supply chain crisis OR freight delay"
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}&pageSize=5&language=en"
    
    try:
        res = requests.get(url, timeout=10).json()
        articles = res.get("articles", [])
        
        # Filter relevant news
        keywords = ["shipping", "port", "logistics", "freight", "cargo", "supply chain", 
                    "container", "maritime", "delay", "disruption", "crisis", "war", "strike"]
        
        relevant = []
        for article in articles:
            text = (article.get("title", "") + " " + article.get("description", "")).lower()
            if any(k in text for k in keywords):
                relevant.append(article)
        return relevant[:5]
    except:
        return []

def calculate_risk_score(news_articles):
    """Calculate risk score from news (0-100)"""
    if not news_articles:
        return 20
    
    score = 0
    for article in news_articles:
        text = (article.get("title", "") + " " + article.get("description", "")).lower()
        
        # Crisis words (high impact)
        if any(w in text for w in ["war", "attack", "crisis", "strike", "blocked", "closed", "halted"]):
            score += 25
        # Disruption words (medium impact)
        if any(w in text for w in ["delay", "congestion", "disruption", "backlog", "slow", "waiting"]):
            score += 15
        # Price trends (low impact)
        if any(w in text for w in ["price", "surge", "shortage", "rising", "increase", "spike"]):
            score += 8
    
    return min(score, 100)

def get_risk_level(score):
    """Convert score to risk level"""
    if score >= 70:
        return "CRITICAL", "critical"
    elif score >= 50:
        return "HIGH", "high"
    elif score >= 30:
        return "MEDIUM", "medium"
    else:
        return "LOW", "low"

def get_recommendation(score):
    """Get recommended actions based on risk score"""
    if score >= 70:
        return """
        **⚠️ IMMEDIATE ACTION REQUIRED**
        • Transship via alternate route
        • Notify buyers immediately
        • File force majeure notice
        • Request deadline extensions
        """
    elif score >= 50:
        return """
        **📊 MONITOR CLOSELY**
        • Prepare contingency plans
        • Review alternative routes
        • Contact freight forwarder
        • Monitor corridor daily
        """
    elif score >= 30:
        return """
        **🔍 REVIEW OPTIONS**
        • No immediate action needed
        • Continue monitoring
        • Review risk factors
        """
    else:
        return """
        **✅ NORMAL OPERATIONS**
        • Proceed with shipments
        • Standard monitoring active
        • No action required
        """

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="TradeGuard", layout="wide")

# -----------------------------
# HIDE SIDEBAR & STYLES
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

.risk-card {
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    margin-bottom: 20px;
}

.risk-critical { background: linear-gradient(135deg, #e53935, #c62828); color: white; }
.risk-high { background: linear-gradient(135deg, #fb8c00, #f57c00); color: white; }
.risk-medium { background: linear-gradient(135deg, #fdd835, #fbc02d); color: black; }
.risk-low { background: linear-gradient(135deg, #43a047, #2e7d32); color: white; }

.news-card {
    padding: 12px;
    border-left: 4px solid #e53935;
    background: #fafafa;
    margin-bottom: 10px;
    border-radius: 8px;
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# GET LIVE DATA
# -----------------------------
with st.spinner("📡 Analyzing live supply chain data..."):
    live_news = get_live_news()
    live_risk = calculate_risk_score(live_news)
    risk_level, risk_class = get_risk_level(live_risk)
    recommendation = get_recommendation(live_risk)

# -----------------------------
# HEADER
# -----------------------------
col1, col2 = st.columns([4,1])

with col1:
    st.title("🚢 TradeGuard")
    st.caption("Supply Chain Decision Intelligence | Live AI Monitoring")

with col2:
    now = datetime.now().strftime("%d %b %H:%M")
    st.markdown(f"**{now}**")
    st.markdown(f"<span class='badge {risk_class}'>LIVE</span>", unsafe_allow_html=True)

st.divider()

# -----------------------------
# LIVE RISK METRICS (UPDATED)
# -----------------------------
m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.metric("Live Risk Score", f"{live_risk}/100", delta=None)
with m2:
    st.metric("Risk Level", risk_level, delta=None)
with m3:
    st.metric("Active News", len(live_news), delta=None)
with m4:
    st.metric("Avg Risk (Week)", "52", delta="-12%")
with m5:
    st.metric("Shipments", "6", delta=None)

st.divider()

# -----------------------------
# LIVE RISK CARD
# -----------------------------
st.markdown(f"""
<div class="risk-card risk-{risk_class}">
    <h1 style="font-size: 48px; margin:0;">{live_risk}/100</h1>
    <h2 style="margin:0;">{risk_level} RISK</h2>
    <p style="margin-top: 10px;">{recommendation.split(chr(10))[0]}</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📰 Live News", "💡 Intelligence", "📈 Trends"])

# =============================
# TAB 1 — DASHBOARD
# =============================
with tab1:
    st.subheader("Active Shipments")

    shipments = [
        {"id":"CNSH772341","risk":f"{risk_level} {live_risk}" if risk_level == "CRITICAL" else "CRITICAL 91","route":"Nhava Sheva → Rotterdam","delay":"7–12d","cost":"₹513K"},
        {"id":"INMU456789","risk":f"{risk_level} {live_risk}" if risk_level == "HIGH" else "HIGH 74","route":"Nhava Sheva → Jebel Ali","delay":"4–7d","cost":"₹111K"},
        {"id":"COCHN887234","risk":f"{risk_level} {live_risk}" if risk_level == "MEDIUM" else "MEDIUM 38","route":"Kochi → Miami","delay":"4–7d","cost":"₹140K"}
    ]

    for s in shipments:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # Determine badge class
        if "CRITICAL" in s["risk"]:
            badge_class = "critical"
        elif "HIGH" in s["risk"]:
            badge_class = "high"
        elif "MEDIUM" in s["risk"]:
            badge_class = "medium"
        else:
            badge_class = "low"
        
        st.markdown(f"**{s['id']}** <span class='badge {badge_class}'>{s['risk']}</span>", unsafe_allow_html=True)
        st.write(s["route"])
        st.caption(f"Delay: {s['delay']} | Exposure: {s['cost']}")
        st.markdown("</div>", unsafe_allow_html=True)

# =============================
# TAB 2 — LIVE NEWS
# =============================
with tab2:
    st.subheader("📰 Live Supply Chain News")
    st.caption("Real-time news analysis from global sources")
    
    if live_news:
        for article in live_news:
            st.markdown(f"""
            <div class="news-card">
                <strong>{article.get('title', 'No title')}</strong>
                <p style="color:#666; font-size:13px; margin-top:5px;">
                    {article.get('description', 'No description')[:200]}...
                </p>
                <p style="color:#999; font-size:11px;">Source: NewsAPI | {datetime.now().strftime('%H:%M')}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No relevant news found at this time")

# =============================
# TAB 3 — INTELLIGENCE
# =============================
with tab3:
    st.subheader("🎯 AI Analysis")
    
    st.markdown(f"<span class='badge {risk_class}'>{risk_level} RISK - {live_risk}/100</span>", unsafe_allow_html=True)
    
    st.markdown(f"""
    ### Current Risk Analysis
    **Risk Score:** {live_risk}/100
    **Level:** {risk_level}
    
    ### Recommended Actions
    {recommendation}
    
    ### Risk Factors Detected
    """)
    
    # Show what triggered the risk
    crisis_detected = False
    disruption_detected = False
    price_detected = False
    
    for article in live_news:
        text = (article.get("title", "") + " " + article.get("description", "")).lower()
        if any(w in text for w in ["war", "attack", "crisis", "strike"]):
            crisis_detected = True
        if any(w in text for w in ["delay", "congestion", "disruption"]):
            disruption_detected = True
        if any(w in text for w in ["price", "surge", "shortage"]):
            price_detected = True
    
    if crisis_detected:
        st.warning("⚠️ Crisis signals detected (war, attacks, strikes)")
    if disruption_detected:
        st.warning("📉 Disruption signals detected (delays, congestion)")
    if price_detected:
        st.info("📈 Price trend signals detected (surge, shortage)")
    if not any([crisis_detected, disruption_detected, price_detected]):
        st.success("✅ No major disruption signals detected")

# =============================
# TAB 4 — RISK TRENDS
# =============================
with tab4:
    st.subheader("Risk Trend Analysis")
    
    # Sample historical data - you can build this from saved data
    data = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Risk Score": [45, 52, 60, 72, 85, 91, live_risk]
    })
    
    st.line_chart(data.set_index("Day"))
    st.caption("Rising trend indicates increasing disruption probability")
    
    st.info(f"**Current Risk:** {live_risk}/100 - {risk_level}")

# -----------------------------
# FOOTER
# -----------------------------
st.divider()
st.caption("🚢 TradeGuard — AI-Powered Supply Chain Decision Intelligence | Real-time News Analysis")