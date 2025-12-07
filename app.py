import streamlit as st
import requests
import time
import plotly.graph_objects as go

# --- AFFILIATE CONFIGURATION ---
# Your REAL NordVPN Link (No discount text, just the link)
LINK_NORDVPN = "https://go.nordvpn.net/aff_c?offer_id=15&aff_id=135688&url_id=902"

st.set_page_config(page_title="Network Privacy Audit", page_icon="🔐", layout="centered")

# --- CUSTOM CSS (Professional/Enterprise Theme) ---
st.markdown("""
<style>
    /* HIDE STREAMLIT UI (Privacy Cloak) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}

    /* MAIN STYLES */
    .main-header { font-size: 2.5rem; text-align: center; font-weight: 700; color: #2c3e50; margin-bottom: 5px; }
    .sub-header { font-size: 1.1rem; text-align: center; color: #7f8c8d; margin-bottom: 30px; }
    
    /* STATUS BOXES */
    .status-box-exposed { 
        padding: 20px; 
        background-color: #fff3cd; 
        color: #856404; 
        border: 1px solid #ffeeba;
        border-radius: 8px; 
        margin: 20px 0;
        text-align: center;
    }
    
    /* CTA BUTTON (System Action Style) */
    .secure-button {
        display: block; width: 100%; padding: 16px; 
        text-align: center; color: white !important; text-decoration: none;
        font-weight: 600; font-size: 1.1rem; border-radius: 6px;
        background-color: #007bff; /* Professional Blue */
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: background-color 0.2s;
    }
    .secure-button:hover { background-color: #0056b3; }
    
    .data-card {
        background: #ffffff; padding: 15px; border-radius: 8px;
        border: 1px solid #e9ecef; text-align: center; margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .data-card h4 { margin: 0; color: #adb5bd; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }
    .data-card p { margin: 5px 0 0 0; font-weight: 600; font-size: 1rem; color: #343a40; }
</style>
""", unsafe_allow_html=True)

# --- LOGIC ---
def get_ip_info():
    try:
        # User-Agent ensures we get a clean JSON response
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get('https://ipapi.co/json/', headers=headers, timeout=5)
        return response.json()
    except:
        return None

# --- UI ---
st.markdown('<div class="main-header">Network Privacy Audit</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Public Visibility Analysis Tool</div>', unsafe_allow_html=True)

with st.spinner("Analyzing network headers..."):
    time.sleep(0.8) # Professional pause
    data = get_ip_info()

if data:
    ip = data.get('ip', 'Unknown')
    city = data.get('city', 'Unknown')
    country = data.get('country_name', 'Unknown')
    org = data.get('org', 'ISP')
    
    # 1. The Map (Clean View)
    lat = data.get('latitude')
    lon = data.get('longitude')
    
    if lat and lon:
        fig = go.Figure(go.Scattermapbox(
            lat=[lat], lon=[lon], mode='markers',
            marker=go.scattermapbox.Marker(size=12, color='#e74c3c'), # Red dot
            text=[f"{city}, {country}"]
        ))
        fig.update_layout(
            mapbox_style="carto-positron", # Cleaner, professional map style
            margin={"r":0,"t":0,"l":0,"b":0},
            height=250,
            mapbox=dict(center=dict(lat=lat, lon=lon), zoom=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    # 2. Data Cards
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="data-card"><h4>IP Address</h4><p>{ip}</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="data-card"><h4>Provider</h4><p>{org}</p></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="data-card"><h4>Location</h4><p>{city}</p></div>', unsafe_allow_html=True)

    # 3. The Diagnosis (Professional Warning)
    st.markdown("""
    <div class="status-box-exposed">
        <h3 style="margin:0; font-size:1.2rem;">⚠️ CONNECTION UNENCRYPTED</h3>
        <p style="margin:5px 0 0 0; font-size:0.95rem;">
        Your digital footprint is currently visible to external networks, advertisers, and potential threat actors.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 4. The Solution (Professional Recommendation)
    st.markdown("### Recommended Action")
    st.markdown(f"""
    <a href="{LINK_NORDVPN}" target="_blank" class="secure-button">
        Enable Secure Tunnel (NordVPN) →
    </a>
    <p style="text-align:center; margin-top:10px; font-size:0.85rem; color:#95a5a6;">
        Standard encryption protocol recommended for professional use.
    </p>
    """, unsafe_allow_html=True)

else:
    st.error("Network analysis failed. Please disable ad-blockers and refresh.")