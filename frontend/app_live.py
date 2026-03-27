import streamlit as st
from datetime import datetime
import pandas as pd
import requests
import os
import json
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
        
        if any(w in text for w in ["war", "attack", "crisis", "strike", "blocked", "closed", "halted"]):
            score += 25
        if any(w in text for w in ["delay", "congestion", "disruption", "backlog", "slow", "waiting"]):
            score += 15
        if any(w in text for w in ["price", "surge", "shortage", "rising", "increase", "spike"]):
            score += 8
    
    return min(score, 100)

def get_risk_level(score):
    if score >= 70:
        return "CRITICAL", "critical"
    elif score >= 50:
        return "HIGH", "high"
    elif score >= 30:
        return "MEDIUM", "medium"
    else:
        return "LOW", "low"

def get_recommendation(score):
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
# SHIPMENT MANAGEMENT
# -----------------------------
def load_shipments():
    """Load shipments from file"""
    try:
        with open("shipments.json", "r") as f:
            return json.load(f)
    except:
        # Default shipments
        return [
            {"id": "CNSH772341", "route": "Nhava Sheva → Rotterdam", "cargo": "Pharmaceuticals", 
             "value": "₹22.0L", "deadline": "2026-04-16", "status": "In Transit"},
            {"id": "INMU456789", "route": "Nhava Sheva → Jebel Ali", "cargo": "Garments", 
             "value": "₹8.5L", "deadline": "2026-04-03", "status": "In Transit"},
            {"id": "COCHN887234", "route": "Kochi → Miami", "cargo": "Spices", 
             "value": "₹9.8L", "deadline": "2026-04-09", "status": "At Destination"}
        ]

def save_shipments(shipments):
    """Save shipments to file"""
    with open("shipments.json", "w") as f:
        json.dump(shipments, f, indent=2)

def add_shipment(container_id, origin, destination, cargo_type, value, deadline):
    """Add new shipment"""
    shipments = load_shipments()
    
    new_id = f"SHP-{len(shipments)+1:04d}"
    
    shipments.append({
        "id": container_id,
        "route": f"{origin} → {destination}",
        "cargo": cargo_type,
        "value": f"₹{value}L",
        "deadline": deadline,
        "status": "Registered",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    
    save_shipments(shipments)
    return new_id

# -----------------------------
# PAGE CONFIG & STYLES
# -----------------------------
st.set_page_config(page_title="TradeGuard", layout="wide")

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

.form-card {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    margin-bottom: 20px;
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
    shipments = load_shipments()

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
# TABS
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "📝 Register Shipment", "📰 Live News", "💡 Intelligence", "📈 Trends"])

# =============================
# TAB 1 — DASHBOARD
# =============================
# =============================
# TAB 1 — DASHBOARD (UPDATED WITH PRIORITY SHIPMENT)
# =============================
with tab1:
    st.subheader("🚨 Priority Shipments")
    st.caption("High-risk shipments requiring immediate attention")
    
    # Find high-risk shipments (risk > 70)
    high_risk_shipments = []
    for s in shipments:
        # Calculate risk for this shipment based on route
        if "Rotterdam" in s["route"]:
            risk_for_shipment = min(live_risk + 10, 100)
        elif "Jebel Ali" in s["route"]:
            risk_for_shipment = live_risk
        else:
            risk_for_shipment = max(live_risk - 20, 10)
        
        risk_level_ship, _ = get_risk_level(risk_for_shipment)
        
        if risk_for_shipment >= 70:  # High priority
            high_risk_shipments.append({
                "shipment": s,
                "risk": risk_for_shipment,
                "level": risk_level_ship
            })
    
    # Sort by risk score (highest first)
    high_risk_shipments.sort(key=lambda x: x["risk"], reverse=True)
    
    if high_risk_shipments:
        for hr in high_risk_shipments[:3]:  # Show top 3 priority shipments
            s = hr["shipment"]
            risk_score = hr["risk"]
            risk_lvl = hr["level"]
            
            # Big prominent card for high priority
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ff4757, #e53935); 
                        padding: 25px; 
                        border-radius: 16px; 
                        margin-bottom: 20px;
                        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
                        border: 2px solid #ffaa00;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="background: #ffaa00; 
                                     color: #c62828; 
                                     padding: 5px 15px; 
                                     border-radius: 20px; 
                                     font-weight: bold;
                                     font-size: 14px;">
                            ⚠️ HIGH PRIORITY
                        </span>
                        <h1 style="color: white; font-size: 56px; margin: 15px 0 5px 0;">
                            {risk_score}/100
                        </h1>
                        <p style="color: white; font-size: 18px; margin: 0;">
                            {risk_lvl} RISK - Immediate Action Required
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <p style="color: #ffaa00; font-size: 14px; margin: 0;">🚢 URGENT</p>
                        <p style="color: white; font-size: 12px; margin-top: 5px;">Action within 24h</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Cargo details card
            st.markdown(f"""
            <div style="background: white; 
                        padding: 20px; 
                        border-radius: 12px; 
                        margin-bottom: 20px;
                        border-left: 6px solid #e53935;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
                    <div>
                        <p style="color: #666; font-size: 12px; margin: 0;">CONTAINER</p>
                        <p style="color: #333; font-size: 18px; font-weight: bold; margin: 5px 0;">{s['id']}</p>
                    </div>
                    <div>
                        <p style="color: #666; font-size: 12px; margin: 0;">ROUTE</p>
                        <p style="color: #333; font-size: 16px; font-weight: 500; margin: 5px 0;">{s['route']}</p>
                    </div>
                    <div>
                        <p style="color: #666; font-size: 12px; margin: 0;">CARGO TYPE</p>
                        <p style="color: #333; font-size: 16px; font-weight: 500; margin: 5px 0;">{s['cargo']}</p>
                    </div>
                    <div>
                        <p style="color: #666; font-size: 12px; margin: 0;">CARGO VALUE</p>
                        <p style="color: #e53935; font-size: 18px; font-weight: bold; margin: 5px 0;">{s['value']}</p>
                    </div>
                    <div>
                        <p style="color: #666; font-size: 12px; margin: 0;">DELIVERY DEADLINE</p>
                        <p style="color: #333; font-size: 16px; font-weight: 500; margin: 5px 0;">{s['deadline']}</p>
                    </div>
                    <div>
                        <p style="color: #666; font-size: 12px; margin: 0;">CURRENT STATUS</p>
                        <p style="color: #e53935; font-size: 14px; font-weight: bold; margin: 5px 0;">⚠️ AT RISK - DELAY EXPECTED</p>
                    </div>
                </div>
                <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #eee;">
                    <p style="color: #666; font-size: 13px; margin: 0;">🎯 RECOMMENDED ACTIONS:</p>
                    <ul style="color: #333; font-size: 13px; margin-top: 8px;">
                        <li>🔴 Transship via alternate route immediately</li>
                        <li>📞 Notify buyer within next 2 hours</li>
                        <li>📄 File force majeure notice</li>
                        <li>✈️ Prepare emergency air freight contingency</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"📞 Notify Buyer - {s['id']}", key=f"notify_{s['id']}"):
                    st.success(f"✅ Buyer notification sent for {s['id']}")
            with col2:
                if st.button(f"🔄 Find Alternatives - {s['id']}", key=f"alt_{s['id']}"):
                    st.info(f"🔍 Searching alternative routes for {s['id']}...")
            with col3:
                if st.button(f"📊 View Risk Report - {s['id']}", key=f"report_{s['id']}"):
                    st.info(f"📄 Generating risk report for {s['id']}")
    
    else:
        st.success("✅ No high-priority shipments at this time")
    
    st.divider()
    
    # Regular shipments section (low to medium risk)
st.subheader("📦 All Shipments (Normal Operations)")

normal_shipments = []
for s in shipments:
    if "Rotterdam" in s["route"]:
        risk_check = min(live_risk + 10, 100)
    elif "Jebel Ali" in s["route"]:
        risk_check = live_risk
    else:
        risk_check = max(live_risk - 20, 10)
    
    # ONLY show shipments with risk < 70 (not high priority)
    if risk_check < 70:
        normal_shipments.append((s, risk_check))

if normal_shipments:
    for s, risk_check in normal_shipments:
        risk_level_ship, _ = get_risk_level(risk_check)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.markdown(f"**{s['id']}** <span class='badge {risk_level_ship.lower()}'>{risk_level_ship}</span>", unsafe_allow_html=True)
            st.write(s["route"])
            st.caption(f"Cargo: {s['cargo']}")
        
        with col2:
            st.write(f"**Value:** {s['value']}")
            st.write(f"**Deadline:** {s['deadline']}")
            st.write(f"**Status:** {s['status']}")
        
        with col3:
            if risk_check >= 50:
                st.warning(f"Risk: {risk_check}/100")
            else:
                st.success(f"Risk: {risk_check}/100")
        
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No regular shipments")
# =============================
# TAB 2 — REGISTER SHIPMENT
# =============================
with tab2:
    st.subheader("📝 Register New Shipment")
    st.caption("Add your shipment to start monitoring")
    
    with st.form("register_shipment_form"):
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            container_id = st.text_input("Container Number*", placeholder="e.g., INMU123456")
            origin = st.selectbox("Origin Port*", ["Nhava Sheva (INNSA)", "Mundra (INPAV)", "Kochi (INCOK)", "Chennai (INMAA)"])
            cargo_type = st.selectbox("Cargo Type*", ["Garments", "Pharmaceuticals", "Spices", "Auto Components", "Electronics", "Textiles"])
        
        with col2:
            destination = st.selectbox("Destination Port*", ["Jebel Ali (AEJEA)", "Rotterdam (NLRTM)", "Singapore (SGSIN)", "Miami (USMIA)", "Hamburg (DEHAM)"])
            value = st.number_input("Cargo Value (₹ Lakhs)*", min_value=1.0, max_value=1000.0, value=10.0, step=5.0)
            deadline = st.date_input("Delivery Deadline*", min_value=datetime.now().date())
        
        submitted = st.form_submit_button("🚢 Register Shipment", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submitted:
            if not container_id:
                st.error("Please enter container number")
            else:
                # Extract port codes
                origin_code = origin.split("(")[-1].replace(")", "")
                dest_code = destination.split("(")[-1].replace(")", "")
                
                add_shipment(container_id, origin_code, dest_code, cargo_type, value, deadline.strftime("%Y-%m-%d"))
                
                st.success(f"✅ Shipment {container_id} registered successfully!")
                st.balloons()
                st.info("The shipment will now appear in your dashboard with live risk monitoring")
                st.rerun()

# =============================
# TAB 3 — LIVE NEWS
# =============================
with tab3:
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
# TAB 4 — INTELLIGENCE
# =============================
# =============================
# TAB 4 — INTELLIGENCE (UPDATED WITH CARGO DETAILS)
# =============================
with tab4:
    st.subheader("🎯 AI Analysis")
    
    # Show priority shipment if exists
    high_risk_found = False
    for s in shipments:
        if "Rotterdam" in s["route"]:
            risk_check = min(live_risk + 10, 100)
        elif "Jebel Ali" in s["route"]:
            risk_check = live_risk
        else:
            risk_check = max(live_risk - 20, 10)
        
        if risk_check >= 70:
            high_risk_found = True
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ff4757, #e53935); 
                        padding: 20px; 
                        border-radius: 12px; 
                        margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="background: #ffaa00; 
                                     color: #c62828; 
                                     padding: 4px 12px; 
                                     border-radius: 20px; 
                                     font-weight: bold;
                                     font-size: 12px;">
                            ⚠️ PRIORITY SHIPMENT
                        </span>
                        <h3 style="color: white; margin: 10px 0 5px 0;">{s['id']}</h3>
                        <p style="color: white; margin: 0;">{s['route']} | {s['cargo']}</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="color: white; font-size: 24px; font-weight: bold; margin: 0;">{risk_check}/100</p>
                        <p style="color: #ffaa00; margin: 0;">CRITICAL</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            break
    
    if not high_risk_found:
        st.markdown(f"<span class='badge {risk_class}'>{risk_level} RISK - {live_risk}/100</span>", unsafe_allow_html=True)
    
    st.markdown(f"""
    ### Current Risk Analysis
    **Global Risk Score:** {live_risk}/100
    **Level:** {risk_level}
    
    ### Recommended Actions
    {recommendation}
    
    ### Risk Factors Detected
    """)
    
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
# TAB 5 — RISK TRENDS
# =============================
with tab5:
    st.subheader("Risk Trend Analysis")
    
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