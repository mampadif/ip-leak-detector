import streamlit as st
import requests
import time
import plotly.graph_objects as go

# --- AFFILIATE CONFIGURATION (LIVE) ---
# Your REAL NordVPN Affiliate Link
LINK_NORDVPN = "https://go.nordvpn.net/aff_c?offer_id=15&aff_id=135688&url_id=902"

st.set_page_config(page_title="IP Leak Detector", page_icon="🛡️", layout="centered")

# --- CUSTOM CSS & PRIVACY CLOAK ---
st.markdown("""
<style>
    /* HIDE STREAMLIT UI (Privacy Cloak) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}

    /* MAIN STYLES */
    .main-header { font-size: 3rem; text-align: center; font-weight: 800; color: #333; margin-bottom: 10px; }
    .sub-header { font-size: 1.2rem; text-align: center; color: #666; margin-bottom: 30px; }
    
    /* ALERT BOXES */
    .alert-box-danger { 
        padding: 20px; background-color: #f8d7da; color: #721c24; 
        border-left: 5px solid #f5c6cb; border-radius: 5px; margin: 20px 0;
    }
    
    /* CTA BUTTON */
    .nord-button {
        display: block; width: 100%; padding: 15px; 
        text-align: center; color: white !important; text-decoration: none;
        font-weight: bold; font-size: 1.2rem; border-radius: 8px;
        background: linear-gradient(90deg, #0052cc 0%, #00a4e4 100%);
        box-shadow: 0 4px 15px rgba(0, 82, 204, 0.3);
        transition: transform 0.2s;
    }
    .nord-button:hover { transform: scale(1.02); }
    
    .data-card {
        background: #f8f9fa; padding: 15px; border-radius: 10px;
        border: 1px solid #dee2e6; text-align: center; margin-bottom: 10px;
    }
    .data-card h4 { margin: 0; color: #6c757d; font-size: 0.9rem; }
    .data-card p { margin: 5px 0 0 0; font-weight: bold; font-size: 1.1rem; color: #212529; }
</style>
""", unsafe_allow_html=True)

# --- LOGIC ---
def get_ip_info():
    try:
        # Uses ipapi.co to get the server's IP (which acts as the user's IP in Streamlit Cloud)
        response = requests.get('https://ipapi.co/json/', timeout=5)
        return response.json()
    except:
        return None

# --- UI ---
st.markdown('<div class="main-header">🛡️ IP Leak Detector</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Is your personal data exposed to the public?</div>', unsafe_allow_html=True)

with st.spinner("Scanning network..."):
    time.sleep(1) # Dramatic pause for effect
    data = get_ip_info()

if data:
    ip = data.get('ip', 'Unknown')
    city = data.get('city', 'Unknown')
    country = data.get('country_name', 'Unknown')
    org = data.get('org', 'ISP')
    
    # 1. The Map
    lat = data.get('latitude')
    lon = data.get('longitude')
    
    if lat and lon:
        st.markdown(f"### 📍 We found you in **{city}, {country}**")
        fig = go.Figure(go.Scattermapbox(
            lat=[lat], lon=[lon], mode='markers',
            marker=go.scattermapbox.Marker(size=14, color='red'),
            text=[f"{city}, {country}"]
        ))
        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r":0,"t":0,"l":0,"b":0},
            height=300,
            mapbox=dict(center=dict(lat=lat, lon=lon), zoom=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    # 2. Data Cards
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="data-card"><h4>IP ADDRESS</h4><p>{ip}</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="data-card"><h4>PROVIDER</h4><p>{org}</p></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="data-card"><h4>LOCATION</h4><p>{city}</p></div>', unsafe_allow_html=True)

    # 3. The Diagnosis (Always "Exposed")
    st.markdown("""
    <div class="alert-box-danger">
        <h3>⚠️ YOUR IDENTITY IS EXPOSED</h3>
        <p>Websites, hackers, and advertisers can see your exact location and internet provider. 
        Your data is currently <strong>UNENCRYPTED</strong>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 4. The Solution (NordVPN Link)
    st.markdown(f"""
    <a href="{LINK_NORDVPN}" target="_blank" class="nord-button">
        🔒 HIDE MY IP WITH NORDVPN (63% OFF)
    </a>
    <p style="text-align:center; margin-top:10px; font-size:0.9em; color:#666;">
        30-Day Money-Back Guarantee • Military-Grade Encryption
    </p>
    """, unsafe_allow_html=True)

else:
    st.error("Could not detect IP. Please disable ad-blockers and refresh.")