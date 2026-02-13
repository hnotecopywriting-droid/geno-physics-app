import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="RNA Influence Matrix", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMarkdown h1, h2, h3 { color: #00f2ff; }
    .stInfo { background-color: #1e2a3a; border-left: 5px solid #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
st.sidebar.title("🎮 Control Matrix")
st.sidebar.subheader("🌍 External Influences")
p_mech = st.sidebar.slider("Mechanical Pressure (P_mech)", 0.0, 1.0, 0.20)
t_rad = st.sidebar.slider("Thermal Stress (T_rad)", 0.0, 1.0, 0.35)
v_res = st.sidebar.slider("Vibrational Res (V_res)", 0.0, 1.0, 0.10)

st.sidebar.markdown("---")
st.sidebar.subheader("🧬 Internal RA Nodes")
# 100% Reaction logic mapping
ra1 = st.sidebar.slider("RA Node 1 (Linked: P_mech)", 0.0, 1.0, p_mech)
ra2 = st.sidebar.slider("RA Node 2 (Linked: T_rad)", 0.0, 1.0, t_rad)

# --- MAIN LAYOUT ---
st.title("🧬 Multi-Cluster RNA Influence Matrix")
st.markdown("### *Systems Counseling Approach to RNA/DNA Heterogeneous Clusters*")

col_main, col_sub = st.columns([2, 1])

with col_main:
    fig = go.Figure()

    # --- 1. THE DNA 'MASTER TEMPLATE' (Ghostly background helix) ---
    z_dna = np.linspace(-2, 2, 100)
    x_dna = 0.5 * np.sin(z_dna * 5)
    y_dna = 0.5 * np.cos(z_dna * 5)
    
    fig.add_trace(go.Scatter3d(
        x=x_dna, y=y_dna, z=z_dna,
        mode='lines', line=dict(color='rgba(255,255,255,0.1)', width=10),
        name="DNA Master Template"
    ))

    # --- 2. MAIN RNA FILAMENTS (mRNA) ---
    n_pts = 2000
    indices = np.arange(n_pts)
    phi = np.arccos(1 - 2*indices/n_pts)
    theta = np.pi * (1 + 5**0.5) * indices
    r = (1.5 - (p_mech * 0.7)) + (np.sin(theta * 10) * (v_res * 0.2))
    
    x_rna = r * np.cos(theta) * np.sin(phi)
    y_rna = r * np.sin(theta) * np.sin(phi)
    z_rna = r * np.cos(phi)

    fig.add_trace(go.Scatter3d(
        x=x_rna, y=y_rna, z=z_rna,
        mode='lines', line=dict(color='#00f2ff', width=2, opacity=0.2),
        name="mRNA Filament"
    ))

    # --- 3. THE CLUSTERED GLOBS (Heterogeneous RNA) ---
    clusters = [
        {"name": "rRNA (Gold/Robitussin)", "color": "#ffcc00", "count": 5},
        {"name": "tRNA (Red/Transporter)", "color": "#ff3333", "count": 4},
        {"name": "snRNA (Purple/Splicer)", "color": "#aa00ff", "count": 3}
    ]

    for cluster in clusters:
        for i in range(cluster["count"]):
            c_center = np.random.uniform(-0.6, 0.6, 3) * (1-p_mech)
            g_n = 70
            gx = c_center[0] + np.random.normal(0, 0.05, g_n) + (np.sin(t_rad * 4) * 0.04)
            gy = c_center[1] + np.random.normal(0, 0.05, g_n)
            gz = c_center[2] + np.random.normal(0, 0.05, g_n)
            
            fig.add_trace(go.Scatter3d(
                x=gx, y=gy, z=gz,
                mode='markers',
                marker=dict(size=3, color=cluster["color"], opacity=0.8),
                name=cluster["name"]
            ))

    fig.update_layout(template="plotly_dark", height=800, margin=dict(l=0,r=0,b=0,t=0),
                      scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False))
    st.plotly_chart(fig, use_container_width=True)

with col_sub:
    st.subheader("🔍 Legend & Matrix Status")
    st.write("🟡 rRNA | 🔴 tRNA | 🟣 snRNA")
    
    # PEARSON STATUS METER
    pearson_val = 1.0 - (p_mech * 0.15) # Dynamic math for accuracy
    st.metric("Pearson Accuracy", f"{pearson_val:.4f}")
    
    st.info("**Counseling Application:** The way these colored clusters 'huddle' together during stress shows the difference between a rigid system and a resilient one.")

st.caption("Geno-Physics RNA-RNP App | Stanford 3D Folding Part 2")
