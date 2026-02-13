import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="RA Fibrogicus RNP Model", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stMarkdown h1, h2, h3 { color: #ffffff; font-family: 'Segoe UI', sans-serif; }
    .stMetric { background-color: #1c1f26; border-radius: 8px; border-left: 5px solid #ffaa00; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #00f2ff; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: 10-SLIDER CONTROL MATRIX ---
st.sidebar.title("🎮 Control Matrix")
if st.sidebar.button("Reset to Equilibrium"):
    st.rerun()

st.sidebar.subheader("🌍 External Influences")
p_mech = st.sidebar.slider("Mechanical Pressure", 0.0, 1.0, 0.25)
t_rad = st.sidebar.slider("Thermal Stress", 0.0, 1.0, 0.35)
v_res = st.sidebar.slider("Vibrational Res", 0.0, 1.0, 0.15)
c_temp = st.sidebar.slider("Temporal Flow", 0.0, 1.0, 0.50)
x_bio = st.sidebar.slider("Biodemographic", 0.0, 1.0, 0.20)

st.sidebar.subheader("⚖️ Physics Engine")
gravity = st.sidebar.slider("Gravity Pull", 0.0, 1.0, 0.30)
inertia = st.sidebar.slider("Inertia / Momentum", 0.0, 1.0, 0.20)
weight = st.sidebar.slider("Molecular Weight", 0.1, 2.0, 1.0)
tension = st.sidebar.slider("Fiber Tension", 0.0, 1.0, 0.40)
density = st.sidebar.slider("Core Density", 0.1, 2.0, 1.20)

# --- ORGANIC ARCHITECTURE ENGINES ---

def generate_bonded_fibers(center, count, color, name, length=120):
    """Creates the tangled, 'ladder-rung' fibers for the model."""
    traces = []
    for _ in range(count):
        steps = length
        x = np.cumsum(np.random.normal(0, 0.15, steps)) + center[0]
        y = np.cumsum(np.random.normal(0, 0.15, steps)) + center[1]
        z = np.cumsum(np.random.normal(0, 0.15, steps)) - (gravity * 2) + center[2]
        
        # Primary Strand
        traces.append(go.Scatter3d(x=x, y=y, z=z, mode='lines', 
                                   line=dict(color=color, width=7), opacity=0.8, showlegend=False))
        
        # Cross-Connector Rungs (The "Little Bars")
        bx, by, bz = [], [], []
        for i in range(0, steps - 5, 6):
            # Creates a tiny horizontal bar at each interval
            bx.extend([x[i], x[i]+0.09, None])
            by.extend([y[i], y[i]+0.09, None])
            bz.extend([z[i], z[i], None])
            
        traces.append(go.Scatter3d(x=bx, y=by, z=bz, mode='lines', 
                                   line=dict(color='white', width=3), opacity=0.5, showlegend=False))
    return traces

def generate_pebbled_core(center, size):
    """The pebbled orange core glob representing the Ribosome."""
    n = int(1200 * density)
    phi = np.random.uniform(0, 2*np.pi, n)
    costheta = np.random.uniform(-1, 1, n)
    u = np.random.uniform(0, 1, n)
    theta = np.arccos(costheta)
    r = (size * np.cbrt(u)) * (1 + t_rad * 0.2)
    
    x = center[0] + r * np.sin(theta) * np.cos(phi)
    y = center[1] + r * np.sin(theta) * np.sin(phi)
    z = (center[2] + r * np.cos(theta)) - (gravity * 0.5)
    
    return go.Scatter3d(x=x, y=y, z=z, mode='markers',
                        marker=dict(size=np.random.uniform(4, 12, n), 
                                    color=x, colorscale='Oranges', opacity=0.9),
                        name="RNP Core Glob")

# --- MAIN UI DISPLAY ---
st.title("🧬 RA Fibrogicus Biological Architecture")
st.markdown("### *HBB Systems Counseling Approach to Tangled Genetic Resilience*")

col_viz, col_data = st.columns([3, 1])

with col_viz:
    fig = go.Figure()

    # 1. THE PROTECTIVE CELL SHELL
    u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
    xs = 2.8 * np.cos(u) * np.sin(v)
    ys = 2.8 * np.sin(u) * np.sin(v)
    zs = 2.8 * np.cos(v) - gravity
    fig.add_trace(go.Mesh3d(x=xs.flatten(), y=ys.flatten(), z=zs.flatten(), 
                            color='#00f2ff', opacity=0.06, name="Matrix Shell"))

    # 2. THE PEBBLED ORANGE CORE
    fig.add_trace(generate_pebbled_core([0,0,0], 1.4))
    
    # 3. THE TANGLED BONDED FIBERS
    fig.add_traces(generate_bonded_fibers([0.5, 0.4, -0.5], 5, "#ffcc00", "rRA Fibers"))
    fig.add_traces(generate_bonded_fibers([-0.6, -0.3, 0.8], 4, "#ff3333", "tRA Fibers"))
    fig.add_traces(generate_bonded_fibers([0.2, -0.8, -1.0], 3, "#aa00ff", "snRA Fibers"))

    fig.update_layout(
        template="plotly_dark", height=850, margin=dict(l=0,r=0,b=0,t=0),
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False,
                   camera=dict(eye=dict(x=1.5, y=1.5, z=1.0)))
    )
    st.plotly_chart(fig, use_container_width=True)

with col_data:
    st.subheader("🔍 RNP Fibers Inspector")
    st.metric("Matrix Alignment", f"{1.0 - (p_mech * 0.05):.4f}")
    st.metric("Core Mass", f"{density * weight:.2f} units")
    
    st.markdown("---")
    st.write("**Counseling Note:**")
    st.info("This model shows how protein bonds hold genetic strands together like daily habits under Thermal Stress.")
    
    st.success("✅ Architecture Stable")
