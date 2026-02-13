import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="RA Fibrogicus Systems Dashboard", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS: PRO MEDICAL/COUNSELING AESTHETIC ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMarkdown h1, h2, h3 { color: #1e3a8a; font-family: 'Helvetica Neue', sans-serif; }
    /* Style for the video container */
    video { 
        border-radius: 20px; 
        box-shadow: 0px 15px 35px rgba(0,0,0,0.2); 
        border: 2px solid #e5e7eb;
    }
    /* Style for metrics */
    [data-testid="stMetricValue"] { color: #1e3a8a; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: 10-SLIDER CONTROL MATRIX ---
st.sidebar.title("🎮 Systems Control Matrix")
st.sidebar.write("Adjust sliders to reflect the client's current environmental and internal state.")

with st.sidebar.expander("🌍 External Influences", expanded=True):
    p_mech = st.sidebar.slider("Mechanical Pressure", 0.0, 1.0, 0.25)
    t_rad = st.sidebar.slider("Thermal Stress", 0.0, 1.0, 0.35)
    v_res = st.sidebar.slider("Vibrational Res", 0.0, 1.0, 0.15)
    c_temp = st.sidebar.slider("Temporal Flow", 0.0, 1.0, 0.50)
    x_bio = st.sidebar.slider("Biodemographic", 0.0, 1.0, 0.20)

with st.sidebar.expander("⚖️ Physics & Dynamics", expanded=True):
    gravity = st.sidebar.slider("Gravity / Grounding", 0.0, 1.0, 0.30)
    inertia = st.sidebar.slider("Inertia / Momentum", 0.0, 1.0, 0.20)
    weight = st.sidebar.slider("Emotional Weight", 0.1, 2.0, 1.0)
    tension = st.sidebar.slider("System Tension", 0.0, 1.0, 0.40)
    density = st.sidebar.slider("Core Density", 0.1, 2.0, 1.20)

if st.sidebar.button("Reset to Equilibrium"):
    st.rerun()

# --- MAIN UI ---
st.title("🧬 RA Fibrogicus: High-Fidelity Systems Model")
st.markdown("#### *HBB Systems Counseling Approach to Genetic Resilience*")

col_vid, col_data = st.columns([2, 1])

with col_vid:
    # VIDEO ENGINE
    video_filename = '2026-02-13T10-05-13_a_3d_model_of_rna_watermarked.mp4'
    try:
        video_file = open(video_filename, 'rb')
        video_bytes = video_file.read()
        # Autoplay and Loop are key for the "Living Model" feel
        st.video(video_bytes, format="video/mp4", loop=True, autoplay=True, muted=True)
    except FileNotFoundError:
        st.error(f"❌ Video file '{video_filename}' not found in the current folder.")
        st.info("Please ensure the video file is named correctly and located in the same directory as this script.")

with col_data:
    st.subheader("🔍 Real-Time Analysis")
    
    # Mathematical Stability Logic linked to Sliders
    # We weigh Tension and Thermal Stress as the biggest destabilizers
    stability_score = 100 - (tension * 40) - (t_rad * 30) - (p_mech * 10)
    
    # Clamp score between 0 and 100
    stability_score = max(min(stability_score, 100), 0)
    
    st.metric("System Stability", f"{stability_score:.1f}%", delta=f"{(1-tension)*100:.0f}% Resilience")
    st.progress(stability_score / 100)
    
    st.markdown("---")
    st.write("### 📝 Counseling Insights")
    
    if stability_score > 75:
        st.success("**Architecture Stable:** The core density is effectively absorbing external pressure. Suggest maintaining current 'Grounding' exercises.")
    elif stability_score > 40:
        st.warning("**High Tension Detected:** The system is beginning to fray. Increase 'Vibrational Res' to counteract Mechanical Pressure.")
    else:
        st.error("**Systemic Collapse Risk:** Critical stress levels. The 'Emotional Weight' is overwhelming the protein bonds. Immediate stabilization required.")

st.divider()
st.caption("Visual powered by Luma Gen | Systems Architecture by RA Counseling © 2026")
