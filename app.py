import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Geno-Physics RNA Lab")

# --- UI STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    stMetric { background-color: #1e2130; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔬 RNA RA Vector Research Terminal")
st.write("Interacting with the Physical and Non-Physical interface of the Genome.")

# --- SIDEBAR: THE 5 VECTORS ---
with st.sidebar:
    st.header("🧬 Vector Control Interface")
    v1_tox = st.slider('V1: Toxicity Load (Structural Decay)', 0.0, 10.0, 2.0)
    v2_rad = st.slider('V2: Radial Expansion (Gravity)', 0.5, 4.0, 2.0)
    v3_ph = st.slider('V3: pH / Ionic Charge Pull', -5.0, 5.0, 0.0)
    v4_freq = st.slider('V4: Frequency / Vibration', 0.1, 5.0, 1.0)
    v5_impact = st.slider('V5: Critical Damage (Mutation)', 0.0, 10.0, 1.0)
    
    st.divider()
    st.info("Cause & Effect Logic: High V5 + High V1 triggers Fragmentation.")

# --- 3D MODEL ENGINE ---
def generate_3d_model(v1, v2, v3, v4, v5):
    z = np.linspace(0, 20, 200)
    theta = v4 * z
    
    # Core Strands with 'Cause and Effect' displacement
    # V5 (Impact) adds randomness to the strands
    noise = np.random.normal(0, v5 * 0.05, 200)
    
    x1 = (v2 * np.cos(theta)) + v3 + noise
    y1 = (v2 * np.sin(theta)) + noise
    x2 = (v2 * np.cos(theta + np.pi)) + v3 + noise
    y2 = (v2 * np.sin(theta + np.pi)) + noise

    fig = go.Figure()

    # 1. DRAW BACKBONE (Cause: V5 Impact)
    line_color = 'rgb(255, 0, 0)' if v5 > 7 else 'rgb(0, 255, 255)'
    fig.add_trace(go.Scatter3d(x=x1, y=y1, z=z, mode='lines', line=dict(color=line_color, width=6)))
    fig.add_trace(go.Scatter3d(x=x2, y=y2, z=z, mode='lines', line=dict(color=line_color, width=6)))

    # 2. DRAW CENTRAL RUNGS (Physical Ladder)
    for i in range(0, len(z), 10):
        fig.add_trace(go.Scatter3d(
            x=[x1[i], x2[i]], y=[y1[i], y2[i]], z=[z[i], z[i]],
            mode='lines', line=dict(color='white', width=2, dash='dot'), showlegend=False
        ))

    # 3. DRAW SENSORY HAIRS (Effect: Environmental Reaction)
    # Hairs change length based on V2 and Sway based on V3
    for i in range(0, len(z), 8):
        # Hair Tip calculation
        reach = 1.2 + (v5 * 0.1)
        tx = x1[i] * reach + (v3 * 0.5)
        ty = y1[i] * reach
        
        # Color logic for pathology
        h_color = 'red' if v5 > 6 or v1 > 7 else 'rgba(0, 255, 150, 0.6)'
        
        fig.add_trace(go.Scatter3d(
            x=[x1[i], tx], y=[y1[i], ty], z=[z[i], z[i]],
            mode='lines', line=dict(color=h_color, width=3), showlegend=False
        ))

    # 4. THE CONTAINMENT CYLINDER (Visualizing the 'Vault')
    u = np.linspace(0, 2*np.pi, 50)
    z_cyl = np.linspace(-2, 22, 50)
    U, Z_cyl = np.meshgrid(u, z_cyl)
    X_cyl = 10 * np.cos(U)
    Y_cyl = 10 * np.sin(U)
    fig.add_trace(go.Surface(x=X_cyl, y=Y_cyl, z=Z_cyl, opacity=0.1, colorscale='Blues', showscale=False))

    # Layout Customization
    fig.update_layout(
        scene=dict(
            xaxis_visible=False, yaxis_visible=False, zaxis_visible=False,
            bgcolor='rgb(10, 10, 20)'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        template="plotly_dark"
    )
    return fig

# --- DISPLAY OUTPUT ---
col_map, col_data = st.columns([3, 1])

with col_map:
    model_fig = generate_3d_model(v1_tox, v2_rad, v3_ph, v4_freq, v5_impact)
    st.plotly_chart(model_fig, use_container_width=True)

with col_data:
    st.subheader("System Status")
    stress = (v1_tox + v5_impact) / 2
    if stress > 7:
        st.error("🔴 CRITICAL DAMAGE")
        st.write("Pathology: Mutation likely.")
    elif stress > 4:
        st.warning("🟡 STRESSED")
        st.write("Pathology: Bond Weakening.")
    else:
        st.success("🟢 STABLE")
        st.write("Pathology: Homeostasis.")
        
    st.metric("Tension Index", f"{stress * 10}%")
    st.metric("Helix Twist", f"{v4_freq} rads")
