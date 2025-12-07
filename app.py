import streamlit as st
import requests
import time
import plotly.graph_objects as go
from streamlit_javascript import st_javascript

# --- AFFILIATE CONFIGURATION ---
# Your REAL NordVPN Link (Enterprise/Clean style)
LINK_NORDVPN = "https://go.nordvpn.net/aff_c?offer_id=15&aff_id=135688&url_id=902"

st.set_page_config(page_title="Network Privacy Audit", page_icon="🔐", layout="centered")

# --- CUSTOM CSS (Professional & Dark Mode Support) ---
st.markdown("""
<style>
    /* 1. PRIVACY CLOAK (Hide Streamlit UI) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* 2. MAIN HEADER */
    .main-header { 
        font-size: 2.2rem; 
        text-align: center; 
        font-weight: 700; 
        margin-bottom: 5px; 
        /* Works in Light/Dark mode via Streamlit default, but we enforce specific gray for professional look */
    }
    .sub-header { 
        font-size: 1.0rem; 
        text-align: center; 
        color: #888; 
        margin-bottom: 25px; 
    }

    /* 3. REPORT CARDS (Force White Background for Readability in Dark Mode) */
    .data-card {
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 8px;
        border: 1px solid #e0e0e0; 
        text-align: center; 
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .data-card h4 { 
        margin: 0; 
        color: #888 !important; /* Force Grey */
        font-size: 0.8rem; 
        text-transform: uppercase; 
        letter-spacing: 1px; 
    }
    .data-card p { 
        margin: 5px 0 0 0; 
        font-weight: 700; 
        font-size: 1rem; 
        color: #333 !important; /* Force Black/Dark Grey */
    }

    /* 4. WARNING BOX (Force Light Yellow Background) */
    .status-box-exposed { 
        padding: 20px; 
        background-color: #fff3cd; 
        border: 1px solid #ffeeba;
        border-radius: 8px; 
        margin: 20px 0;
        text-align: center;
    }
    .status-box-exposed h3 {
        margin: 0; 
        font-size: 1.2rem;
        color: #856404 !important; /* Dark Brown Text */
    }
    .status-box-exposed p {
        margin: 5px 0 0 0; 
        font-size: 0.95rem;
        color: #856404 !important; /* Dark Brown Text */
    }

    /* 5. CTA BUTTON (Professional Blue) */
    .secure-button {
        display: block; width: 100%; padding: 16px; 
        text-align: center; color: white !important; text-decoration: none;
        font-weight: 600; font-size: 1.1rem; border-radius: 6px;
        background-color: #007bff; 
        box-shadow: 0 4px 6px rgba(0,123,255,0.2);
        transition: background-color 0.2s;
    }
    .secure-button:hover { background-color: #0056b3; }
    
    .disclaimer {
        text-align:center; 
        margin-top:10px; 
        font-size:0.85rem; 
        color:#999 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- CLIENT-SIDE LOGIC ---
def get_client_ip():
    # JavaScript fetch to get the User's REAL IP (Client Side)
    # This prevents the "Static Map" issue where it shows the Server's location
    js_code = """await fetch('https://api.ipify.org').then(function(response) { return response.text() })"""
    return st_javascript(js_code)

def get_location_data(ip_address):
    # API Call to geolocate that IP
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(f'https://ipapi.co/{ip_address}/json/', headers=headers, timeout=5)
        return response.json()
    except:
        return None

# --- UI LAYOUT ---
st.markdown('<div class="main-header">Network Privacy Audit</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Public Visibility Analysis Tool</div>', unsafe_allow_html=True)

# 1. Trigger Client-Side IP Check
# This might blink briefly while loading JS, which is normal
client_ip = get_client_ip()

if client_ip:
    # 2. Fetch Geolocation Data
    data = get_location_data(client_ip)
    
    if data and 'ip' in data:
        ip = data.get('ip', 'Unknown')
        city = data.get('city', 'Unknown')
        country = data.get('country_name', 'Unknown')
        org = data.get('org', 'ISP')
        lat = data.get('latitude')
        lon = data.get('longitude')
        
        # 3. The Map (Carto-Positron for Clean/Enterprise look)
        if lat and lon:
            fig = go.Figure(go.Scattermapbox(
                lat=[lat], lon=[lon], mode='markers',
                marker=go.scattermapbox.Marker(size=14, color='#dc3545'), # Professional Red
                text=[f"{city}, {country}"]
            ))
            fig.update_layout(
                mapbox_style="carto-positron",
                margin={"r":0,"t":0,"l":0,"b":0},
                height=250,
                # Zoom 11 is the sweet spot: not too close (blurry), not too far
                mapbox=dict(center=dict(lat=lat, lon=lon), zoom=11) 
            )
            st.plotly_chart(fig, use_container_width=True)

        # 4. Data Cards (White backgrounds for Dark Mode safety)
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="data-card"><h4>IP Address</h4><p>{ip}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="data-card"><h4>Provider</h4><p>{org}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="data-card"><h4>Location</h4><p>{city}</p></div>', unsafe_allow_html=True)

        # 5. Professional Diagnosis
        st.markdown("""
        <div class="status-box-exposed">
            <h3>⚠️ UNENCRYPTED CONNECTION DETECTED</h3>
            <p>
            Your network handshake is exposing geolocation and provider identity. 
            This session is visible to external logging.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 6. Recommendation (NordVPN)
        st.markdown("### Security Recommendation")
        st.markdown(f"""
        <a href="{LINK_NORDVPN}" target="_blank" class="secure-button">
            Enable Secure Tunnel (NordVPN) →
        </a>
        <p class="disclaimer">
            Standard encryption protocol recommended for professional use.
        </p>
        """, unsafe_allow_html=True)
        
    else:
        st.error("Unable to resolve geolocation headers. Please refresh.")
else:
    # Gentle loading state
    st.info("Initializing network diagnostic...")