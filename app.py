import streamlit as st
import requests
import time
import pandas as pd

# --- CONFIGURATION ---
# REPLACE THIS with your NordVPN Affiliate Link later
LINK_NORDVPN = "https://nordvpn.com/affiliate/link" 

st.set_page_config(page_title="IP Leak Detector", page_icon="🛡️", layout="centered")

# --- CSS STYLING (Professional & Alarming) ---
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; text-align: center; margin-bottom: 2rem; font-weight: 700; }
    .ip-box { background-color: #FFEBEE; border: 2px solid #FF5252; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    .detail-label { font-weight: bold; color: #555; }
    .cta-button { 
        display: block; width: 100%; padding: 15px; 
        background-color: #2962FF; color: white !important; 
        text-align: center; text-decoration: none; font-weight: bold; 
        border-radius: 8px; font-size: 1.2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .cta-button:hover { background-color: #0039CB; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# --- LOGIC ---
def get_ip_data():
    """Fetches public IP data from a free API."""
    try:
        # ip-api.com is free for non-commercial use (perfect for this demo)
        response = requests.get('http://ip-api.com/json/')
        return response.json()
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

# --- UI LAYOUT ---
st.markdown('<h1 class="main-header">🛡️ IP Leak Detector</h1>', unsafe_allow_html=True)
st.write("Check what websites, hackers, and your ISP can see about you right now.")

if st.button("🔍 Scan My Connection", type="primary", use_container_width=True):
    with st.spinner("Pinging external servers..."):
        time.sleep(1.5) # Slight delay for dramatic effect
        data = get_ip_data()
        
    if data and data.get('status') == 'success':
        # 1. THE VERDICT (The Hook)
        st.markdown(f"""
        <div class="ip-box">
            <h2 style="color: #D32F2F; margin:0;">⚠️ YOU ARE EXPOSED</h2>
            <p style="font-size: 1.2rem; margin-top:10px;">Your Public IP Address is:</p>
            <h1 style="font-family: monospace; font-size: 3rem; color: #333;">{data.get('query')}</h1>
        </div>
        """, unsafe_allow_html=True)

        # 2. THE DETAILS (The Proof)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📍 Location Detected:**")
            st.write(f"{data.get('city')}, {data.get('regionName')}")
            st.write(f"{data.get('country')}")
            
        with col2:
            st.markdown("**🏢 ISP Detected:**")
            st.write(f"{data.get('isp')}")
            st.markdown("**📡 Coordinates:**")
            st.write(f"{data.get('lat')}, {data.get('lon')}")

        # 3. THE MAP (The Visual)
        st.markdown("### 🗺️ They can pinpoint your location here:")
        if 'lat' in data and 'lon' in data:
            map_df = pd.DataFrame({'lat': [data['lat']], 'lon': [data['lon']]})
            st.map(map_df, zoom=10)

        # 4. THE SOLUTION (The Sale)
        st.markdown("---")
        st.markdown("""
        ### 🛑 Stop broadcasting your personal data.
        Websites use this data to track you. Hackers use it to target you. Your ISP sells this data to advertisers.
        
        **Hide your IP instantly with a VPN:**
        """)
        
        st.markdown(f"""
        <a href="{LINK_NORDVPN}" target="_blank" class="cta-button">
            🛡️ Encrypt My Connection with NordVPN
        </a>
        <p style="text-align: center; margin-top: 10px; font-size: 0.8rem; color: #666;">
            30-Day Money-Back Guarantee • Block Ads & Trackers
        </p>
        """, unsafe_allow_html=True)

    else:
        st.error("Could not fetch IP data. Please check your internet connection.")

# --- SIDEBAR EDUCATION ---
with st.sidebar:
    st.header("Why does this matter?")
    st.info("""
    **Your IP Address is your digital fingerprint.**
    
    It reveals:
    1. **Who you are** (linked to your ISP account)
    2. **Where you live** (City/Zip accuracy)
    3. **What you do** (Your ISP sees every site you visit)
    """)
    st.markdown("---")
    st.caption("Built with Python & Streamlit")