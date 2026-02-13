import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="RA Fibrogicus Systems Dashboard", 
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMarkdown h1, h2, h3 { color: #1e3a8a; font-family: 'Helvetica Neue', sans-serif; }
    video { 
        border-radius: 20px; 
        box-shadow: 0px 15px 35px rgba(0,0,0,0.2); 
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("🎮 Systems Control")
p_mech = st.sidebar.slider("Mechanical Pressure", 0.0, 1.0, 0.25)
t_rad = st.sidebar.slider("Thermal Stress", 0.0, 1.0, 0.35)
v_res = st.sidebar.slider("Vibrational Res", 0.0, 1.0, 0.15)
c_temp = st.sidebar.slider("Temporal Flow", 0.0, 1.0, 0.50)
x_bio = st.sidebar.slider("Biodemographic", 0.0, 1.0, 0.20)
gravity = st.sidebar.slider("Gravity / Grounding", 0.0, 1.0, 0.30)
inertia = st.sidebar.slider("Inertia / Momentum", 0.0, 1.0, 0.20)
weight = st.sidebar.slider("Emotional Weight", 0.1, 2.0, 1.0)
tension = st.sidebar.slider("System Tension", 0.0, 1.0, 0.40)
density = st.sidebar.slider("Core Density", 0.1, 2.0, 1.20)

# --- MAIN UI ---
st.title("🧬 RA Fibrogicus: High-Fidelity Systems Model")

col_vid, col_data = st.columns([2, 1])

with col_vid:
    video_filename = '2026-02-13T10-05-13_a_3d_model_of_rna_watermarked.mp4'
    try:
        # We use st.video with autoplay and muted set to True to ensure it plays
        st.video(video_filename, format="video/mp4", loop=True, autoplay=True, muted=True)
    except Exception as e:
        st.error(f"Error loading video: {e}")

with col_data:
    st.subheader("🔍 Real-Time Analysis")
    stability_score = 100 - (tension * 40) - (t_rad * 30) - (p_mech * 10)
    stability_score = max(min(stability_score, 100), 0)
    
    st.metric("System Stability", f"{stability_score:.1f}%")
    st.progress(stability_score / 100)
    
    st.info("**Counseling Note:** Observe the 'pebbled' texture. As tension increases, we work to stabilize these bonds.")

st.caption("RA Counseling Presentation Tool 2026")
