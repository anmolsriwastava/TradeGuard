import streamlit as st
import json
import requests
from datetime import datetime, timedelta

st.set_page_config(
    page_title="TradeGuard · AI Supply Chain Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Base Theme - Modern Slate Palette */
html,body,[class*="css"],.stApp {font-family:'Space Grotesk',sans-serif!important; background:#0f172a!important; color:#cbd5e1!important;}
section[data-testid="stSidebar"] {background:#0b1120!important; border-right:1px solid #1e293b!important;}
section[data-testid="stSidebar"] .stMarkdown p, section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] span {color:#94a3b8!important;}
h1,h2,h3,h4 {color:#f8fafc!important; font-family:'Space Grotesk',sans-serif!important;}

/* Cards */
.mc, .sc, .dp, .cc {background:#1e293b; border:1px solid #334155; border-radius:12px; position:relative; overflow:hidden;}
.mc {padding:20px 22px;}
.sc, .cc {padding:14px 16px; margin-bottom:8px;}
.dp {padding:20px 22px; margin-bottom:14px;}

/* Soft Top Borders for Metrics */
.mc::before {content:''; position:absolute; top:0; left:0; right:0; height:3px;}
.mc.cr::before {background:#f87171;} /* Soft Red */
.mc.hi::before {background:#fb923c;} /* Soft Orange */
.mc.me::before {background:#fbbf24;} /* Soft Yellow */
.mc.lo::before {background:#4ade80;} /* Soft Green */
.mc.bl::before {background:#60a5fa;} /* Soft Blue */

/* Typography */
.mn {font-size:32px; font-weight:700; font-family:'JetBrains Mono',monospace; line-height:1; margin-bottom:4px;}
.ml {font-size:10px; font-weight:600; letter-spacing:.1em; text-transform:uppercase; color:#94a3b8;}
.sl {font-size:10px; font-weight:700; letter-spacing:.14em; text-transform:uppercase; color:#60a5fa; font-family:'JetBrains Mono',monospace; border-bottom:1px solid #334155; padding-bottom:8px; margin-bottom:14px;}

/* Badges - Semi-transparent instead of solid dark */
.rb {display:inline-block; padding:3px 10px; border-radius:20px; font-size:10px; font-weight:700; font-family:'JetBrains Mono',monospace; letter-spacing:.06em;}
.rb.CRITICAL {background:rgba(248,113,113,0.1); color:#f87171; border:1px solid rgba(248,113,113,0.2);}
.rb.HIGH {background:rgba(251,146,60,0.1); color:#fb923c; border:1px solid rgba(251,146,60,0.2);}
.rb.MEDIUM {background:rgba(251,191,36,0.1); color:#fbbf24; border:1px solid rgba(251,191,36,0.2);}
.rb.LOW {background:rgba(74,222,128,0.1); color:#4ade80; border:1px solid rgba(74,222,128,0.2);}
.rb.stg {background:rgba(96,165,250,0.1); color:#60a5fa; border:1px solid rgba(96,165,250,0.2);}

/* Card Left Borders */
.sc {border-left:4px solid transparent;}
.sc.CRITICAL, .cc.CRITICAL {border-left-color:#f87171!important;}
.sc.HIGH, .cc.HIGH {border-left-color:#fb923c!important;}
.sc.MEDIUM, .cc.MEDIUM {border-left-color:#fbbf24!important;}
.sc.LOW, .cc.LOW {border-left-color:#4ade80!important;}

/* UI Elements */
.sb-bg {background:#334155; border-radius:3px; height:5px;}
.ro {background:#0f172a; border:1px solid #334155; border-radius:8px; padding:14px 16px; margin-bottom:8px;}
.ro.rec {border-color:#3b82f6; background:rgba(59,130,246,0.05);}

/* WhatsApp Simulation - Closer to real WhatsApp Dark Mode */
.wa-t {background:#202c33; border-radius:12px 12px 0 0; padding:10px 14px; display:flex; align-items:center; gap:10px;}
.wa-o {background:#111b21; border-radius:0 12px 12px 12px; padding:16px 18px; font-family:'JetBrains Mono',monospace; font-size:12px; line-height:1.8; color:#e9edef; white-space:pre-wrap;}

/* Buttons & Misc */
.stButton button {background:#1e293b!important; color:#cbd5e1!important; border:1px solid #334155!important; border-radius:6px!important; font-family:'Space Grotesk',sans-serif!important; font-size:12px!important; padding:4px 12px!important; transition: all 0.2s;}
.stButton button:hover {background:#334155!important; color:#f8fafc!important;}
.stTabs [data-baseweb="tab"] {color:#94a3b8!important;}
.stTabs [aria-selected="true"] {color:#60a5fa!important;}
.wx {background:#1e293b; border:1px solid #334155; border-radius:8px; padding:10px 14px; font-size:12px; color:#cbd5e1; margin-top:8px;}
</style>
""", unsafe_allow_html=True)

# ── Data ───────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        with open("data/mock_shipments.json") as f:
            ships = json.load(f)["shipments"]
    except:
        ships = [
            {"shipment_id":"SHP-2026-001234","container_no":"INMU456789","vessel_name":"MSC MAYA","origin_port":"INNSA","origin_name":"Nhava Sheva","destination_port":"AEJEA","destination_name":"Jebel Ali","booking_date":"2026-03-20","etd":"2026-03-25","eta":"2026-04-01","delivery_deadline":"2026-04-03","cargo_value_inr":850000,"penalty_per_day_inr":25000,"lifecycle_stage":"mid_ocean","buyer_contact":"+971-50-1234567","priority":"cost","cargo_type":"Garments","buyer_name":"Al Futtaim Trading LLC"},
            {"shipment_id":"SHP-2026-001891","container_no":"CNSH772341","vessel_name":"EVER GIVEN 2","origin_port":"INNSA","origin_name":"Nhava Sheva","destination_port":"NLRTM","destination_name":"Rotterdam","booking_date":"2026-03-18","etd":"2026-03-22","eta":"2026-04-14","delivery_deadline":"2026-04-16","cargo_value_inr":2200000,"penalty_per_day_inr":60000,"lifecycle_stage":"mid_ocean","buyer_contact":"+31-20-5551234","priority":"speed","cargo_type":"Pharmaceuticals","buyer_name":"Pharma Europa BV"},
            {"shipment_id":"SHP-2026-002103","container_no":"SGSIN334892","vessel_name":"MAERSK ALTAIR","origin_port":"INPAV","origin_name":"Mundra","destination_port":"SGSIN","destination_name":"Singapore","booking_date":"2026-03-24","etd":"2026-03-29","eta":"2026-04-07","delivery_deadline":"2026-04-10","cargo_value_inr":540000,"penalty_per_day_inr":15000,"lifecycle_stage":"booked","buyer_contact":"+65-6224-8899","priority":"green","cargo_type":"Textiles","buyer_name":"Singapore Traders Pte Ltd"},
            {"shipment_id":"SHP-2026-002567","container_no":"MUMB119045","vessel_name":"CMA CGM THALASSA","origin_port":"INNSA","origin_name":"Nhava Sheva","destination_port":"GBFXT","destination_name":"Felixstowe","booking_date":"2026-03-26","etd":"2026-04-02","eta":"2026-04-24","delivery_deadline":"2026-04-28","cargo_value_inr":1750000,"penalty_per_day_inr":45000,"lifecycle_stage":"pre_booking","buyer_contact":"+44-20-71234567","priority":"cost","cargo_type":"Engineering Goods","buyer_name":"Midlands Industrial UK"},
            {"shipment_id":"SHP-2026-003012","container_no":"COCHN887234","vessel_name":"MSC AMBRA","origin_port":"INCOK","origin_name":"Kochi","destination_port":"USMIA","destination_name":"Miami","booking_date":"2026-03-15","etd":"2026-03-19","eta":"2026-04-08","delivery_deadline":"2026-04-09","cargo_value_inr":980000,"penalty_per_day_inr":35000,"lifecycle_stage":"destination","buyer_contact":"+1-305-5559876","priority":"speed","cargo_type":"Spices & Food","buyer_name":"Spice Imports USA Inc"},
            {"shipment_id":"SHP-2026-003341","container_no":"SURTP445621","vessel_name":"HAPAG LLOYD PHOENIX","origin_port":"INPAV","origin_name":"Mundra","destination_port":"DEHAM","destination_name":"Hamburg","booking_date":"2026-03-27","etd":"2026-04-04","eta":"2026-04-26","delivery_deadline":"2026-04-30","cargo_value_inr":3100000,"penalty_per_day_inr":80000,"lifecycle_stage":"pre_booking","buyer_contact":"+49-40-3601234","priority":"cost","cargo_type":"Auto Components","buyer_name":"Deutsche Auto Parts GmbH"},
        ]
    try:
        with open("data/corridor_risks.json") as f:
            corrs = json.load(f)["corridors"]
    except:
        corrs = [
            {"corridor_id":"INNSA-AEJEA","name":"Nhava Sheva → Jebel Ali","risk_score":74,"risk_level":"HIGH","components":{"ais_score":68,"weather_score":45,"freight_score":82,"nlp_score":79},"key_signal":"Freight rates +38% above 30-day mean. Terminal workers strike notice filed at Jebel Ali."},
            {"corridor_id":"INNSA-NLRTM","name":"Nhava Sheva → Rotterdam","risk_score":91,"risk_level":"CRITICAL","components":{"ais_score":88,"weather_score":72,"freight_score":95,"nlp_score":90},"key_signal":"Red Sea rerouting active. Cape of Good Hope transit adding 6,000 nautical miles."},
            {"corridor_id":"INPAV-SGSIN","name":"Mundra → Singapore","risk_score":38,"risk_level":"MEDIUM","components":{"ais_score":40,"weather_score":55,"freight_score":30,"nlp_score":28},"key_signal":"Bay of Bengal weather system developing. Monitor closely."},
            {"corridor_id":"INNSA-GBFXT","name":"Nhava Sheva → Felixstowe","risk_score":22,"risk_level":"LOW","components":{"ais_score":20,"weather_score":18,"freight_score":25,"nlp_score":24},"key_signal":"No active disruptions. Normal seasonal variation."},
            {"corridor_id":"INCOK-USMIA","name":"Kochi → Miami","risk_score":67,"risk_level":"HIGH","components":{"ais_score":70,"weather_score":60,"freight_score":65,"nlp_score":71},"key_signal":"Suez transit congestion. Average waiting time up 3.2 days vs 30-day mean."},
            {"corridor_id":"INPAV-DEHAM","name":"Mundra → Hamburg","risk_score":18,"risk_level":"LOW","components":{"ais_score":15,"weather_score":22,"freight_score":18,"nlp_score":16},"key_signal":"All clear. Corridor operating normally."},
        ]
    return ships, corrs

CMAP = {("INNSA","AEJEA"):"INNSA-AEJEA",("INNSA","NLRTM"):"INNSA-NLRTM",("INPAV","SGSIN"):"INPAV-SGSIN",("INNSA","GBFXT"):"INNSA-GBFXT",("INCOK","USMIA"):"INCOK-USMIA",("INPAV","DEHAM"):"INPAV-DEHAM"}
RC = {"CRITICAL":"#f87171","HIGH":"#fb923c","MEDIUM":"#fbbf24","LOW":"#4ade80"}
SL = {"pre_booking":"Pre-booking","booked":"Booked","mid_ocean":"Mid-ocean","destination":"At destination"}

def get_corr(s, lut):
    cid = CMAP.get((s["origin_port"],s["destination_port"]))
    return lut.get(cid,{"risk_score":20,"risk_level":"LOW","key_signal":"No data","components":{"ais_score":20,"weather_score":20,"freight_score":20,"nlp_score":20}})

def delay_str(sc):
    if sc>=85: return "7–12 days"
    if sc>=65: return "4–7 days"
    if sc>=30: return "1–3 days"
    return "< 1 day"

def exposure(s, sc):
    prob = min(0.95, sc/100*1.2)
    rl = "CRITICAL" if sc>=85 else "HIGH" if sc>=65 else "MEDIUM" if sc>=30 else "LOW"
    mid = {"CRITICAL":9,"HIGH":5,"MEDIUM":2,"LOW":0.3}[rl]
    return prob * s["penalty_per_day_inr"] * mid

def resp_opts(s, c):
    stage = s["lifecycle_stage"]
    if stage=="pre_booking":
        return [
            {"title":"Rebook on alternate vessel","desc":"Next vessel avoids disrupted corridor entirely. No penalty window applies.","cost":0,"days":"+3","co2":"Neutral","rec":True},
            {"title":"Tranship via Colombo hub","desc":"Faster route via DP World Colombo transhipment hub.","cost":18000,"days":"+1","co2":"+2%","rec":False},
            {"title":"Switch to Mundra port","desc":"Alternate origin port with lower corridor risk score (18/100).","cost":8000,"days":"+2","co2":"−5%","rec":False},
        ]
    elif stage=="booked":
        return [
            {"title":"Rebook on next vessel","desc":"Cancel within free-cancel window. Switch to safer alternate route.","cost":12000,"days":"+2","co2":"Neutral","rec":True},
            {"title":"Keep + send force majeure notice","desc":"Auto-draft notice to buyer. Protects against penalty clause trigger.","cost":0,"days":"0","co2":"0","rec":False},
            {"title":"Upgrade to expedited clearance","desc":"Pre-book priority clearance at destination port.","cost":9000,"days":"−1","co2":"+1%","rec":False},
        ]
    elif stage=="mid_ocean":
        return [
            {"title":"Tranship at Colombo layover","desc":"Transfer cargo to faster onward vessel before disruption leg.","cost":22000,"days":"+1","co2":"+3%","rec":True},
            {"title":"Auto-send buyer delay notice","desc":"Force majeure notice with revised ETA + AIS evidence package.","cost":0,"days":"0","co2":"0","rec":False},
            {"title":"Request formal deadline extension","desc":"Auto-generated extension request with port authority evidence.","cost":0,"days":"+5","co2":"0","rec":False},
        ]
    else:
        return [
            {"title":"File pre-clearance documents now","desc":"Submit customs paperwork immediately to cut port dwell time.","cost":0,"days":"−1","co2":"0","rec":True},
            {"title":"Book priority berth slot","desc":"Reserve priority unloading — limited availability at destination.","cost":15000,"days":"−2","co2":"0","rec":False},
            {"title":"Alternate inland transport","desc":"Redirect cargo via road from alternate terminal if berth blocked.","cost":8000,"days":"−1","co2":"+8%","rec":False},
        ]

def wa_msg(s, c):
    rl,sc = c["risk_level"],c["risk_score"]
    exp = exposure(s,sc)
    em = {"CRITICAL":"🚨","HIGH":"⚠️","MEDIUM":"📊","LOW":"ℹ️"}.get(rl,"ℹ️")
    sig = c.get("key_signal","")[:100]
    return f"""{em} *TradeGuard Alert — {rl} RISK*

📦 Container: {s['container_no']}
🚢 Vessel: {s['vessel_name']}
🛤️  Route: {s['origin_name']} → {s['destination_name']}

📊 Risk Score: {sc}/100
⏱️  Predicted delay: {delay_str(sc)}
💸 Penalty exposure: ₹{exp:,.0f}
📅 Your deadline: {s['delivery_deadline']}

🔍 {sig}

👆 3 response options ready. Reply *OPTIONS* to view.

_Powered by TradeGuard AI · DP World Network_"""

def get_weather(city):
    try:
        key = st.secrets.get("OPENWEATHER_API_KEY","")
        if not key: return None
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric",timeout=5)
        if r.status_code==200:
            d=r.json()
            return {"temp":round(d["main"]["temp"]),"desc":d["weather"][0]["description"].title(),
                    "wind":round(d["wind"]["speed"]),"hum":d["main"]["humidity"],"icon":d["weather"][0]["main"]}
    except: pass
    return None

# ── Load ───────────────────────────────────────────────────────────────────────
ships, corrs = load_data()
clut = {c["corridor_id"]:c for c in corrs}
enriched = sorted([{**s,"corridor":get_corr(s,clut),"exp":exposure(s,get_corr(s,clut)["risk_score"])} for s in ships],
                  key=lambda x:x["corridor"]["risk_score"],reverse=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛡️ TradeGuard")
    st.markdown("<small style='color:#1d4ed8;font-weight:600;letter-spacing:0.05em;'>AI SUPPLY CHAIN INTELLIGENCE</small>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Risk Filter**")
    rf = st.multiselect("Risk",["CRITICAL","HIGH","MEDIUM","LOW"],default=["CRITICAL","HIGH","MEDIUM","LOW"],label_visibility="collapsed")
    st.markdown("**Lifecycle Stage**")
    sf = st.multiselect("Stage",["pre_booking","booked","mid_ocean","destination"],
                        default=["pre_booking","booked","mid_ocean","destination"],
                        format_func=lambda x:SL[x],label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Live port weather**")
    wcity = st.selectbox("Port",["Mumbai","Jebel Ali","Rotterdam","Singapore","Hamburg"],label_visibility="collapsed")
    wx = get_weather(wcity)
    icons = {"Clear":"☀️","Clouds":"☁️","Rain":"🌧️","Thunderstorm":"⛈️","Drizzle":"🌦️","Mist":"🌫️","Haze":"🌫️"}
    if wx:
        st.markdown(f"""<div class="wx">{icons.get(wx['icon'],'🌡️')} <b style="color:#e2edf8">{wx['temp']}°C</b> · {wx['desc']}<br>
💨 {wx['wind']} m/s &nbsp;💧 {wx['hum']}% humidity</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="wx">🔑 Add <code>OPENWEATHER_API_KEY</code> to<br><code>.streamlit/secrets.toml</code><br>to enable live weather data.</div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"<small style='color:#4a6a8a'>🔄 Scan: <code>{datetime.now().strftime('%Y-%m-%d %H:%M')}</code><br>⏱ Next: every 6 hours<br>🌐 73 countries · 6 corridors</small>", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
h1,h2 = st.columns([7,2])
with h1:
    st.markdown("# 🛡️ TradeGuard")
    st.markdown("<small style='color:#4a6a8a'>AI-Powered Supply Chain Disruption Intelligence · DP World Hackathon 2026 · BITS Pilani Hyderabad</small>", unsafe_allow_html=True)
with h2:
    st.markdown(f"<div style='text-align:right;padding-top:20px;font-family:JetBrains Mono,monospace;font-size:11px;color:#4a6a8a;'>{datetime.now().strftime('%d %b %Y %H:%M IST')}<br><span style='color:#22c55e;'>● System Online</span></div>", unsafe_allow_html=True)
st.markdown("---")

# ── Metrics ────────────────────────────────────────────────────────────────────
filt = [e for e in enriched if e["corridor"]["risk_level"] in rf and e["lifecycle_stage"] in sf]
crit_n = sum(1 for e in enriched if e["corridor"]["risk_level"]=="CRITICAL")
high_n = sum(1 for e in enriched if e["corridor"]["risk_level"]=="HIGH")
tot_exp = sum(e["exp"] for e in enriched)
avg_sc = sum(e["corridor"]["risk_score"] for e in enriched)/len(enriched) if enriched else 0

cols = st.columns(5)
for col,(v,l,c,cls) in zip(cols,[
    (str(crit_n),"CRITICAL ALERTS","#ef4444","cr"),
    (str(high_n),"HIGH RISK","#f97316","hi"),
    (f"₹{tot_exp/100000:.1f}L","TOTAL EXPOSURE","#e2edf8","bl"),
    (f"{avg_sc:.0f}","AVG CORRIDOR RISK","#eab308","me"),
    (str(len(ships)),"ACTIVE SHIPMENTS","#22c55e","lo"),
]):
    with col:
        st.markdown(f'<div class="mc {cls}"><div class="mn" style="color:{c}">{v}</div><div class="ml">{l}</div></div>',unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Two-column layout ──────────────────────────────────────────────────────────
L,R = st.columns([5,6],gap="large")

with L:
    st.markdown('<div class="sl">▸ Active Shipments</div>',unsafe_allow_html=True)
    if "sel" not in st.session_state:
        st.session_state.sel = filt[0]["shipment_id"] if filt else None
    for e in filt:
        c = e["corridor"]; rl = c["risk_level"]
        bg = "background:#0d1c35;" if e["shipment_id"]==st.session_state.sel else ""
        st.markdown(f"""<div class="sc {rl}" style="{bg}">
<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
  <span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#60a5fa;font-weight:500;">{e['container_no']}</span>
  <div><span class="rb {rl}">{rl}</span>&nbsp;<span style="font-family:'JetBrains Mono',monospace;font-size:20px;font-weight:700;color:{RC[rl]};">{c['risk_score']}</span></div>
</div>
<div style="font-size:13px;font-weight:600;color:#e2edf8;margin-bottom:3px;">{e['origin_name']} → {e['destination_name']}</div>
<div style="font-size:11px;color:#4a6a8a;margin-bottom:8px;">{e['vessel_name']} · {e['cargo_type']} · <span class="rb stg">{SL[e['lifecycle_stage']]}</span></div>
<div style="display:flex;gap:18px;font-size:11px;color:#7a9ab8;">
  <span>⏱ <b style="color:#e2edf8">{delay_str(c['risk_score'])}</b></span>
  <span>💸 <b style="color:#f97316">₹{e['exp']:,.0f}</b></span>
  <span>📅 <b style="color:#e2edf8">{e['delivery_deadline']}</b></span>
</div></div>""", unsafe_allow_html=True)
        if st.button("View details →", key=f"b_{e['shipment_id']}"):
            st.session_state.sel = e["shipment_id"]; st.rerun()

with R:
    st.markdown('<div class="sl">▸ Shipment Intelligence</div>',unsafe_allow_html=True)
    sel = next((e for e in enriched if e["shipment_id"]==st.session_state.sel), enriched[0] if enriched else None)
    if sel:
        c = sel["corridor"]; rl = c["risk_level"]; sc = c["risk_score"]

        # Overview card
        st.markdown(f"""<div class="dp">
<div style="display:flex;justify-content:space-between;align-items:flex-start;">
  <div>
    <div style="font-size:15px;font-weight:700;color:#e2edf8;margin-bottom:4px;">{sel['origin_name']} → {sel['destination_name']}</div>
    <div style="font-size:11px;color:#4a6a8a;">{sel['vessel_name']} · {sel['cargo_type']} · {sel['buyer_name']}</div>
  </div>
  <div style="text-align:right;">
    <span class="rb {rl}">{rl} RISK</span><br>
    <span style="font-family:'JetBrains Mono',monospace;font-size:30px;font-weight:700;color:{RC[rl]};">{sc}</span>
    <span style="font-size:12px;color:#4a6a8a;">/100</span>
  </div>
</div>
<div style="margin-top:10px;padding-top:10px;border-top:1px solid #0f2040;display:flex;gap:20px;flex-wrap:wrap;font-size:11px;color:#7a9ab8;">
  <span>📦 <code style="color:#60a5fa;">{sel['container_no']}</code></span>
  <span>📅 Deadline: <b style="color:#e2edf8;">{sel['delivery_deadline']}</b></span>
  <span>⚙️ Priority: <b style="color:#e2edf8;">{sel['priority'].title()}</b></span>
  <span>💰 Cargo: <b style="color:#e2edf8;">₹{sel['cargo_value_inr']/100000:.1f}L</b></span>
</div></div>""", unsafe_allow_html=True)

        # Score breakdown
        st.markdown('<div style="font-size:10px;font-weight:700;color:#4a6a8a;letter-spacing:.1em;text-transform:uppercase;margin-bottom:10px;">Risk Signal Breakdown (composite score)</div>', unsafe_allow_html=True)
        comp = c["components"]
        for lbl,val,w in [("AIS / Vessel positioning",comp["ais_score"],"w=35%"),("NLP news signal",comp["nlp_score"],"w=25%"),("Freight rate anomaly",comp["freight_score"],"w=20%"),("Weather systems",comp["weather_score"],"w=20%")]:
            bc = "#ef4444" if val>=75 else "#f97316" if val>=50 else "#eab308" if val>=30 else "#22c55e"
            st.markdown(f"""<div style="margin-bottom:10px;">
<div style="display:flex;justify-content:space-between;font-size:11px;color:#4a6a8a;margin-bottom:4px;">
  <span>{lbl} <span style="color:#1d4ed8;">({w})</span></span><b style="color:{bc};">{val}</b>
</div>
<div class="sb-bg"><div style="height:5px;width:{val}%;background:{bc};border-radius:3px;"></div></div>
</div>""", unsafe_allow_html=True)

        sig = c.get("key_signal","")
        st.markdown(f'<div style="background:#060b14;border:1px solid #0f2040;border-radius:6px;padding:10px 14px;font-size:12px;color:#7a9ab8;margin:10px 0;">🔍 <b style="color:#e2edf8;">Key signal:</b> {sig}</div>',unsafe_allow_html=True)

        # Tabs
        t1,t2,t3 = st.tabs(["📋  Response Options","📱  WhatsApp Alert","📊  Financial Impact"])

        with t1:
            st.markdown(f"<small style='color:#4a6a8a'>Stage: <b style='color:#60a5fa'>{SL[sel['lifecycle_stage']]}</b> · Priority: <b style='color:#60a5fa'>{sel['priority'].title()}</b> · Ranked by convex optimisation</small>",unsafe_allow_html=True)
            st.markdown("<br>",unsafe_allow_html=True)
            for i,opt in enumerate(resp_opts(sel,c)):
                rec_style = "border-color:#1d4ed8;background:#080f20;" if opt["rec"] else ""
                rbadge = "<span style='background:#0f2040;color:#60a5fa;border:1px solid #1d4ed8;border-radius:20px;font-size:9px;font-weight:700;padding:2px 8px;'>⭐ RECOMMENDED</span>&nbsp;" if opt["rec"] else f"<span style='background:#0a1525;color:#4a6a8a;border:1px solid #0f2040;border-radius:20px;font-size:9px;padding:2px 8px;'>Option {i+1}</span>&nbsp;"
                cc = f"₹{opt['cost']:,}" if opt["cost"]>0 else "Free"
                ccol = "#f97316" if opt["cost"]>0 else "#22c55e"
                st.markdown(f"""<div class="ro{'  rec' if opt['rec'] else ''}">
<div style="margin-bottom:6px;">{rbadge}<b style="font-size:13px;color:#e2edf8;">{opt['title']}</b></div>
<div style="font-size:12px;color:#7a9ab8;margin-bottom:10px;">{opt['desc']}</div>
<div style="display:flex;gap:20px;font-size:11px;border-top:1px solid #0f2040;padding-top:8px;">
  <span>💰 <b style="color:{ccol};">{cc}</b></span>
  <span>⏱ <b style="color:#e2edf8;">{opt['days']} days</b></span>
  <span>🌱 CO₂: <b style="color:#22c55e;">{opt['co2']}</b></span>
</div></div>""",unsafe_allow_html=True)

        with t2:
            st.markdown("<small style='color:#4a6a8a'>Auto-generated and dispatched when risk threshold is crossed</small>",unsafe_allow_html=True)
            st.markdown("<br>",unsafe_allow_html=True)
            msg = wa_msg(sel,c)
            st.markdown(f"""<div class="wa-t">
  <div style="width:34px;height:34px;background:#1a5c1a;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:17px;">🛡️</div>
  <div><div style="font-size:13px;font-weight:600;color:#e2edf8;">TradeGuard</div><div style="font-size:10px;color:#4a6a8a;">Business Account ✓ · WhatsApp</div></div>
  <div style="margin-left:auto;font-size:10px;color:#4a6a8a;">{datetime.now().strftime('%H:%M')}</div>
</div><div class="wa-o">{msg}</div>
<div style="margin-top:8px;font-size:11px;color:#4a6a8a;">📲 Sending to: <code style="color:#60a5fa;">{sel['buyer_contact']}</code> · {sel['buyer_name']}</div>""",unsafe_allow_html=True)

        with t3:
            exp_val = sel["exp"]; dp = sel["penalty_per_day_inr"]; cv = sel["cargo_value_inr"]
            prob = min(0.95,sc/100*1.2)
            mid = {"CRITICAL":9,"HIGH":5,"MEDIUM":2,"LOW":0.3}.get(rl,1)
            st.markdown(f"""<div class="dp">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px;">
  <div style="background:#060b14;border:1px solid #0f2040;border-radius:8px;padding:14px;">
    <div style="font-size:24px;font-weight:700;font-family:'JetBrains Mono',monospace;color:#ef4444;">₹{exp_val:,.0f}</div>
    <div style="font-size:10px;color:#4a6a8a;text-transform:uppercase;letter-spacing:.08em;">Total penalty exposure</div>
  </div>
  <div style="background:#060b14;border:1px solid #0f2040;border-radius:8px;padding:14px;">
    <div style="font-size:24px;font-weight:700;font-family:'JetBrains Mono',monospace;color:#f97316;">{prob*100:.0f}%</div>
    <div style="font-size:10px;color:#4a6a8a;text-transform:uppercase;letter-spacing:.08em;">Delay probability</div>
  </div>
  <div style="background:#060b14;border:1px solid #0f2040;border-radius:8px;padding:14px;">
    <div style="font-size:24px;font-weight:700;font-family:'JetBrains Mono',monospace;color:#eab308;">₹{dp:,}</div>
    <div style="font-size:10px;color:#4a6a8a;text-transform:uppercase;letter-spacing:.08em;">Penalty per day</div>
  </div>
  <div style="background:#060b14;border:1px solid #0f2040;border-radius:8px;padding:14px;">
    <div style="font-size:24px;font-weight:700;font-family:'JetBrains Mono',monospace;color:#e2edf8;">₹{cv/100000:.1f}L</div>
    <div style="font-size:10px;color:#4a6a8a;text-transform:uppercase;letter-spacing:.08em;">Cargo value</div>
  </div>
</div>
<div style="background:#060b14;border:1px solid #0f2040;border-radius:8px;padding:12px 14px;font-size:12px;color:#7a9ab8;">
  📐 <b style="color:#e2edf8;">ImpactAssessor formula:</b><br>
  E = P(delay) × (penalty/day × E[Δt])<br>
  &nbsp;&nbsp;= {prob:.2f} × (₹{dp:,} × {mid} days) = <b style="color:#f97316;">₹{exp_val:,.0f}</b>
</div></div>""",unsafe_allow_html=True)

# ── Corridor overview ──────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="sl">▸ Corridor Risk Index</div>',unsafe_allow_html=True)
c1,c2,c3 = st.columns(3)
for i,corr in enumerate(corrs):
    lvl=corr["risk_level"]; sc=corr["risk_score"]; comp=corr["components"]; bar=RC[lvl]
    with [c1,c2,c3][i%3]:
        st.markdown(f"""<div class="cc {lvl}">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
  <span style="font-size:12px;font-weight:600;color:#c9d8ea;">{corr['name']}</span>
  <span class="rb {lvl}">{lvl}</span>
</div>
<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
  <div style="flex:1;background:#0f2040;border-radius:3px;height:6px;">
    <div style="height:6px;width:{sc}%;background:{bar};border-radius:3px;"></div>
  </div>
  <span style="font-family:'JetBrains Mono',monospace;font-size:18px;font-weight:700;color:{bar};min-width:28px;">{sc}</span>
</div>
<div style="display:flex;gap:10px;font-size:10px;color:#4a6a8a;margin-bottom:6px;">
  <span>AIS:{comp['ais_score']}</span><span>WX:{comp['weather_score']}</span>
  <span>FRT:{comp['freight_score']}</span><span>NLP:{comp['nlp_score']}</span>
</div>
<div style="font-size:10px;color:#4a6a8a;border-top:1px solid #0f2040;padding-top:6px;">{corr['key_signal'][:88]}{'…' if len(corr['key_signal'])>88 else ''}</div>
</div>""",unsafe_allow_html=True)

st.markdown("<br>")
st.markdown('<div style="text-align:center;font-family:JetBrains Mono,monospace;font-size:10px;color:#0f2040;letter-spacing:.1em;">TRADEGUARD · DP WORLD HACKATHON 2026 · BITS PILANI HYDERABAD · DETECT → QUANTIFY → RESPOND</div>',unsafe_allow_html=True)