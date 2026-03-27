import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="TradeGuard | Supply Chain Intelligence",
    page_icon="🚢",
    layout="wide"
)

# Simple, professional CSS
st.markdown("""
<style>
    /* Clean, professional styling */
    .main-header {
        border-bottom: 2px solid #e6e9f0;
        padding-bottom: 1rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background-color: #ffffff;
        border: 1px solid #e6e9f0;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 600;
        color: #1a2c3e;
        margin-bottom: 0.25rem;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: #6c7a89;
        letter-spacing: 0.3px;
    }
    
    .alert-item {
        background-color: #fff5f0;
        border-left: 4px solid #f97316;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .alert-high {
        border-left-color: #dc2626;
        background-color: #fef2f2;
    }
    
    .alert-medium {
        border-left-color: #f59e0b;
        background-color: #fffbeb;
    }
    
    .risk-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    .risk-high {
        background-color: #fee2e2;
        color: #dc2626;
    }
    
    .risk-medium {
        background-color: #fed7aa;
        color: #c2410c;
    }
    
    .risk-low {
        background-color: #d1fae5;
        color: #059669;
    }
    
    .footer {
        border-top: 1px solid #e6e9f0;
        margin-top: 3rem;
        padding-top: 1.5rem;
        text-align: center;
        color: #6c7a89;
        font-size: 0.8rem;
    }
    
    hr {
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

API_URL = "http://localhost:8000"

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.title("🚢 TradeGuard")
with col2:
    st.markdown("### AI-Powered Supply Chain Intelligence")
with col3:
    # Check backend status
    try:
        requests.get(f"{API_URL}/health", timeout=2)
        st.markdown("<p style='text-align: right; color: #10b981;'>● System Online</p>", unsafe_allow_html=True)
    except:
        st.markdown("<p style='text-align: right; color: #ef4444;'>● Connection Error</p>", unsafe_allow_html=True)

st.markdown("<div class='main-header'></div>", unsafe_allow_html=True)

# Fetch data
try:
    alerts_response = requests.get(f"{API_URL}/api/alerts", timeout=5)
    shipments_response = requests.get(f"{API_URL}/api/shipments", timeout=5)
    
    if alerts_response.status_code == 200:
        alerts = alerts_response.json()
        shipments = shipments_response.json()
    else:
        alerts = []
        shipments = []
except:
    alerts = []
    shipments = []

# Statistics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{len(shipments)}</div>
        <div class="stat-label">ACTIVE SHIPMENTS</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    high_risk = len([a for a in alerts if a.get('risk_level') == 'HIGH'])
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number" style="color: #dc2626;">{high_risk}</div>
        <div class="stat-label">HIGH RISK ALERTS</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">73</div>
        <div class="stat-label">CORRIDORS MONITORED</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">52K</div>
        <div class="stat-label">CO₂ SAVED (TONS/YR)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Main Content - Two Columns
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("⚠️ Active Disruption Alerts")
    
    if alerts:
        for alert in alerts:
            risk_class = "alert-high" if alert['risk_level'] == 'HIGH' else "alert-medium"
            badge_class = "risk-high" if alert['risk_level'] == 'HIGH' else "risk-medium"
            
            st.markdown(f"""
            <div class="alert-item {risk_class}">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <strong style="font-size: 1rem;">Container: {alert['container_no']}</strong>
                        <span class="risk-badge {badge_class}" style="margin-left: 0.75rem;">{alert['risk_level']} RISK</span>
                        <div style="margin-top: 0.5rem;">
                            <span style="color: #4b5563;">Shipment: {alert['shipment_id']}</span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #dc2626; font-weight: 600;">{alert['penalty_exposure']}</div>
                        <div style="color: #6b7280; font-size: 0.8rem;">Penalty Exposure</div>
                    </div>
                </div>
                <div style="margin-top: 0.75rem; padding-top: 0.5rem; border-top: 1px solid #ffe4e2;">
                    <span>📅 Predicted Delay: {alert['predicted_delay']}</span>
                    <span style="margin-left: 1.5rem;">📍 Route: Nhava Sheva → Jebel Ali</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Response options as expander
            with st.expander("📋 View Response Options"):
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.markdown("**Alternative Route**")
                    st.caption("Switch to alternate vessel")
                    st.markdown("💰 +₹15,000 | 📅 +2 days")
                with col_b:
                    st.markdown("**Buyer Notification**")
                    st.caption("Auto-generate force majeure notice")
                    st.markdown("💰 Free | ⚡ Immediate")
                with col_c:
                    st.markdown("**Expedited Clearance**")
                    st.caption("Priority handling at destination")
                    st.markdown("💰 +₹12,000 | 📅 -1 day")
    else:
        st.info("✅ No active alerts. All shipments are on track.")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.subheader("📦 Recent Shipments")
    
    if shipments:
        shipment_data = []
        for s in shipments[:5]:
            shipment_data.append({
                "Container": s['container_no'],
                "Vessel": s['vessel_name'],
                "Route": f"{s['origin_port']} → {s['destination_port']}",
                "ETA": s['eta'],
                "Status": "In Transit"
            })
        
        df = pd.DataFrame(shipment_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No shipments registered")

with right_col:
    st.subheader("🌍 Corridor Risk Index")
    
    # Risk meter
    risk_score = 74
    st.markdown(f"""
    <div style="background: #f3f4f6; border-radius: 12px; padding: 1rem;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span>Nhava Sheva → Jebel Ali</span>
            <strong>{risk_score}/100</strong>
        </div>
        <div style="background: #e5e7eb; border-radius: 8px; height: 8px; overflow: hidden;">
            <div style="width: {risk_score}%; background: #f97316; height: 100%;"></div>
        </div>
        <div style="margin-top: 1rem;">
            <span class="risk-badge risk-high">HIGH RISK CORRIDOR</span>
        </div>
        <div style="margin-top: 0.75rem; font-size: 0.8rem; color: #6b7280;">
            ⚠️ Congestion + Weather alerts active
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("📊 Risk Breakdown")
    
    st.markdown("""
    <div style="background: #f9fafb; border-radius: 12px; padding: 1rem;">
        <div style="margin-bottom: 0.75rem;">
            <div style="display: flex; justify-content: space-between;">
                <span>Port Congestion</span>
                <span>82%</span>
            </div>
            <div style="background: #e5e7eb; border-radius: 4px; height: 4px; margin-top: 0.25rem;">
                <div style="width: 82%; background: #ef4444; height: 4px; border-radius: 4px;"></div>
            </div>
        </div>
        <div style="margin-bottom: 0.75rem;">
            <div style="display: flex; justify-content: space-between;">
                <span>Weather Conditions</span>
                <span>65%</span>
            </div>
            <div style="background: #e5e7eb; border-radius: 4px; height: 4px; margin-top: 0.25rem;">
                <div style="width: 65%; background: #f59e0b; height: 4px; border-radius: 4px;"></div>
            </div>
        </div>
        <div>
            <div style="display: flex; justify-content: space-between;">
                <span>Freight Rate Volatility</span>
                <span>71%</span>
            </div>
            <div style="background: #e5e7eb; border-radius: 4px; height: 4px; margin-top: 0.25rem;">
                <div style="width: 71%; background: #f97316; height: 4px; border-radius: 4px;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("💰 Financial Impact")
    
    total_exposure = sum([float(a['penalty_exposure'].replace('₹', '').replace(',', '')) for a in alerts]) if alerts else 0
    st.markdown(f"""
    <div style="background: #fef2f2; border-radius: 12px; padding: 1rem; border: 1px solid #fee2e2;">
        <div style="font-size: 0.85rem; color: #6b7280;">Total At Risk</div>
        <div style="font-size: 2rem; font-weight: 700; color: #dc2626;">₹{total_exposure:,.0f}</div>
        <div style="font-size: 0.8rem; color: #6b7280; margin-top: 0.5rem;">Potential penalty exposure</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    if st.button("📞 Contact Buyer Support", use_container_width=True):
        st.info("Buyer notification ready. Review and send.")
    if st.button("🔄 View Alternative Routes", use_container_width=True):
        st.info("3 alternative routes available for affected shipments.")
    if st.button("📊 Download Risk Report", use_container_width=True):
        st.success("Report generated. Check downloads folder.")

# Footer
st.markdown("""
<div class="footer">
    <p>TradeGuard — Real-time supply chain intelligence for SME exporters</p>
    <p>Powered by DP World Network | 73 countries monitored | 24/7 AI surveillance</p>
</div>
""", unsafe_allow_html=True)