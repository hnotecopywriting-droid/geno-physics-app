import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="RA Cinematic RNP", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS: PRO DASHBOARD LOOK ---
st.markdown("""
    <style>
    .main { background-color: #05070a; }
    .stMarkdown h1, h2, h3 { color: #ffffff; text-shadow: 0 0 8px #00f2ff; }
    .stMetric { background-color: #0e121a; border-radius: 12px; border: 1px solid #1e2a3a; padding: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: 10-SLIDER CONTROL MATRIX ---
st.sidebar.title("🎮 Control Matrix")
if st.sidebar.button("🔄 Reset Equilibrium"):
    st.rerun()

st.sidebar.subheader("🌍 External Influences")
p_mech = st.sidebar.slider("Mechanical Pressure", 0.0, 1.0, 0.25)
t_rad = st.sidebar.slider("Thermal Stress", 0.0, 1.0, 0.35)
v_res = st.sidebar.slider("Vibrational Resonance", 0.0, 1.0, 0.15)
c_temp = st.sidebar.slider("Temporal Flow", 0.0, 1.0, 0.50)
x_bio = st.sidebar.slider("Biodemographic", 0.0, 1.0, 0.20)

st.sidebar.subheader("⚖️ Physics Engine")
gravity = st.sidebar.slider("Gravity Pull", 0.0, 1.0, 0.30)
inertia = st.sidebar.slider("Inertia / Momentum", 0.0, 1.0, 0.40)
weight = st.sidebar.slider("Molecular Weight", 0.1, 2.0, 1.0)
tension = st.sidebar.slider("Fiber Tension", 0.0, 1.0, 0.40)
density = st.sidebar.slider("Core Density", 0.1, 2.0, 1.30)

# --- THE "EXACT MATCH" RNP ENGINES ---

def generate_cinematic_helix(center, twists, length, color, name):
    """Generates tight, pebbled helical strands that match the image texture."""
    t = np.linspace(0, length, 400)
    # Math for the tight twist
    d_twists = twists + (inertia * 8)
    radius = 0.12 + (tension * 0.05)
    
    # Primary Strand
    x1 = center[0] + radius * np.sin(t * d_twists)
    y1 = center[1] + radius * np.cos(t * d_twists)
    z1 = center[2] + t - (gravity * 2)
    
    # Secondary Strand (Offset for that thick braided look)
    x2 = x1 + 0.05
    y2 = y1 + 0.05
    
    traces = []
    # Using 'markers' instead of lines to get that pebbled/atomistic texture from the picture
    traces.append(go.Scatter3d(x=x1, y=y1, z=z1, mode='markers', 
                               marker=dict(size=3, color=color, opacity=0.9), name=name))
    traces.append(go.Scatter3d(x=x2, y=y2, z=z1, mode='markers', 
                               marker=dict(size=3, color=color, opacity=0.7), showlegend=False))
    
    # Add horizontal 'rung' connectors
    rx, ry, rz = [], [], []
    for i in range(0, len(t), 10):
        rx.extend([x1[i], x2[i], None])
        ry.extend([y1[i], y2[i], None])
        rz.extend([z1[i], z1[i], None])
        
    traces.append(go.Scatter3d(x=rx, y=ry, z=rz, mode='lines', 
                               line=dict(color='white', width=1), opacity=0.3, showlegend=False))
    return traces

def generate_chunky_core(center, size):
    """The massive, pebbled orange ribosome core."""
    n = int(1500 * density)
    phi = np.random.uniform(0, 2*np.pi, n)
    costheta = np.random.uniform(-1, 1, n)
    u = np.random.uniform(0, 1, n)
    theta = np.arccos(costheta)
    r = size * np.cbrt(u)
    
    x = center[0] + r * np.sin(theta) * np.cos(phi)
    y = center[1] + r * np.sin(theta) * np.sin(phi)
    z = (center[2] + r * np.cos(theta)) - (gravity * 0.5)
    
    return go.Scatter3d(x=x, y=y, z=z, mode='markers',
                        marker=dict(size=np.random.uniform(4, 14, n), 
                                    color=x, colorscale='Oranges', opacity=1.0),
                        name="RNP Ribosome Core")

# --- MAIN UI ---
st.title("🔬 RA-RNP Cinematic Biological Architecture")
st.markdown("### *Systems Counseling approach to Ribonucleoprotein Form*")

col_viz, col_data = st.columns([3, 1])

with col_viz:
    fig = go.Figure()

    # 1. THE GLOWING MATRIX SHELL (The Background Sphere)
    u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
    xs = 2.5 * np.cos(u) * np.sin(v)
    ys = 2.5 * np.sin(u) * np.sin(v)
    zs = 2.5 * np.cos(v) - gravity
    fig.add_trace(go.Mesh3d(x=xs.flatten(), y=ys.flatten(), z=zs.flatten(), 
                            color='deepskyblue', opacity=0.08, name="Cellular Boundary"))

    # 2. THE PEBBLED CORE (The Meat)
    fig.add_trace(generate_chunky_core([0,0,0], 1.3))
    
    # 3. CINEMATIC STRANDS (Threaded exactly like the photo)
    # Purple Strand - Vertical
    fig.add_traces(generate_cinematic_helix([0, 0, -3], 15, 6, "#8a2be2", "mRNA Template"))
    # Gold Strand - Diagonal
    fig.add_traces(generate_cinematic_helix([0.5, 0.3, -2], 12, 4.5, "#ffcc00", "rRA Helix"))
    # Red Strand - Diagonal
    fig.add_traces(generate_cinematic_helix([-0.4, -0.4, -1], 10, 4, "#ff3333", "tRA Helix"))

    fig.update_layout(
        template="plotly_dark", height=850, margin=dict(l=0,r=0,b=0,t=0),
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False,
                   camera=dict(eye=dict(x=1.3, y=1.3, z=0.7)))
    )
    st.plotly_chart(fig, use_container_width=True)

with col_data:
    st.subheader("🔍 Cinematic Inspector")
    st.metric("Matrix Alignment", "99.2%")
    st.metric("System Tension", f"{inertia:.2%}")
    
        
    st.info("**Counseling Selling Point:** This visualization shows that even when a system looks tangled (the fibers), it has a solid core (the ribosome). Our work is to ensure the bonds (the white connectors) remain strong during stress.")
    
    st.success("✅ Architecture Rendered")

st.caption("RA-RNP Cinematic Render | Created for Systems Counseling Presentation 2026")
