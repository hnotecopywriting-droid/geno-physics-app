import streamlit as st
import plotly.graph_objects as go
import numpy as np
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="RA Layered RNP Console", layout="wide")

# --- SIDEBAR: 10 PHYSICS SLIDERS ---
st.sidebar.title("🎮 Systems Control")
with st.sidebar.expander("🌍 External Forces", expanded=True):
    p_mech = st.sidebar.slider("Mechanical Pressure", 0.0, 1.0, 0.25)
    t_rad = st.sidebar.slider("Thermal Stress", 0.0, 1.0, 0.35)
    v_res = st.sidebar.slider("Vibrational Res", 0.0, 1.0, 0.15)
    c_temp = st.sidebar.slider("Temporal Flow", 0.0, 1.0, 0.50)
    x_bio = st.sidebar.slider("Biodemographic", 0.0, 1.0, 0.20)

with st.sidebar.expander("⚖️ Internal Dynamics", expanded=True):
    gravity = st.sidebar.slider("Gravity / Grounding", 0.0, 1.0, 0.30)
    inertia = st.sidebar.slider("Inertia / Momentum", 0.0, 1.0, 0.20)
    weight = st.sidebar.slider("Emotional Weight", 0.1, 2.0, 1.0)
    tension = st.sidebar.slider("System Tension", 0.0, 1.0, 0.40)
    density = st.sidebar.slider("Core Density", 0.1, 2.0, 1.20)

# --- LAYERED ENGINE ---

def generate_live_strand(t_range, color, shift, name):
    """Generates the 'Top Layer' interactive strands."""
    # The math here is affected by the sliders
    t = np.linspace(0, 10, 150)
    # Tension makes the coils tighter, Inertia adds 'wobble'
    x = (1 + inertia) * np.sin(t * (1 + tension)) + shift[0]
    y = np.cos(t) + shift[1]
    z = t - (gravity * 3) + shift[2]
    
    return go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(color=color, width=8),
        name=name
    )

# --- MAIN UI ---
st.title("🧬 RA Fibrogicus: Layered System Model")
st.markdown("### *High-Fidelity Still Frame + Real-Time Physics Overlay*")

col_viz, col_data = st.columns([2, 1])

with col_viz:
    fig = go.Figure()

    # LAYER 1: THE BACKGROUND STILL (The 'Ideal' State)
    # We place the high-res image behind the 3D grid
    try:
        img = Image.open('your_still_frame.jpg') # <-- SAVE YOUR STILL AS THIS NAME
        fig.add_layout_image(
            dict(
                source=img,
                xref="paper", yref="paper",
                x=0, y=1,
                sizex=1, sizey=1,
                xanchor="left", yanchor="top",
                sizing="stretch",
                opacity=0.7,
                layer="below"
            )
        )
    except FileNotFoundError:
        st.warning("Please save a still frame as 'your_still_frame.jpg' in the app folder.")

    # LAYER 2: THE LIVE OVERLAY (The 'Current' State)
    # Purple snRA Strand
    fig.add_trace(generate_live_strand(10, "#aa00ff", [0.5, 0.2, -5], "snRA Layer"))
    # Red tRA Strand
    fig.add_trace(generate_live_strand(8, "#ff3333", [-0.5, -0.3, -4], "tRA Layer"))

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor="rgba(0,0,0,0)" # Transparent background so image shows through
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=800,
        margin=dict(l=0, r=0, b=0, t=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col_data:
    st.subheader("📊 Systems Metrology")
    stability = 100 - (tension * 50) - (p_mech * 20)
    st.metric("System Equilibrium", f"{stability:.1f}%")
    st.progress(max(0, stability/100))
    
    st.info("**Counseling Note:** The background image represents your core architecture. The moving lines represent your current reactions to stressors. Notice how adjusting 'Grounding' aligns the strands with the core.")

st.caption("RA Layered RNP Model | Hybrid Render 2026")
