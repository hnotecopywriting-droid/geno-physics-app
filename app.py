import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Geno-Physics RNA Lab")

# --- UI STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1e2130; border-radius: 10px; padding: 10px; }
    h1 { color: #87CEEB; } /* Sky Blue for the title */
    h2 { color: #ADD8E6; } /* Light Blue for subheaders */
    .stSlider > div > div {
        background-color: #4CAF50; /* Green slider fill */
    }
    .stSlider > div > div > div > div {
        background-color: #A0C49D; /* Lighter green thumb */
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔬 RNA RA Vector Research Terminal")
st.write("Interacting with the Physical and Non-Physical interface of the Genome.")
st.write("Visualizing how external energies (RA Nodes) influence the RNA structure.")

# --- SIDEBAR: THE 5 VECTORS (RA Nodes) ---
with st.sidebar:
    st.header("🧬 Receptor-Antennae (RA) Node Controls")
    st.write("Adjust the sliders to simulate environmental and internal influences on the RNA.")

    # Renamed sliders to reflect user's conceptual influences
    v1_conscience = st.slider('V1: Conscience (Awake/Asleep) - Structural Decay', 0.0, 10.0, 2.0)
    v2_gravity = st.slider('V2: Gravity/Inertia (Radial Force) - Expansion', 0.5, 4.0, 2.0)
    v3_pressure = st.slider('V3: Pressure/Weight (Ionic Pull) - Sway', -5.0, 5.0, 0.0)
    v4_temp = st.slider('V4: Temperature (Day/Night Frequency) - Vibration', 0.1, 5.0, 1.0)
    v5_optic = st.slider('V5: Optic (Near/Far Impact) - Critical Damage', 0.0, 10.0, 1.0)
    
    st.divider()
    st.info("Cause & Effect Logic: High Optic Impact + High Conscience leads to Fragmentation.")

# --- 3D MODEL ENGINE ---
def generate_3d_model(v1, v2, v3, v4, v5):
    z = np.linspace(0, 20, 200)
    theta = v4 * z
    
    # Core Strands with 'Cause and Effect' displacement
    # V5 (Optic Impact) adds randomness to the strands and enhances highlighting
    noise = np.random.normal(0, v5 * 0.07, 200) # Increased noise for more visible impact
    
    x1 = (v2 * np.cos(theta)) + v3 + noise
    y1 = (v2 * np.sin(theta)) + noise
    x2 = (v2 * np.cos(theta + np.pi)) + v3 + noise
    y2 = (v2 * np.sin(theta + np.pi)) + noise

    fig = go.Figure()

    # 1. DRAW BACKBONE (RNA Highlighted)
    # Highlight RNA more prominently based on Optic Impact (V5)
    rna_line_width = 8 + (v5 * 0.5) # Thicker line based on V5
    rna_base_color = 'rgb(0, 255, 255)' # Cyan base
    rna_stressed_color = 'rgb(255, 69, 0)' # Orange-red for stress
    rna_color = rna_stressed_color if v5 > 7 or v1 > 7 else rna_base_color
    
    fig.add_trace(go.Scatter3d(x=x1, y=y1, z=z, mode='lines', line=dict(color=rna_color, width=rna_line_width), name='RNA Strand 1'))
    fig.add_trace(go.Scatter3d(x=x2, y=y2, z=z, mode='lines', line=dict(color=rna_color, width=rna_line_width), name='RNA Strand 2'))

    # 2. DRAW CENTRAL RUNGS (Physical Ladder) - connect the two main strands
    for i in range(0, len(z), 10):
        fig.add_trace(go.Scatter3d(
            x=[x1[i], x2[i]], y=[y1[i], y2[i]], z=[z[i], z[i]],
            mode='lines', line=dict(color='white', width=2, dash='dot'), showlegend=False
        ))

    # 3. DRAW SENSORY HAIRS (RA Nodes) - more prominent and responsive
    # Hairs change length based on Gravity/Inertia (V2) and Sway based on Pressure/Weight (V3)
    # V5 (Optic Impact) also increases their reach, and V1 (Conscience) affects color
    
    for i in range(0, len(z), 8):
        # Calculate hair tip (RA Node endpoint)
        # Increased base reach and multiplier for V5 (Optic)
        reach_multiplier = 1.5 + (v2 * 0.2) + (v5 * 0.08)
        
        # Sway based on V3 (Pressure/Weight)
        sway_factor = v3 * 0.3
        
        tx = x1[i] * reach_multiplier + sway_factor
        ty = y1[i] * reach_multiplier
        
        # Color logic for pathology, now more tied to Conscience (V1) and Optic Impact (V5)
        # Hairs glow red when critical conditions, otherwise a vibrant green/yellow
        hair_color_critical = 'red' if v5 > 6 or v1 > 7 else 'rgba(50, 255, 50, 0.8)' # Vibrant green
        
        fig.add_trace(go.Scatter3d(
            x=[x1[i], tx], y=[y1[i], ty], z=[z[i], z[i]],
            mode='lines', line=dict(color=hair_color_critical, width=4), # Thicker hairs
            showlegend=False
        ))
        # Add a sphere at the tip of each hair to represent the 'RA Node'
        fig.add_trace(go.Scatter3d(
            x=[tx], y=[ty], z=[z[i]],
            mode='markers',
            marker=dict(size=4 + v5*0.5, color=hair_color_critical, opacity=0.8), # Size based on V5
            showlegend=False
        ))


    # 4. THE CONTAINMENT CYLINDER (Visualizing the 'Vault')
    u = np.linspace(0, 2*np.pi, 50)
    z_cyl = np.linspace(-2, 22, 50)
    U, Z_cyl = np.meshgrid(u, z_cyl)
    X_cyl = 10 * np.cos(U)
    Y_cyl = 10 * np.sin(U)
    fig.add_trace(go.Surface(x=X_cyl, y=Y_cyl, z=Z_cyl, opacity=0.08, colorscale='Blues', showscale=False))

    # Layout Customization
    fig.update_layout(
        scene=dict(
            xaxis_visible=False, yaxis_visible=False, zaxis_visible=False,
            bgcolor='rgb(10, 10, 20)' # Darker background
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        template="plotly_dark",
        height=700 # Make the chart a bit taller
    )
    return fig

# --- DISPLAY OUTPUT ---
col_map, col_data = st.columns([3, 1])

with col_map:
    # Pass the new slider values to the model generation
    model_fig = generate_3d_model(v1_conscience, v2_gravity, v3_pressure, v4_temp, v5_optic)
    st.plotly_chart(model_fig, use_container_width=True)

with col_data:
    st.subheader("System Status: RNA Vitality")
    # Update stress calculation based on new vector names
    stress = (v1_conscience + v5_optic) / 2
    if stress > 7:
        st.error("🚨 CRITICAL FRACTURE")
        st.write("High Optic Impact & Conscience: RNA Fragmentation imminent.")
    elif stress > 4:
        st.warning("⚠️ RESONANCE DISTURBANCE")
        st.write("Forces are weakening RNA stability.")
    else:
        st.success("✅ HARMONIC STABILITY")
        st.write("RNA structure is resilient.")
        
    st.metric("Integrity Index", f"{stress * 10:.1f}%")
    st.metric("Helix Dynamics (Temperature Influence)", f"{v4_temp:.1f} Hz")
    st.metric("Gravitational Adherence", f"{v2_gravity:.1f} Units")
