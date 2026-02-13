import streamlit as st
import base64

# --- PAGE CONFIG ---
st.set_page_config(page_title="RA Fibrogicus Systems Dashboard", layout="wide")

# --- CUSTOM CSS: THE "MEDICAL CONSOLE" LOOK ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    .stMetric { background-color: #1c1f26; border-radius: 10px; padding: 15px; border-left: 5px solid #00f2ff; }
    video { width: 100%; border-radius: 15px; box-shadow: 0 0 20px rgba(0,242,255,0.2); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: THE 10-SLIDER CONTROL MATRIX ---
st.sidebar.title("🎮 Systems Control")
st.sidebar.markdown("---")

# Group 1: Environmental
st.sidebar.subheader("🌍 External Influences")
p_mech = st.sidebar.slider("Mechanical Pressure", 0.0, 1.0, 0.25)
t_rad = st.sidebar.slider("Thermal Stress", 0.0, 1.0, 0.35)
v_res = st.sidebar.slider("Vibrational Res", 0.0, 1.0, 0.15)
c_temp = st.sidebar.slider("Temporal Flow", 0.0, 1.0, 0.50)
x_bio = st.sidebar.slider("Biodemographic", 0.0, 1.0, 0.20)

# Group 2: Internal Dynamics
st.sidebar.subheader("⚖️ Physics Engine")
gravity = st.sidebar.slider("Gravity / Grounding", 0.0, 1.0, 0.30)
inertia = st.sidebar.slider("Inertia / Momentum", 0.0, 1.0, 0.20)
weight = st.sidebar.slider("Emotional Weight", 0.1, 2.0, 1.0)
tension = st.sidebar.slider("System Tension", 0.0, 1.0, 0.40)
density = st.sidebar.slider("Core Density", 0.1, 2.0, 1.20)

# --- VIDEO HANDLER: ENCODING FOR SMOOTH PLAY ---
def get_video_html(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    return f'''
        <video autoplay loop muted playsinline>
            <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    '''

# --- MAIN UI ---
st.title("🧬 RA Fibrogicus: High-Fidelity Systems Model")
st.markdown("### *Counseling Approach to Tangled Genetic Resilience*")

col_vid, col_data = st.columns([2, 1])

with col_vid:
    # This block forces the Luma video to play and loop
    video_path = '2026-02-13T10-05-13_a_3d_model_of_rna_watermarked.mp4'
    try:
        video_html = get_video_html(video_path)
        st.markdown(video_html, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("❌ Video file not found. Ensure it is in the same folder as app.py.")

with col_data:
    st.subheader("🔍 Real-Time Analysis")
    
    # Calculate Stability based on sliders
    stability = 100 - (tension * 40) - (t_rad * 30) - (p_mech * 10)
    stability = max(min(stability, 100), 0)
    
    st.metric("System Stability", f"{stability:.1f}%")
    st.progress(stability / 100)
    
    st.markdown("---")
    st.info("**Counseling Selling Point:** This visualization shows that while the system (the fibers) may look tangled, the core (the ribosome) remains a solid foundation. Our goal is to lower the 'System Tension' to maintain this equilibrium.")

st.caption("Visual powered by Luma AI | Systems Architecture by RA Counseling 2026")
