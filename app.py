import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="RA Fibrogicus RNP", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMarkdown h1, h2, h3 { color: #00f2ff; }
    .stMetric { background-color: #1e2a3a; border-radius: 10px; border: 1px solid #ffaa00; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: PHYSICS ENGINE SLIDERS ---
st.sidebar.title("🎮 RA Physics Engine")
if st.sidebar.button("🔄 Reset Equilibrium"):
    st.rerun()

st.sidebar.subheader("⚖️ Force Multipliers")
gravity = st.sidebar.slider("Gravity Pull (G-Force)", 0.0, 1.0, 0.30)
inertia = st.sidebar.slider("Inertia / Momentum", 0.0, 1.0, 0.20)
weight = st.sidebar.slider("Molecular Weight", 0.1, 2.0, 1.0)
thermal = st.sidebar.slider("Thermal Tension", 0.0, 1.0, 0.40)

st.sidebar.markdown("---")
st.sidebar.subheader("🌍 Environmental Influence")
p_mech = st.sidebar.slider("Mechanical Pressure", 0.0, 1.0, 0.25)
v_res = st.sidebar.slider("Vibrational Resonance", 0.0, 1.0, 0.15)
c_temp = st.sidebar.slider("Temporal Flow", 0.0, 1.0, 0.50)

# --- ORGANIC RNP GENERATORS ---

def generate_fibers(center, count, color, name, length=100):
    """Creates the 'beaded string' look of protein fibers."""
    traces = []
    for _ in range(count):
        # Random walk math to create 'tangled' fibers
        steps = length
        x = np.cumsum(np.random.normal(0, 0.1, steps)) * (1 + inertia) + center[0]
        y = np.cumsum(np.random.normal(0, 0.1, steps)) * (1 + inertia) + center[1]
        z = np.cumsum(np.random.normal(0, 0.1, steps)) - (gravity * 2) + center[2]
        
        traces.append(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(color=color, width=3 + (weight * 2)),
            opacity=0.6,
            name=name,
            showlegend=False
        ))
    return traces

def generate_ra_glob(center, size, color, name):
    """Creates the dense Ribosome core with 'Internal Tension'."""
    n = int(500 * weight)
    # Sphere mapping with thermal 'jitter'
    phi = np.random.uniform(0, 2*np.pi, n)
    costheta = np.random.uniform(-1, 1, n)
    u = np.random.uniform(0, 1, n)
    
    theta = np.arccos(costheta)
    r = (size * np.cbrt(u)) * (1 + thermal * 0.5)
    
    # Gravity pulls the glob down, Pressure packs it in
    x = center[0] + r * np.sin(theta) * np.cos(phi)
    y = center[1] + r * np.sin(theta) * np.sin(phi)
    z = (center[2] + r * np.cos(theta)) - (gravity * 0.5)
    
    return go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=np.random.uniform(3, 8, n),
            color=color,
            opacity=0.8,
            colorscale='Oranges'
        ),
        name=name
    )

# --- MAIN INTERFACE ---
st.title("🧬 RA-RNP Fibrogicus Architecture")
st.markdown("### *Systems Counseling Approach to Tangled Genetic Resilience*")

col_viz, col_data = st.columns([3, 1])

with col_viz:
    fig = go.Figure()

    # 1. THE CENTRAL RIBOSOME "MEAT" (Dense Core)
    fig.add_trace(generate_ra_glob([0,0,0], 1.2, "#ff6600", "RA Core Glob"))
    
    # 2. TANGLED PROTEIN FIBERS (The 'Bonding' lines)
    # Gold rRNA fibers
    fig.add_traces(generate_fibers([0.2, 0.2, 0], 5, "#ffcc00", "rRA Fibers"))
    # Red tRA fibers
    fig.add_traces(generate_fibers([-0.3, -0.3, 0], 4, "#ff3333", "tRA Fibers"))
    # Purple snRA fibers
    fig.add_traces(generate_fibers([0, 0, 0.5], 3, "#aa00ff", "snRA Fibers"))

    # 3. OUTER CYTOPLASMIC SHELL (Ghostly)
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    xs = 2.5 * np.cos(u) * np.sin(v)
    ys = 2.5 * np.sin(u) * np.sin(v)
    zs = 2.5 * np.cos(v) - gravity
    fig.add_trace(go.Mesh3d(x=xs.flatten(), y=ys.flatten(), z=zs.flatten(), 
                            color='cyan', opacity=0.03, name="RA Matrix"))

    fig.update_layout(
        template="plotly_dark", height=850, margin=dict(l=0,r=0,b=0,t=0),
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False,
                   camera=dict(eye=dict(x=1.8, y=1.8, z=1.2)))
    )
    st.plotly_chart(fig, use_container_width=True)

with col_data:
    st.subheader("🔍 Fibrogicus Inspector")
    
    # REACTIVE METRICS
    st.metric("System Inertia", f"{inertia * 100:.1f}%")
    st.metric("Gravitational Load", f"{gravity * 9.8:.2f} m/s²")
    
    st.markdown("---")
    st.info("**Counseling Insight:** Notice how the 'Protein Fibers' bond together to hold the core during high Gravity. In a crisis, your connections (the fibers) are what stop your core (the glob) from falling apart.")
    
    st.success("✅ Architecture Stable")

st.caption("RA-RNP Fibrogicus Model | Inspired by Genomic Phase Separation & Ribosome Complexity")
