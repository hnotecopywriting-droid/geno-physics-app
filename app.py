import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="RA Fibrogicus Bonded", layout="wide", initial_sidebar_state="expanded")

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

# --- ORGANIC BONDED FIBER GENERATOR ---

def generate_bonded_fibers(center, count, color, name, length=80):
    """Creates organic fibers with tiny cross-connector rungs."""
    traces = []
    for _ in range(count):
        steps = length
        # Primary Strand (The Backbone)
        x = np.cumsum(np.random.normal(0, 0.12, steps)) + center[0]
        y = np.cumsum(np.random.normal(0, 0.12, steps)) + center[1]
        z = np.cumsum(np.random.normal(0, 0.12, steps)) - (gravity * 2) + center[2]
        
        # Secondary Strand (Slightly offset to create the ladder)
        x2 = x + 0.1
        y2 = y + 0.1
        z2 = z 

        # 1. Add the main thick strands
        traces.append(go.Scatter3d(x=x, y=y, z=z, mode='lines', 
                                   line=dict(color=color, width=6), opacity=0.7, showlegend=False))
        
        # 2. Add the CROSS CONNECTORS (The little bars)
        cx, cy, cz = [], [], []
        for i in range(0, steps, 5): # Every 5th point, draw a rung
            cx.extend([x[i], x2[i], None])
            cy.extend([y[i], y2[i], None])
            cz.extend([z[i], z2[i], None])
            
        traces.append(go.Scatter3d(x=cx, y=cy, z=cz, mode='lines', 
                                   line=dict(color='white', width=2), 
                                   opacity=0.4, name=f"{name} Connectors"))
        
    return traces

def generate_ra_glob(center, size, color):
    """The dense Ribosome meat from the previous successful version."""
    n = int(550 * weight)
    phi = np.random.uniform(0, 2*np.pi, n)
    costheta = np.random.uniform(-1, 1, n)
    u = np.random.uniform(0, 1, n)
    theta = np.arccos(costheta)
    r = (size * np.cbrt(u)) * (1 + thermal * 0.4)
    
    x = center[0] + r * np.sin(theta) * np.cos(phi)
    y = center[1] + r * np.sin(theta) * np.sin(phi)
    z = (center[2] + r * np.cos(theta)) - (gravity * 0.7)
    
    return go.Scatter3d(x=x, y=y, z=z, mode='markers',
                        marker=dict(size=np.random.uniform(3, 9, n), 
                                    color=color, opacity=0.8, colorscale='YlOrRd'),
                        name="RA Ribosome Core")

# --- MAIN INTERFACE ---
st.title("🧬 RA-RNP Fibrogicus (Bonded Edition)")
st.markdown("### *Systems Counseling Approach to Genetic Connectivity*")

col_viz, col_data = st.columns([3, 1])

with col_viz:
    fig = go.Figure()

    # 1. THE HEAVY RIBOSOME GLOB (The core "Meat")
    fig.add_trace(generate_ra_glob([0,0,0], 1.2, "#ff6600"))
    
    # 2. TANGLED BONDED FIBERS (The stringy stuff with bars)
    fig.add_traces(generate_bonded_fibers([0.3, 0.3, 0], 4, "#ffcc00", "rRA Fibers"))
    fig.add_traces(generate_bonded_fibers([-0.4, -0.2, 0.5], 3, "#ff3333", "tRA Fibers"))
    fig.add_traces(generate_bonded_fibers([0.1, -0.5, -0.5], 3, "#aa00ff", "snRA Fibers"))

    # 3. THE OUTER MATRIX
    fig.update_layout(
        template="plotly_dark", height=850, margin=dict(l=0,r=0,b=0,t=0),
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False,
                   camera=dict(eye=dict(x=1.6, y=1.6, z=1.0)))
    )
    st.plotly_chart(fig, use_container_width=True)

with col_data:
    st.subheader("🔍 Connector Inspector")
    st.metric("Bonding Integrity", f"{1.0 - (thermal * 0.2):.2%}")
    
    

    st.info("**Counseling Selling Point:** Look at the tiny white bars. Those are the **Bonds**. They represent the micro-connections—the small daily habits—that keep your entire genetic 'fiber' from becoming just a loose wire.")
    
    st.success("✅ System Bonded & Stable")

st.caption("RA-RNP Fibrogicus Bonded | Stanford RNA 3D Challenge 2026")
