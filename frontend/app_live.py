import streamlit as st
import pandas as pd
import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from models.forecast import RiskForecaster

forecaster = RiskForecaster()
load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM — VyaparAI
# ─────────────────────────────────────────────────────────────────────────────

DESIGN = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=IBM+Plex+Mono:wght@300;400;500&family=Lato:wght@300;400;700&display=swap');

:root {
    --navy:       #0a1628;
    --navy-mid:   #0f2040;
    --navy-light: #162d55;
    --slate:      #1e3a5f;
    --gold:       #c9a84c;
    --gold-light: #e8c97a;
    --gold-dim:   #7a6030;
    --mist:       #e8edf4;
    --mist-mid:   #c5cfdc;
    --mist-dim:   #8a9ab5;
    --white:      #f5f8ff;
    --critical:   #c0392b;
    --high:       #d4751a;
    --medium:     #b8941a;
    --low:        #1a7a4a;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: var(--navy) !important;
    font-family: 'Lato', sans-serif !important;
    color: var(--mist) !important;
}

#MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"], .stDeployButton { display: none !important; }

.main .block-container { padding: 0 !important; max-width: 100% !important; }

h1,h2,h3,h4,h5,h6,p,span,div,label { color: var(--mist) !important; }

.vyapar-topbar {
    background: linear-gradient(90deg, var(--navy) 0%, var(--navy-mid) 60%, var(--slate) 100%);
    border-bottom: 1px solid var(--gold-dim);
    padding: 0 40px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 1000;
}

.topbar-brand { display: flex; align-items: baseline; gap: 10px; }
.topbar-logo { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 700; color: var(--gold) !important; letter-spacing: 0.04em; }
.topbar-tagline { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: var(--mist-dim) !important; letter-spacing: 0.12em; text-transform: uppercase; }
.topbar-right { display: flex; align-items: center; gap: 28px; }
.topbar-time { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: var(--mist-dim) !important; letter-spacing: 0.06em; }

.live-pill { display: flex; align-items: center; gap: 6px; background: rgba(201,168,76,0.1); border: 1px solid var(--gold-dim); border-radius: 20px; padding: 4px 12px; font-family: 'IBM Plex Mono', monospace; font-size: 10px; font-weight: 500; color: var(--gold) !important; letter-spacing: 0.1em; text-transform: uppercase; }
.live-dot { width: 6px; height: 6px; background: var(--gold); border-radius: 50%; animation: pulse 1.8s ease-in-out infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(0.7); } }

.hero-banner { background: linear-gradient(135deg, var(--navy-mid) 0%, var(--slate) 100%); border-bottom: 1px solid rgba(201,168,76,0.15); padding: 36px 40px; display: grid; grid-template-columns: 1fr auto; gap: 40px; align-items: center; }
.hero-label { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: var(--gold) !important; letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 8px; }
.hero-score { font-family: 'Playfair Display', serif; font-size: 72px; font-weight: 700; line-height: 1; letter-spacing: -0.02em; }
.hero-score-critical { color: #e74c3c !important; }
.hero-score-high { color: #e67e22 !important; }
.hero-score-medium { color: #f1c40f !important; }
.hero-score-low { color: #2ecc71 !important; }
.hero-meta { margin-top: 12px; display: flex; gap: 24px; align-items: center; }
.hero-level-badge { font-family: 'IBM Plex Mono', monospace; font-size: 11px; font-weight: 500; padding: 4px 14px; border-radius: 4px; letter-spacing: 0.1em; text-transform: uppercase; }
.badge-critical { background: rgba(192,57,43,0.2); border: 1px solid #c0392b; color: #e74c3c !important; }
.badge-high { background: rgba(212,117,26,0.2); border: 1px solid #d4751a; color: #e67e22 !important; }
.badge-medium { background: rgba(184,148,26,0.2); border: 1px solid #b8941a; color: #f1c40f !important; }
.badge-low { background: rgba(26,122,74,0.2); border: 1px solid #1a7a4a; color: #2ecc71 !important; }
.hero-updated { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: var(--mist-dim) !important; }
.hero-stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: rgba(201,168,76,0.1); border: 1px solid rgba(201,168,76,0.15); border-radius: 10px; overflow: hidden; }
.hero-stat { background: var(--navy); padding: 20px 24px; text-align: center; }
.hero-stat-val { font-family: 'IBM Plex Mono', monospace; font-size: 24px; font-weight: 500; color: var(--gold) !important; display: block; }
.hero-stat-lbl { font-family: 'Lato', sans-serif; font-size: 11px; color: var(--mist-dim) !important; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; display: block; }

.stTabs [data-baseweb="tab-list"] { background: var(--navy-mid) !important; border-bottom: 1px solid rgba(201,168,76,0.2) !important; padding: 0 40px !important; gap: 0 !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; border: none !important; border-bottom: 2px solid transparent !important; color: var(--mist-dim) !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 11px !important; font-weight: 400 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; padding: 16px 24px !important; }
.stTabs [aria-selected="true"] { color: var(--gold) !important; border-bottom-color: var(--gold) !important; }
.stTabs [data-baseweb="tab-panel"] { background: var(--navy) !important; padding: 0 !important; }

.content-area { padding: 32px 40px; }
.section-header { display: flex; align-items: baseline; gap: 16px; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid rgba(201,168,76,0.15); }
.section-title { font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 600; color: var(--white) !important; }
.section-count { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: var(--gold) !important; background: rgba(201,168,76,0.1); border: 1px solid var(--gold-dim); padding: 2px 8px; border-radius: 3px; }

.shipment-card { background: var(--navy-mid); border: 1px solid rgba(197,207,220,0.1); border-radius: 10px; padding: 24px 28px; margin-bottom: 14px; position: relative; overflow: hidden; }
.shipment-card::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; }
.card-critical::before { background: #e74c3c; }
.card-high::before { background: #e67e22; }
.card-medium::before { background: #f1c40f; }
.card-low::before { background: #2ecc71; }
.card-top { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 16px; }
.card-id { font-family: 'IBM Plex Mono', monospace; font-size: 16px; font-weight: 500; color: var(--white) !important; letter-spacing: 0.06em; }
.card-route { font-family: 'Lato', sans-serif; font-size: 13px; color: var(--mist-dim) !important; margin-top: 4px; display: flex; align-items: center; gap: 8px; }
.route-arrow { color: var(--gold-dim) !important; font-size: 12px; }
.card-risk-circle { display: flex; flex-direction: column; align-items: center; justify-content: center; width: 64px; height: 64px; border-radius: 50%; border: 2px solid; flex-shrink: 0; }
.circle-critical { border-color: #e74c3c; background: rgba(231,76,60,0.08); }
.circle-high { border-color: #e67e22; background: rgba(230,126,34,0.08); }
.circle-medium { border-color: #f1c40f; background: rgba(241,196,15,0.08); }
.circle-low { border-color: #2ecc71; background: rgba(46,204,113,0.08); }
.circle-score { font-family: 'IBM Plex Mono', monospace; font-size: 18px; font-weight: 500; }
.circle-label { font-family: 'IBM Plex Mono', monospace; font-size: 8px; letter-spacing: 0.05em; text-transform: uppercase; margin-top: 1px; }
.score-critical, .label-critical { color: #e74c3c !important; }
.score-high, .label-high { color: #e67e22 !important; }
.score-medium, .label-medium { color: #f1c40f !important; }
.score-low, .label-low { color: #2ecc71 !important; }
.card-meta { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; padding-top: 16px; border-top: 1px solid rgba(197,207,220,0.08); }
.meta-item-lbl { font-family: 'IBM Plex Mono', monospace; font-size: 9px; color: var(--mist-dim) !important; letter-spacing: 0.15em; text-transform: uppercase; display: block; margin-bottom: 4px; }
.meta-item-val { font-family: 'Lato', sans-serif; font-size: 14px; font-weight: 700; color: var(--mist) !important; display: block; }
.meta-item-val-gold { font-family: 'Lato', sans-serif; font-size: 14px; font-weight: 700; color: var(--gold) !important; display: block; }
.meta-item-val-delay { font-family: 'Lato', sans-serif; font-size: 14px; font-weight: 700; color: #e74c3c !important; display: block; }

.priority-alert { background: linear-gradient(135deg, #1a0505 0%, #160d00 100%); border: 1px solid rgba(231,76,60,0.4); border-radius: 12px; padding: 28px 32px; margin-bottom: 20px; position: relative; overflow: hidden; }
.priority-alert::after { content: 'PRIORITY'; position: absolute; top: 16px; right: -24px; background: #e74c3c; color: white !important; font-family: 'IBM Plex Mono', monospace; font-size: 9px; font-weight: 600; letter-spacing: 0.15em; padding: 4px 36px; transform: rotate(45deg); }
.priority-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 20px; }
.priority-score-display { font-family: 'Playfair Display', serif; font-size: 56px; font-weight: 700; color: #e74c3c !important; line-height: 1; }
.priority-score-sub { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: rgba(231,76,60,0.6) !important; margin-top: 4px; }
.priority-actions-label { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: var(--mist-dim) !important; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 10px; }
.priority-action-item { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; font-family: 'Lato', sans-serif; font-size: 13px; color: var(--mist) !important; }
.action-dot { width: 5px; height: 5px; background: #e74c3c; border-radius: 50%; flex-shrink: 0; }

.rec-panel { background: var(--navy-mid); border: 1px solid rgba(201,168,76,0.2); border-radius: 10px; padding: 24px 28px; margin-bottom: 20px; }
.rec-title { font-family: 'Playfair Display', serif; font-size: 16px; font-weight: 600; color: var(--gold) !important; margin-bottom: 16px; }
.rec-item { display: flex; align-items: flex-start; gap: 12px; padding: 10px 0; border-bottom: 1px solid rgba(197,207,220,0.06); font-family: 'Lato', sans-serif; font-size: 14px; color: var(--mist) !important; }
.rec-item:last-child { border-bottom: none; }
.rec-icon { font-size: 16px; flex-shrink: 0; margin-top: 1px; }

.news-item { background: var(--navy-mid); border: 1px solid rgba(197,207,220,0.08); border-radius: 8px; padding: 18px 22px; margin-bottom: 12px; border-left: 3px solid var(--gold-dim); }
.news-title { font-family: 'Lato', sans-serif; font-size: 14px; font-weight: 700; color: var(--white) !important; margin-bottom: 6px; }
.news-desc { font-family: 'Lato', sans-serif; font-size: 13px; color: var(--mist-dim) !important; line-height: 1.6; }
.news-meta { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: var(--gold-dim) !important; margin-top: 10px; display: flex; gap: 12px; }

.signal-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 20px; }
.signal-card { background: var(--navy-mid); border: 1px solid rgba(197,207,220,0.08); border-radius: 8px; padding: 16px 20px; display: flex; align-items: center; gap: 14px; }
.signal-icon { font-size: 20px; }
.signal-info-lbl { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: var(--mist-dim) !important; letter-spacing: 0.1em; text-transform: uppercase; display: block; }
.signal-info-val { font-family: 'Lato', sans-serif; font-size: 14px; font-weight: 700; color: var(--mist) !important; display: block; margin-top: 2px; }

.form-wrapper { background: var(--navy-mid); border: 1px solid rgba(201,168,76,0.15); border-radius: 12px; padding: 32px 36px; max-width: 720px; }
.form-title { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 600; color: var(--white) !important; margin-bottom: 6px; }
.form-subtitle { font-family: 'Lato', sans-serif; font-size: 13px; color: var(--mist-dim) !important; margin-bottom: 28px; }

.stTextInput input, .stNumberInput input, .stSelectbox select, .stDateInput input { background: var(--navy) !important; border: 1px solid rgba(201,168,76,0.2) !important; border-radius: 6px !important; color: var(--mist) !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 13px !important; padding: 10px 14px !important; }
.stButton button { background: transparent !important; border: 1px solid rgba(201,168,76,0.4) !important; border-radius: 6px !important; color: var(--gold) !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 11px !important; font-weight: 500 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; padding: 8px 18px !important; }
.stFormSubmitButton button { background: linear-gradient(135deg, var(--gold-dim), var(--gold)) !important; border: none !important; color: var(--navy) !important; font-weight: 700 !important; }

.forecast-row { display: grid; grid-template-columns: 100px 1fr 80px; gap: 16px; align-items: center; padding: 12px 0; border-bottom: 1px solid rgba(197,207,220,0.06); }
.forecast-date { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: var(--mist-dim) !important; }
.forecast-bar-track { background: rgba(197,207,220,0.06); border-radius: 3px; height: 6px; overflow: hidden; }
.forecast-bar-fill { height: 100%; border-radius: 3px; transition: width 0.6s ease; }
.forecast-score { font-family: 'IBM Plex Mono', monospace; font-size: 14px; font-weight: 500; text-align: right; }

.corridor-row { display: flex; align-items: center; justify-content: space-between; padding: 14px 0; border-bottom: 1px solid rgba(197,207,220,0.06); }
.corridor-name { font-family: 'Lato', sans-serif; font-size: 14px; font-weight: 700; color: var(--mist) !important; }
.corridor-sub { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: var(--mist-dim) !important; margin-top: 2px; }
.corridor-score-badge { font-family: 'IBM Plex Mono', monospace; font-size: 12px; font-weight: 500; padding: 4px 10px; border-radius: 4px; border: 1px solid; }

.empty-state { text-align: center; padding: 60px 20px; }
.empty-icon { font-size: 40px; margin-bottom: 16px; opacity: 0.5; }
.empty-title { font-family: 'Playfair Display', serif; font-size: 18px; color: var(--mist-dim) !important; margin-bottom: 8px; }
.empty-sub { font-family: 'Lato', sans-serif; font-size: 13px; color: var(--mist-dim) !important; opacity: 0.7; }
"""

# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def get_live_news():
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    if not NEWS_API_KEY:
        return []
    query = "port congestion OR shipping disruption OR supply chain crisis OR freight delay"
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}&pageSize=5&language=en"
    try:
        res = requests.get(url, timeout=10).json()
        articles = res.get("articles", [])
        keywords = ["shipping","port","logistics","freight","cargo","supply chain",
                    "container","maritime","delay","disruption","crisis","war","strike"]
        relevant = [a for a in articles
                    if any(k in (a.get("title","") + a.get("description","")).lower() for k in keywords)]
        return relevant[:5]
    except:
        return []

def calculate_delay_and_eta(risk_score, deadline_date):
    """Calculate predicted delay days and new estimated delivery date"""
    if risk_score >= 80:
        delay_days = 7 + (risk_score - 80) / 5
    elif risk_score >= 60:
        delay_days = 4 + (risk_score - 60) / 6.67
    elif risk_score >= 40:
        delay_days = 2 + (risk_score - 40) / 10
    elif risk_score >= 20:
        delay_days = 1 + (risk_score - 20) / 20
    else:
        delay_days = 0
    
    delay_days = round(delay_days, 1)
    
    if isinstance(deadline_date, str):
        deadline_date = datetime.strptime(deadline_date, "%Y-%m-%d")
    
    new_eta = deadline_date + timedelta(days=delay_days)
    
    if delay_days >= 7:
        delay_range = f"{int(delay_days)}-{int(delay_days + 3)} days"
    elif delay_days >= 4:
        delay_range = f"{int(delay_days)}-{int(delay_days + 2)} days"
    elif delay_days >= 1:
        delay_range = f"{int(delay_days)}-{int(delay_days + 1)} days"
    else:
        delay_range = "< 1 day"
    
    return {
        "delay_days": delay_days,
        "delay_range": delay_range,
        "original_deadline": deadline_date.strftime("%d %b %Y"),
        "estimated_delivery": new_eta.strftime("%d %b %Y"),
        "status": "DELAYED" if delay_days > 0 else "ON TIME"
    }

def calculate_risk_score(news_articles):
    if not news_articles:
        return 20
    score = 0
    for article in news_articles:
        text = (article.get("title","") + " " + article.get("description","")).lower()
        if any(w in text for w in ["war","attack","crisis","strike","blocked","closed","halted"]):
            score += 25
        if any(w in text for w in ["delay","congestion","disruption","backlog","slow","waiting"]):
            score += 15
        if any(w in text for w in ["price","surge","shortage","rising","increase","spike"]):
            score += 8
    return min(score, 100)

def get_risk_meta(score):
    if score >= 70:   return "CRITICAL", "critical", "#e74c3c"
    elif score >= 50: return "HIGH", "high", "#e67e22"
    elif score >= 30: return "MEDIUM", "medium", "#f1c40f"
    else:             return "LOW", "low", "#2ecc71"

def get_recommendation_items(score):
    if score >= 70:
        return [
            ("🔴", "Transship via alternate route — contact freight forwarder immediately"),
            ("📨", "Notify all affected buyers within the next 2 hours"),
            ("📄", "File force majeure notice to protect against penalty clauses"),
            ("✈️", "Prepare emergency air freight contingency for critical cargo"),
        ]
    elif score >= 50:
        return [
            ("📋", "Prepare contingency routing options — do not book yet"),
            ("🔍", "Review alternative vessel schedules on affected corridors"),
            ("📞", "Contact freight forwarder for updated ETA information"),
        ]
    elif score >= 30:
        return [
            ("📊", "Continue monitoring at standard frequency"),
            ("✅", "No immediate action required — situation stable"),
        ]
    else:
        return [
            ("✅", "All corridors operating normally"),
            ("🚢", "Proceed with planned shipments as scheduled"),
        ]

def load_shipments():
    try:
        with open("shipments.json", "r") as f:
            return json.load(f)
    except:
        return [
            {"id": "CNSH772341", "route": "Nhava Sheva → Rotterdam", "cargo": "Pharmaceuticals", "value": "₹22.0L", "deadline": "2026-04-16", "status": "In Transit"},
            {"id": "INMU456789", "route": "Nhava Sheva → Jebel Ali", "cargo": "Garments", "value": "₹8.5L", "deadline": "2026-04-03", "status": "In Transit"},
            {"id": "COCHN887234", "route": "Kochi → Miami", "cargo": "Spices", "value": "₹9.8L", "deadline": "2026-04-09", "status": "At Destination"},
        ]

def save_shipments(shipments):
    with open("shipments.json", "w") as f:
        json.dump(shipments, f, indent=2)

def add_shipment(container_id, origin, destination, cargo_type, value, deadline):
    shipments = load_shipments()
    shipments.append({
        "id": container_id,
        "route": f"{origin} → {destination}",
        "cargo": cargo_type,
        "value": f"₹{value}L",
        "deadline": deadline,
        "status": "Registered",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    save_shipments(shipments)

def get_shipment_risk(s, live_risk):
    if "Rotterdam" in s["route"]:   return min(live_risk + 10, 100)
    elif "Jebel Ali" in s["route"]: return live_risk
    else:                           return max(live_risk - 20, 10)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="VyaparAI", layout="wide", initial_sidebar_state="collapsed")
st.markdown(f"<style>{DESIGN}</style>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
with st.spinner(""):
    live_news = get_live_news()
    live_risk = calculate_risk_score(live_news)
    level, cls, color = get_risk_meta(live_risk)
    rec_items = get_recommendation_items(live_risk)
    forecaster.add_current_risk(live_risk)
    shipments = load_shipments()
    now_str = datetime.now().strftime("%d %b %Y · %H:%M UTC")

# ─────────────────────────────────────────────────────────────────────────────
# TOPBAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="vyapar-topbar">
    <div class="topbar-brand">
        <span class="topbar-logo">VyaparAI</span>
        <span class="topbar-tagline">Supply Chain Intelligence</span>
    </div>
    <div class="topbar-right">
        <span class="topbar-time">{now_str}</span>
        <div class="live-pill">
            <div class="live-dot"></div>
            Live Monitoring
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HERO RISK BANNER
# ─────────────────────────────────────────────────────────────────────────────
high_risk_count = sum(1 for s in shipments if get_shipment_risk(s, live_risk) >= 70)
active_count = len(shipments)
corridors_count = 4

st.markdown(f"""
<div class="hero-banner">
    <div>
        <div class="hero-label">Global Supply Chain Risk Index</div>
        <div class="hero-score hero-score-{cls}">{live_risk}<span style="font-size:28px;font-weight:400;color:var(--mist-dim);">/100</span></div>
        <div class="hero-meta">
            <span class="hero-level-badge badge-{cls}">{level}</span>
            <span class="hero-updated">Updated {datetime.now().strftime('%H:%M')}</span>
        </div>
    </div>
    <div class="hero-stats-grid">
        <div class="hero-stat"><span class="hero-stat-val">{active_count}</span><span class="hero-stat-lbl">Active Shipments</span></div>
        <div class="hero-stat"><span class="hero-stat-val" style="color:{'#e74c3c' if high_risk_count > 0 else 'var(--gold)'} !important;">{high_risk_count}</span><span class="hero-stat-lbl">High Risk</span></div>
        <div class="hero-stat"><span class="hero-stat-val">{corridors_count}</span><span class="hero-stat-lbl">Corridors Monitored</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Fleet Overview", "Register Shipment", "Live Intelligence", "Response Engine", "Risk Trends", "Forecast"
])

# ============================= TAB 1 — FLEET OVERVIEW =============================
with tab1:
    st.markdown('<div class="content-area">', unsafe_allow_html=True)

    # Priority alerts
    priority = [(s, get_shipment_risk(s, live_risk)) for s in shipments if get_shipment_risk(s, live_risk) >= 70]
    priority.sort(key=lambda x: x[1], reverse=True)

    if priority:
        st.markdown(f'<div class="section-header"><span class="section-title">Priority Alerts</span><span class="section-count">{len(priority)} require action</span></div>', unsafe_allow_html=True)
        
        for s, risk in priority[:3]:
            lv, lc, lcolor = get_risk_meta(risk)
            delay_info = calculate_delay_and_eta(risk, s['deadline'])
            
            st.markdown(f"""
            <div class="priority-alert">
                <div class="priority-header">
                    <div>
                        <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:rgba(231,76,60,0.6);letter-spacing:0.15em;text-transform:uppercase;margin-bottom:6px;">Immediate Action Required</div>
                        <div style="font-family:'IBM Plex Mono',monospace;font-size:20px;font-weight:500;color:var(--white);">{s['id']}</div>
                        <div style="font-family:'Lato',sans-serif;font-size:13px;color:var(--mist-dim);margin-top:4px;">{s['route']}</div>
                        <div style="font-family:'Lato',sans-serif;font-size:13px;color:var(--mist-dim);">{s['cargo']} · {s['value']}</div>
                        <div style="font-family:'Lato',sans-serif;font-size:12px;color:#e67e22;margin-top:6px;">📅 Deadline: {delay_info['original_deadline']} → Est: {delay_info['estimated_delivery']} · {delay_info['delay_range']}</div>
                    </div>
                    <div style="text-align:right;padding-right:32px;">
                        <div class="priority-score-display">{risk}</div>
                        <div class="priority-score-sub">Risk Score</div>
                    </div>
                </div>
                <div class="priority-actions-label">Recommended Actions</div>
                <div class="priority-action-item"><div class="action-dot"></div>Transship via alternate route — contact freight forwarder now</div>
                <div class="priority-action-item"><div class="action-dot"></div>Notify buyer within 2 hours — use auto-generated template</div>
                <div class="priority-action-item"><div class="action-dot"></div>File force majeure notice to protect penalty exposure</div>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button(f"Notify Buyer", key=f"nb_{s['id']}"):
                    st.success(f"Buyer notification dispatched for {s['id']}")
            with c2:
                if st.button(f"Find Alternatives", key=f"fa_{s['id']}"):
                    st.info(f"Searching alternative routes for {s['id']}...")
            with c3:
                if st.button(f"Generate Report", key=f"gr_{s['id']}"):
                    st.info(f"Generating full risk report for {s['id']}")

    # All shipments
    st.markdown(f'<div class="section-header" style="margin-top:32px;"><span class="section-title">All Shipments</span><span class="section-count">{len(shipments)} total</span></div>', unsafe_allow_html=True)

    for s in shipments:
        risk = get_shipment_risk(s, live_risk)
        lv, lc, lcolor = get_risk_meta(risk)
        delay_info = calculate_delay_and_eta(risk, s['deadline'])
        
        st.markdown(f"""
        <div class="shipment-card card-{lc}">
            <div class="card-top">
                <div>
                    <div class="card-id">{s['id']}</div>
                    <div class="card-route">{s['route'].replace('→', '<span class="route-arrow">→</span>')}</div>
                </div>
                <div class="card-risk-circle circle-{lc}">
                    <span class="circle-score score-{lc}">{risk}</span>
                    <span class="circle-label label-{lc}">{lv}</span>
                </div>
            </div>
            <div class="card-meta" style="grid-template-columns: repeat(3, 1fr);">
                <div><span class="meta-item-lbl">Cargo</span><span class="meta-item-val">{s['cargo']}</span></div>
                <div><span class="meta-item-lbl">Value</span><span class="meta-item-val-gold">{s['value']}</span></div>
                <div><span class="meta-item-lbl">Deadline</span><span class="meta-item-val">{delay_info['original_deadline']}</span></div>
                <div><span class="meta-item-lbl">Est. Delivery</span><span class="meta-item-val" style="color:#e67e22;">{delay_info['estimated_delivery']}</span></div>
                <div><span class="meta-item-lbl">Delay</span><span class="meta-item-val-delay">{delay_info['delay_range']}</span></div>
                <div><span class="meta-item-lbl">Status</span><span class="meta-item-val">{delay_info['status']}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================= TAB 2 — REGISTER SHIPMENT =============================
with tab2:
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    st.markdown('<div class="form-wrapper"><div class="form-title">Register New Shipment</div><div class="form-subtitle">Add a shipment to begin real-time disruption monitoring</div></div>', unsafe_allow_html=True)
    
    with st.form("register_form"):
        c1, c2 = st.columns(2)
        with c1:
            container_id = st.text_input("Container Number", placeholder="INMU123456")
            origin = st.selectbox("Origin Port", ["Nhava Sheva (INNSA)", "Mundra (INPAV)", "Kochi (INCOK)", "Chennai (INMAA)"])
            cargo_type = st.selectbox("Cargo Type", ["Garments", "Pharmaceuticals", "Spices", "Auto Components", "Electronics"])
        with c2:
            destination = st.selectbox("Destination Port", ["Jebel Ali (AEJEA)", "Rotterdam (NLRTM)", "Singapore (SGSIN)", "Miami (USMIA)", "Hamburg (DEHAM)"])
            value = st.number_input("Cargo Value (₹ Lakhs)", min_value=1.0, max_value=1000.0, value=10.0, step=5.0)
            deadline = st.date_input("Delivery Deadline", min_value=datetime.now().date())
        
        submitted = st.form_submit_button("Register Shipment →", use_container_width=True)
        
        if submitted:
            if not container_id:
                st.error("Container number is required.")
            else:
                origin_code = origin.split("(")[-1].replace(")", "")
                dest_code = destination.split("(")[-1].replace(")", "")
                add_shipment(container_id, origin_code, dest_code, cargo_type, value, deadline.strftime("%Y-%m-%d"))
                st.success(f"Shipment {container_id} registered. Monitoring active.")
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================= TAB 3 — LIVE INTELLIGENCE =============================
with tab3:
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><span class="section-title">Live News Feed</span><span class="section-count">AI-filtered · Updated now</span></div>', unsafe_allow_html=True)
    
    if live_news:
        for article in live_news:
            title = article.get("title", "No title")
            desc = (article.get("description") or "")[:220]
            src = article.get("source", {}).get("name", "NewsAPI")
            st.markdown(f'<div class="news-item"><div class="news-title">{title}</div><div class="news-desc">{desc}{"..." if len(desc) == 220 else ""}</div><div class="news-meta"><span>{src}</span><span>·</span><span>{datetime.now().strftime("%H:%M")}</span></div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-state"><div class="empty-icon">📰</div><div class="empty-title">No news data</div><div class="empty-sub">Add a NEWS_API_KEY to .env to enable live news monitoring</div></div>', unsafe_allow_html=True)
    
    # Signal detection
    crisis_det = any(any(w in (a.get("title","") + a.get("description","")).lower() for w in ["war","attack","crisis","strike"]) for a in live_news)
    disrupt_det = any(any(w in (a.get("title","") + a.get("description","")).lower() for w in ["delay","congestion","disruption"]) for a in live_news)
    price_det = any(any(w in (a.get("title","") + a.get("description","")).lower() for w in ["price","surge","shortage"]) for a in live_news)
    
    signals = [("⚡", "Crisis Events", "Detected" if crisis_det else "None", crisis_det), ("🌊", "Port Disruptions", "Detected" if disrupt_det else "Nominal", disrupt_det), ("📈", "Price Anomalies", "Detected" if price_det else "Stable", price_det), ("🌐", "Geopolitical", "Monitoring", False)]
    
    st.markdown('<div class="signal-grid">', unsafe_allow_html=True)
    for icon, lbl, val, is_alert in signals:
        val_color = "#e74c3c" if is_alert else "#2ecc71"
        st.markdown(f'<div class="signal-card"><span class="signal-icon">{icon}</span><div><span class="signal-info-lbl">{lbl}</span><span class="signal-info-val" style="color:{val_color} !important;">{val}</span></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================= TAB 4 — RESPONSE ENGINE =============================
with tab4:
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><span class="section-title">Response Engine</span><span class="section-count">AI-generated recommendations</span></div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="rec-panel"><div class="rec-title">Current Situation · <span style="color:var(--mist-dim);font-size:13px;font-family:\'IBM Plex Mono\',monospace;">Risk Score {live_risk}/100 · {level}</span></div>', unsafe_allow_html=True)
    for icon, text in rec_items:
        st.markdown(f'<div class="rec-item"><span class="rec-icon">{icon}</span><span>{text}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Corridor monitor
    st.markdown('<div class="section-header" style="margin-top:32px;"><span class="section-title">Corridor Monitor</span></div>', unsafe_allow_html=True)
    corridors = [("Nhava Sheva → Jebel Ali", "India · UAE", live_risk), ("Nhava Sheva → Rotterdam", "India · Netherlands", min(live_risk+10, 100)), ("Kochi → Miami", "India · USA", max(live_risk-15, 10)), ("Chennai → Singapore", "India · Singapore", max(live_risk-20, 10))]
    
    st.markdown('<div class="rec-panel">', unsafe_allow_html=True)
    for name, sub, score in corridors:
        clv, clc, clcolor = get_risk_meta(score)
        st.markdown(f'<div class="corridor-row"><div><div class="corridor-name">{name}</div><div class="corridor-sub">{sub}</div></div><div style="display:flex;align-items:center;gap:14px;"><div style="width:120px;background:rgba(197,207,220,0.06);border-radius:3px;height:4px;"><div style="width:{score}%;height:100%;background:{clcolor};border-radius:3px;"></div></div><span class="corridor-score-badge" style="border-color:{clcolor};color:{clcolor} !important;">{score} · {clv}</span></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================= TAB 5 — RISK TRENDS =============================
with tab5:
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><span class="section-title">Risk Trend Analysis</span><span class="section-count">7-day window</span></div>', unsafe_allow_html=True)
    trend_data = pd.DataFrame({"Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Today"], "Score": [45, 52, 60, 72, 85, 91, live_risk]})
    st.line_chart(trend_data.set_index("Day"), color=["#c9a84c"])
    st.markdown('</div>', unsafe_allow_html=True)

# ============================= TAB 6 — FORECAST =============================
with tab6:
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><span class="section-title">7-Day Risk Forecast</span><span class="section-count">Moving average · Linear regression</span></div>', unsafe_allow_html=True)
    
    try:
        forecasts = forecaster.forecast(7)
        trend = forecaster.get_trend()
        trend_color = {"increasing": "#e74c3c", "decreasing": "#2ecc71"}.get(trend, "#f1c40f")
        trend_msg = {"increasing": "Risk expected to rise — prepare contingency plans", "decreasing": "Situation improving — continue monitoring"}.get(trend, "Risk levels stable — normal operations")
        
        st.markdown(f'<div class="rec-panel" style="margin-bottom:24px;"><div class="rec-title" style="color:{trend_color} !important;">Trend: {trend.upper()}</div><div style="font-family:\'Lato\',sans-serif;font-size:14px;color:var(--mist-dim);">{trend_msg}</div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="rec-panel">', unsafe_allow_html=True)
        for i, score in enumerate(forecasts):
            date_str = (datetime.now() + timedelta(days=i+1)).strftime("%a %d %b")
            score_r = round(score)
            _, _, fc = get_risk_meta(score_r)
            st.markdown(f'<div class="forecast-row"><span class="forecast-date">{date_str}</span><div class="forecast-bar-track"><div class="forecast-bar-fill" style="width:{score_r}%;background:{fc};"></div></div><span class="forecast-score" style="color:{fc} !important;">{score_r}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        forecast_df = pd.DataFrame({"Date": [(datetime.now() + timedelta(days=i+1)).strftime("%d %b") for i in range(7)], "Forecast Risk": [round(f, 0) for f in forecasts]})
        st.line_chart(forecast_df.set_index("Date"), color=["#c9a84c"])
        
    except Exception as e:
        st.markdown('<div class="empty-state"><div class="empty-icon">📈</div><div class="empty-title">Forecast unavailable</div><div class="empty-sub">Collecting historical data — forecast appears after sufficient history</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)