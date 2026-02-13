import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="RA Influence Matrix", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMarkdown h1, h2, h3 { color: #00f2ff; }
    .stInfo { background-color: #1e2a3a; border-left: 5px solid #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: 10-SLIDER CONTROL MATRIX ---
st.sidebar.title("🎮 RA Control Matrix")
st.sidebar.subheader("🌍 External Influences")
p_mech = st.sidebar.slider("Mechanical Pressure (P_mech)", 0.0, 1.0, 0.25)
t_rad = st.sidebar.slider("Thermal Stress (T_rad)", 0.0, 1.0, 0.35)
v_res = st.sidebar.slider("Vibrational Res (V_res)", 0.0, 1.0, 0.15)

st.sidebar.markdown("---")
st.sidebar.subheader("🧬 Internal RA Nodes")
ra1 = st.sidebar.slider("RA Node 1 (Linked: P_mech)", 0.0, 1.0, p_mech)
ra2 = st.sidebar.slider("RA Node 2 (Linked: T_rad)", 0.0, 1.0, t_rad)

# --- MAIN LAYOUT ---
st.title("🧬 RA-RNP 175,000 Influence Matrix")
st.markdown("### *Systems Counseling Approach to RA Cluster Architecture*")

col_main, col_sub = st.columns([2, 1])

with col_main:
    fig = go.Figure()

    # --- 1. THE OUTER SHELL (mRNA Filaments) ---
    # We make this a bit more transparent so we can see inside
    n_pts = 2000
    indices = np.arange(n_pts)
    phi = np.arccos(1 - 2*indices/n_pts)
    theta = np.pi * (1 + 5**0.5) * indices
    r_outer = (1.8 - (p_mech * 0.5)) 
    
    x_shell = r_outer * np.cos(theta) * np.sin(phi)
    y_shell = r_outer * np.sin(theta) * np.sin(phi)
    z_shell = r_outer * np.cos(phi)

    fig.add_trace(go.Scatter3d(
        x=x_shell, y=y_shell, z=z_shell,
        mode='lines', 
        line=dict(color='#00f2ff', width=1, opacity=0.15), # Ghostly shell
        name="RA Outer Shell"
    ))

    # --- 2. THE RA CLUSTER GLOBS (The 'Robitussin' core) ---
    # We define 3 distinct types of internal globs
    clusters = [
        {"name": "rRA (Primary Glob)", "color": "#ffcc00", "count": 6}, # Gold
        {"name": "tRA (Response Glob)", "color": "#ff3333", "count": 4}, # Red
        {"name": "snRA (Nuclear Glob)", "color": "#aa00ff", "count": 3}  # Purple
    ]

    for cluster in clusters:
        for i in range(cluster["count"]):
            # Position centers closer to the core as pressure increases
            c_center = np.random.uniform(-0.4, 0.4, 3) * (1.2 - p_mech)
            
            # Generate a dense globule of points
            g_pts = 120
            gx = c_center[0] + np.random.normal(0, 0.08, g_pts) + (np.sin(t_rad * 5) * 0.05)
            gy = c_center[1] + np.random.normal(0, 0.08, g_pts)
            gz = c_center[2] + np.random.normal(0, 0.08, g_pts)
            
            fig.add_trace(go.Scatter3d(
                x=gx, y=gy, z=gz,
                mode='markers',
                marker=dict(size=4, color=cluster["color"], opacity=0.9), # Bold markers
                name=cluster["name"]
            ))

    fig.update_layout(
        template="plotly_dark", 
        height=850, 
        margin=dict(l=0,r=0,b=0,t=0),
        scene=dict(
            xaxis_visible=False, 
            yaxis_visible=False, 
            zaxis_visible=False,
            aspectmode='data'
        )
    )
    st.plotly_chart(fig, use_container_width=True)

with col_sub:
    st.subheader("🔍 RA Matrix Inspector")
    st.write("The RA model shows how internal clusters huddle inside the protection of the RNA shell.")
    
    # Legend with RA branding
    st.markdown("""
    - 🟡 **rRA:** Ribosomal Clusters
    - 🔴 **tRA:** Transfer Clusters
    - 🟣 **snRA:** Splicing Clusters
    """)

    # 100% Reaction Calculation
    intensity = (p_mech * 1.0) + (t_rad * 0.2)
    st.metric("RA Reaction Intensity", f"{intensity:.2%}")
    st.progress(min(intensity, 1.0))
    
    st.info("**Counseling Selling Point:** This visualization demonstrates the 'safe space' inside the shell where RA clusters can survive external pressure.")

st.caption("RA-RNP Influence Model | Developed for Stanford RNA Challenge")
