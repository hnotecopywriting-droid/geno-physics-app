import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="RA High-Def RNP Model", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM NEON THEME ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMarkdown h1, h2, h3 { color: #00f2ff; }
    .stMetric { background-color: #1e2a3a; padding: 10px; border-radius: 10px; border: 1px solid #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: 10 CONTROL MATRIX & RESET ---
st.sidebar.title("🎮 RA Control Matrix")

if st.sidebar.button("🔄 Reset to Equilibrium"):
    st.rerun()

st.sidebar.subheader("🌍 External Influences")
p_mech = st.sidebar.slider("Mechanical Pressure", 0.0, 1.0, 0.25)
t_rad = st.sidebar.slider("Thermal Stress", 0.0, 1.0, 0.35)
v_res = st.sidebar.slider("Vibrational Res", 0.0, 1.0, 0.15)
c_temp = st.sidebar.slider("Temporal Flow", 0.0, 1.0, 0.50)
x_bio = st.sidebar.slider("Biodemographic", 0.0, 1.0, 0.20)

# --- CORE RNP GENERATOR ---
def generate_braided_strand(center, length, radius, base_twists, color, name, thickness=8):
    t = np.linspace(0, length, 250)
    # Dynamics tied to sliders
    d_twists = base_twists + (p_mech * 10)
    d_rad = radius + (t_rad * 0.5)
    
    x = center[0] + d_rad * np.sin(t * d_twists)
    y = center[1] + d_rad * np.cos(t * d_twists)
    z = center[2] + t
    
    return go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(color=color, width=thickness),
        name=name,
        opacity=0.9
    )

def generate_ribosome_glob(center, size, color, name):
    # Generates a dense cluster of points to simulate the RNP complex
    n = 400
    phi = np.random.uniform(0, 2*np.pi, n)
    costheta = np.random.uniform(-1, 1, n)
    u = np.random.uniform(0, 1, n)
    
    theta = np.arccos(costheta)
    r = size * np.cbrt(u)
    
    x = center[0] + r * np.sin(theta) * np.cos(phi)
    y = center[1] + r * np.sin(theta) * np.sin(phi)
    z = center[2] + r * np.cos(theta)
    
    return go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(size=np.random.uniform(4, 10, n), color=color, opacity=0.7),
        name=name
    )

# --- MAIN INTERFACE ---
st.title("🧬 RA-RNP Biological Architecture")
st.markdown("### *Systems Counseling Approach to Genetic Form*")

col_viz, col_data = st.columns([3, 1])

with col_viz:
    fig = go.Figure()

    # 1. THE CENTRAL RIBOSOME "GLOB" (From your 3rd image)
    # We layer multiple colors to get that "organic" orange/gold feel
    fig.add_trace(generate_ribosome_glob([0,0,0], 0.8, "#ffaa00", "Central RNP Glob"))
    fig.add_trace(generate_ribosome_glob([0,0,0], 0.6, "#ff5500", "RNP Core"))

    # 2. THE THICK HELICAL STRANDS (Braided RNA)
    # Purple Strand threading through the middle
    fig.add_trace(generate_braided_strand([0,0,-3], 6, 0.25, 4, "#aa00ff", "mRNA Template", thickness=12))
    
    # Red & Gold strands emerging from the glob
    fig.add_trace(generate_braided_strand([0.3, 0.3, 0], 2.5, 0.4, 8, "#ffcc00", "rRA Strand", thickness=10))
    fig.add_trace(generate_braided_strand([-0.3, -0.3, 0], 2.5, 0.4, 8, "#ff3333", "tRA Strand", thickness=10))

    # 3. THE OUTER PROTECTIVE SHELL
    fig.add_trace(go.Scatter3d(
        x=2 * np.sin(np.linspace(0, 10, 100)), y=2 * np.cos(np.linspace(0, 10, 100)), z=np.linspace(-3, 3, 100),
        mode='lines', line=dict(color='rgba(0,242,255,0.05)', width=20),
        name="Outer RA Matrix"
    ))

    fig.update_layout(
        template="plotly_dark", height=850, margin=dict(l=0,r=0,b=0,t=0),
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_data:
    st.subheader("🔍 RNP Helix Inspector")
    st.metric("Matrix Alignment", f"{1.0 - abs(p_mech-t_rad)*0.1:.4f}")
    
    
    st.info("**Counseling Note:** The 'Glob' in the center represents the client's core. The strands are the connections they make. Under pressure, the glob becomes denser to protect the helix.")
    st.success("✅ Architecture Stable")

st.caption("RA-RNP Biological Model | Inspired by Genomic Phase Separation")
