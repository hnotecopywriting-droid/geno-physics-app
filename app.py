import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="RA Deep Helix RNP", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMarkdown h1, h2, h3 { color: #00f2ff; }
    .stMetric { background-color: #1e2a3a; border-radius: 10px; border: 1px solid #ffaa00; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: PHYSICS ENGINE ---
st.sidebar.title("🎮 RA Physics Engine")
if st.sidebar.button("🔄 Reset Equilibrium"):
    st.rerun()

st.sidebar.subheader("⚖️ Force Multipliers")
gravity = st.sidebar.slider("Gravity Pull", 0.0, 1.0, 0.30)
inertia = st.sidebar.slider("Inertia / Momentum", 0.0, 1.0, 0.20)
weight = st.sidebar.slider("Molecular Weight", 0.1, 2.0, 1.0)
thermal = st.sidebar.slider("Thermal Tension", 0.0, 1.0, 0.40)

st.sidebar.markdown("---")
st.sidebar.subheader("🌍 Environmental Influence")
p_mech = st.sidebar.slider("Mechanical Pressure", 0.0, 1.0, 0.25)
v_res = st.sidebar.slider("Vibrational Resonance", 0.0, 1.0, 0.15)

# --- ADVANCED HELIX & CONNECTOR GENERATOR ---

def generate_connected_helix(center, twists, length, color, name, radius=0.3):
    """Generates a helix with internal protein connectors (rungs)."""
    t = np.linspace(0, length, 100)
    
    # Physics modifiers
    d_twists = twists + (p_mech * 5)
    d_rad = radius + (thermal * 0.2)
    
    # Strand A (The Backbone)
    x1 = center[0] + d_rad * np.sin(t * d_twists)
    y1 = center[1] + d_rad * np.cos(t * d_twists)
    z1 = center[2] + t - (gravity * 1.5)
    
    # Strand B (The Complementary Backbone)
    x2 = center[0] + d_rad * np.sin(t * d_twists + np.pi)
    y2 = center[1] + d_rad * np.cos(t * d_twists + np.pi)
    z2 = z1
    
    traces = []
    
    # Add Backbones
    traces.append(go.Scatter3d(x=x1, y=y1, z=z1, mode='lines', 
                               line=dict(color=color, width=8), name=name, opacity=0.8))
    traces.append(go.Scatter3d(x=x2, y=y2, z=z2, mode='lines', 
                               line=dict(color=color, width=8), showlegend=False, opacity=0.8))
    
    # Add Connectors (The Rungs/Protein Connectors)
    # We draw lines between x1,y1,z1 and x2,y2,z2 every few steps
    cx, cy, cz = [], [], []
    for i in range(0, len(t), 4):
        cx.extend([x1[i], x2[i], None])
        cy.extend([y1[i], y2[i], None])
        cz.extend([z1[i], z2[i], None])
        
    traces.append(go.Scatter3d(x=cx, y=cy, z=cz, mode='lines', 
                               line=dict(color='white', width=3), 
                               name=f"{name} Connectors", opacity=0.4))
    
    # Add the "Dots" (Protein nodes) on the connectors
    traces.append(go.Scatter3d(x=x1[::4], y=y1[::4], z=z1[::4], mode='markers',
                               marker=dict(size=4, color='white', opacity=0.9), showlegend=False))
    
    return traces

def generate_ra_glob(center, size, color):
    """Creates the dense Ribosome core."""
    n = int(600 * weight)
    phi = np.random.uniform(0, 2*np.pi, n)
    costheta = np.random.uniform(-1, 1, n)
    u = np.random.uniform(0, 1, n)
    theta = np.arccos(costheta)
    r = (size * np.cbrt(u)) * (1 + thermal * 0.3)
    
    x = center[0] + r * np.sin(theta) * np.cos(phi)
    y = center[1] + r * np.sin(theta) * np.sin(phi)
    z = (center[2] + r * np.cos(theta)) - (gravity * 0.8)
    
    return go.Scatter3d(x=x, y=y, z=z, mode='markers',
                        marker=dict(size=np.random.uniform(3, 9, n), 
                                    color=color, opacity=0.7, colorscale='YlOrRd'),
                        name="RA Ribosome Core")

# --- MAIN INTERFACE ---
st.title("🧬 RA-RNP Deep Helix Architecture")
st.markdown("### *Systems Counseling Approach to Connected Genetic Form*")

col_viz, col_data = st.columns([3, 1])

with col_viz:
    fig = go.Figure()

    # 1. THE RIBOSOME CORE
    fig.add_trace(generate_ra_glob([0,0,0], 1.3, "#ff6600"))
    
    # 2. THE CONNECTED HELICES (The "Real" Strands)
    # Gold rRA
    fig.add_traces(generate_connected_helix([0.5, 0.5, -1], 8, 3, "#ffcc00", "rRA Helix"))
    # Red tRA
    fig.add_traces(generate_connected_helix([-0.6, -0.4, 0], 6, 2.5, "#ff3333", "tRA Helix"))
    # Purple snRA (Single strand with markers to look like mRNA)
    fig.add_traces(generate_connected_helix([0, -0.8, -2], 12, 4, "#aa00ff", "snRA Helix", radius=0.2))

    fig.update_layout(
        template="plotly_dark", height=850, margin=dict(l=0,r=0,b=0,t=0),
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False,
                   camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)))
    )
    st.plotly_chart(fig, use_container_width=True)

with col_data:
    st.subheader("🔍 Helix Inspector")
    st.metric("Molecular Weight", f"{weight:.2f} kDa")
    st.metric("Tension Score", f"{(p_mech + thermal)/2:.2%}")
    
    
    

    st.info("**Counseling Selling Point:** Notice the connectors (the white rungs). These are the 'Bonds'—the shared values and connections that prevent the helices from unraveling under pressure.")
    
    st.success("✅ Architecture Bonded")

st.caption("RA-RNP Deep Helix Model | 175,000 Residue Simulation | Stanford 2026")
