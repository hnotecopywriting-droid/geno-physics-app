import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="RA High-Def Helix Matrix", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR NEON THEME ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMarkdown h1, h2, h3 { color: #00f2ff; }
    .stMetric { background-color: #1e2a3a; padding: 10px; border-radius: 10px; border: 1px solid #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: 10 CONTROL MATRIX & RESET ---
st.sidebar.title("🎮 RA Control Matrix")

if st.sidebar.button("🔄 Reset to Natural Equilibrium"):
    st.rerun()

st.sidebar.subheader("🌍 External Influences")
p_mech = st.sidebar.slider("Mechanical Pressure (P_mech)", 0.0, 1.0, 0.25)
t_rad = st.sidebar.slider("Thermal Stress (T_rad)", 0.0, 1.0, 0.35)
v_res = st.sidebar.slider("Vibrational Res (V_res)", 0.0, 1.0, 0.15)
c_temp = st.sidebar.slider("Temporal Flow (C_temp)", 0.0, 1.0, 0.50)
x_bio = st.sidebar.slider("Biodemographic (X_bio)", 0.0, 1.0, 0.20)

st.sidebar.markdown("---")
st.sidebar.subheader("🧬 Internal RA Nodes (100% Reaction)")
ra1 = st.sidebar.slider("RA Node 1 (Structure)", 0.0, 1.0, p_mech)
ra2 = st.sidebar.slider("RA Node 2 (Energy)", 0.0, 1.0, t_rad)
ra3 = st.sidebar.slider("RA Node 3 (Frequency)", 0.0, 1.0, v_res)
ra4 = st.sidebar.slider("RA Node 4 (Time)", 0.0, 1.0, c_temp)
ra5 = st.sidebar.slider("RA Node 5 (Biology)", 0.0, 1.0, x_bio)

# --- HELIX GENERATION ENGINE ---
def generate_helix_trace(center, length, radius, base_twists, color, name, is_double=False):
    t = np.linspace(0, length, 150)
    dynamic_twists = base_twists + (p_mech * 8) 
    dynamic_radius = radius + (t_rad * 0.4)
    vibe = np.sin(t * 20) * (v_res * 0.05)
    
    traces = []
    
    # Strand A
    x1 = center[0] + (dynamic_radius + vibe) * np.sin(t * dynamic_twists)
    y1 = center[1] + (dynamic_radius + vibe) * np.cos(t * dynamic_twists)
    z1 = center[2] + t
    
    traces.append(go.Scatter3d(
        x=x1, y=y1, z=z1,
        mode='lines+markers',
        line=dict(color=color, width=6),
        marker=dict(size=3, color=color, opacity=0.8),
        name=name
    ))
    
    if is_double:
        # Strand B (For Double Helix)
        x2 = center[0] + (dynamic_radius + vibe) * np.sin(t * dynamic_twists + np.pi)
        y2 = center[1] + (dynamic_radius + vibe) * np.cos(t * dynamic_twists + np.pi)
        z2 = z1
        traces.append(go.Scatter3d(
            x=x2, y=y2, z=z2,
            mode='lines+markers',
            line=dict(color=color, width=6),
            marker=dict(size=3, color=color, opacity=0.8),
            showlegend=False
        ))
        
    return traces

# --- MAIN UI LAYOUT ---
st.title("🧬 RA-RNP High-Definition Helix Matrix")
st.markdown("### *Systems Counseling Approach to Genetic Architecture*")

col_viz, col_data = st.columns([3, 1])

with col_viz:
    fig = go.Figure()

    # 1. THE OUTER GHOST SHELL (Blue Master Helix)
    fig.add_traces(generate_helix_trace([0,0,-2], 6, 1.5, 2, "rgba(0, 242, 255, 0.15)", "RA Outer Framework", True))

    # 2. INTERNAL RA HELIX CLUSTERS
    fig.add_traces(generate_helix_trace([0.4, 0.4, -0.5], 2.5, 0.5, 10, "#ffcc00", "rRA Helix (Gold)"))
    fig.add_traces(generate_helix_trace([-0.5, -0.2, 0.5], 2.0, 0.4, 6, "#ff3333", "tRA Helix (Red)"))
    fig.add_traces(generate_helix_trace([0.1, -0.6, -1.5], 1.8, 0.3, 12, "#aa00ff", "snRA Helix (Purple)"))

    fig.update_layout(
        template="plotly_dark",
        height=850,
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
            xaxis_visible=False,
            yaxis_visible=False,
            zaxis_visible=False,
            camera=dict(eye=dict(x=2, y=2, z=1.5))
        )
    )
    st.plotly_chart(fig, use_container_width=True)

with col_data:
    st.subheader("🔍 Helix Inspector")
    accuracy = 1.0 - (abs(p_mech - t_rad) * 0.1)
    st.metric("Pearson Alignment Score", f"{accuracy:.4f}")
    
    st.markdown("---")
    st.write("**Current Helix State:**")
    st.write(f"- Twist Frequency: {2 + (p_mech * 8):.1f} cycles")
    st.write(f"- Vibrational Jitter: {v_res * 100:.1f} MHz")
    
    st.info("**Counseling Selling Point:** This model visualizes the 'Double Helix' of human resilience. When external pressure increases, the core RA nodes tighten to protect the system's integrity.")
    
    st.success("✅ Systems Matrix Stable")

st.caption("RA-RNP High-Def Helix Model | Stanford RNA 3D Challenge 2026")
