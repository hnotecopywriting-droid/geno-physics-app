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

# --- MAIN LAYOUT ---
st.title("🧬 RA-RNP 175,000 Bonded Matrix")
st.markdown("### *Systems Counseling Approach to Bonded RA Protein Strains*")

col_main, col_sub = st.columns([2, 1])

with col_main:
    fig = go.Figure()

    # --- 1. THE OUTER SHELL (mRNA Filaments) ---
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
        line=dict(color='#00f2ff', width=1), 
        opacity=0.1,
        name="Outer RA Shell"
    ))

    # --- 2. THE BONDED RA CLUSTERS (The 'Strains') ---
    clusters = [
        {"name": "rRA Strains (Gold)", "color": "#ffcc00", "count": 6},
        {"name": "tRA Strains (Red)", "color": "#ff3333", "count": 4},
        {"name": "snRA Strains (Purple)", "color": "#aa00ff", "count": 3}
    ]

    for cluster in clusters:
        for i in range(cluster["count"]):
            # Center of the cluster
            c_center = np.random.uniform(-0.4, 0.4, 3) * (1.2 - p_mech)
            
            # Create a "Strain" by connecting points in a sequence rather than random dots
            g_pts = 60
            # Sort points or use a random walk to create a "stringy" look
            t = np.linspace(0, 1, g_pts)
            gx = c_center[0] + np.cumsum(np.random.normal(0, 0.04, g_pts)) + (np.sin(t_rad * 5) * 0.05)
            gy = c_center[1] + np.cumsum(np.random.normal(0, 0.04, g_pts))
            gz = c_center[2] + np.cumsum(np.random.normal(0, 0.04, g_pts))
            
            # Mode set to 'lines+markers' to see both the bonders and the points
            fig.add_trace(go.Scatter3d(
                x=gx, y=gy, z=gz,
                mode='lines+markers',
                line=dict(color=cluster["color"], width=3),
                marker=dict(size=2, color=cluster["color"]),
                opacity=0.8,
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
    st.subheader("🔍 RA Bonder Inspector")
    st.write("The dots are now connected by protein strains, creating the 'stringy' biological reality of the RA model.")
    
    
    
    st.markdown("""
    - 🟡 **rRA Strains:** Ribosomal bonds
    - 🔴 **tRA Strains:** Transfer bonds
    - 🟣 **snRA Strains:** Nuclear splicing bonds
    """)

    intensity = (p_mech * 1.0) + (t_rad * 0.2)
    st.metric("RA Reaction Intensity", f"{intensity:.2%}")
    st.progress(min(intensity, 1.0))
    
    st.info("**Counseling Selling Point:** These bonds (strains) represent the connections we hold onto under pressure. They turn isolated 'dots' of experience into a cohesive structure of resilience.")

st.caption("RA-RNP Bonded Model | Developed for Stanford RNA Challenge")
