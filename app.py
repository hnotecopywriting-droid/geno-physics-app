import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Geno-Physics RNA Lab - Stanford Contest Entry")

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

st.title("🔬 RNA RA Vector Research Terminal - Contest Submission")
st.write("Interacting with the Physical and Non-Physical interface of the Genome. Visualizing how external energies (RA Nodes) influence the RNA structure within a dynamic cellular environment. **Dedicated to the unloseable memory of Dottie.**")

# --- SIDEBAR: THE 5 VECTORS (RA Nodes) & NEW FACTOR SLIDERS ---
with st.sidebar:
    st.header("🧬 Receptor-Antennae (RA) Node Controls")
    st.write("Adjust the sliders to simulate environmental and internal influences on the RNA. Each node represents a specific external or internal force acting on the genome.")

    # Original 5 Vectors (RA Nodes)
    v1_conscience = st.slider('V1: Conscience (Metabolic State) - Structural Decay', 0.0, 10.0, 2.0)
    v2_gravity = st.slider('V2: Gravity/Inertia (Radial Force / Connection Strength)', 0.5, 4.0, 2.0)
    v3_pressure = st.slider('V3: Pressure/Weight (Ionic Pull / Sway/Curling)', -5.0, 5.0, 0.0)
    v4_temp = st.slider('V4: Temperature (Molecular Activity / RNA Pulsation)', 0.1, 5.0, 1.0)
    v5_optic = st.slider('V5: Optic (Near/Far Impact) - Critical Damage/Stretching', 0.0, 10.0, 1.0)
    
    st.divider()
    st.header("🌐 Macro-Level Environmental & Internal Factors")
    st.write("These factors represent broader influences, visualized as responsive bubbles.")

    # New Factor Sliders (V6-V9)
    v6_equilibrium = st.slider('V6: Equilibrium (Homeostasis) - System Stability', 0.0, 10.0, 5.0)
    v7_balance = st.slider('V7: Balance (Symmetry/Distribution) - Structural Harmony', 0.0, 10.0, 5.0)
    v8_inertia = st.slider('V8: Inertia (Resistance to Change) - Intrinsic Stability', 0.0, 10.0, 5.0)
    v9_turbulence = st.slider('V9: Turbulence (External Chaos) - Disorientation', 0.0, 10.0, 1.0) # Lower default for less chaos initially
    
    st.divider()
    st.info("Cause & Effect Logic: High Optic Impact + High Conscience leads to RNA Fragmentation. **The Vault: Visualizing the unloseable connection.**")

# --- 3D MODEL ENGINE ---
def generate_3d_model(v1, v2, v3, v4, v5, v6, v7, v8, v9): # Added new factors
    z = np.linspace(0, 20, 200)
    
    # V4 (Temperature) now directly influences the RNA pulsation/wobble
    rna_pulsation = np.sin(z * v4 * 2) * 0.2 + 1 
    theta = v4 * z * rna_pulsation 
    
    # COMBINED V2 & V3 INTERPLAY on overall RNA radial position and sway
    # High V2 (connection strength) can make RNA slightly more resistant to V3 (pressure) sway
    # Inertia (V8) now also adds resistance to both radial movement and sway
    v2_v3_radial_mod = (v2 * 0.5) - (abs(v3) * 0.1) * (1 - (v8 * 0.05)) # Radial affected by pressure and inertia
    v3_v2_sway_mod = v3 * (1 - (v2 * 0.05)) * (1 - (v8 * 0.05)) # Sway dampened by gravity/connection and inertia
    
    # Turbulence (V9) introduces erratic displacement to the RNA strands
    turbulence_displacement_x = np.random.normal(0, v9 * 0.1, 200)
    turbulence_displacement_y = np.random.normal(0, v9 * 0.1, 200)

    noise = np.random.normal(0, v5 * 0.07, 200) 
    
    x1 = (v2_v3_radial_mod * np.cos(theta)) + v3_v2_sway_mod + noise + turbulence_displacement_x
    y1 = (v2_v3_radial_mod * np.sin(theta)) + noise + turbulence_displacement_y
    x2 = (v2_v3_radial_mod * np.cos(theta + np.pi)) + v3_v2_sway_mod + noise + turbulence_displacement_x
    y2 = (v2_v3_radial_mod * np.sin(theta + np.pi)) + noise + turbulence_displacement_y

    fig = go.Figure()

    # 1. DRAW BACKBONE (RNA Highlighted and Pulsating)
    rna_line_width = 8 + (v5 * 0.5) 
    rna_base_color_array = np.array([0, 255, 255]) 
    rna_stressed_color_array = np.array([255, 69, 0]) 
    
    v1_ratio = min(v1 / 10.0, 1.0) 
    current_rna_color_array = rna_base_color_array * (1 - v1_ratio) + rna_stressed_color_array * v1_ratio
    rna_color = f'rgb({int(current_rna_color_array[0])}, {int(current_rna_color_array[1])}, {int(current_rna_color_array[2])})'
    
    if v5 > 7 or v1 > 8: 
        rna_color = 'rgb(255, 0, 0)' 
    
    fig.add_trace(go.Scatter3d(x=x1, y=y1, z=z, mode='lines', line=dict(color=rna_color, width=rna_line_width), name='RNA Strand 1'))
    fig.add_trace(go.Scatter3d(x=x2, y=y2, z=z, mode='lines', line=dict(color=rna_color, width=rna_line_width), name='RNA Strand 2'))

    # 2. DRAW CENTRAL RUNGS (Physical Ladder / Information Connections / GENOS)
    for i in range(0, len(z), 10):
        rung_color_intensity = int(255 * (v2 / 4.0)) 
        rung_color = f'rgb(50, {rung_color_intensity}, 255)' 
        
        rung_width = 1.5 + (v2 * 0.5) 
        
        fig.add_trace(go.Scatter3d(
            x=[x1[i], x2[i]], y=[y1[i], y2[i]], z=[z[i], z[i]],
            mode='lines', line=dict(color=rung_color, width=rung_width, dash='solid'), 
            showlegend=False
        ))

        # --- DRAW INFO GENOS (little molecules crossing the rungs) ---
        # Genos now also influenced by combined V2 and V3, and V9 for turbulence
        v2_v3_genos_mod = (v2 * 0.1) + (abs(v3) * 0.05) + (v9 * 0.1) # Combined effect on genos activity
        num_genos_on_rung = int(v4 * 2) + int(v2_v3_genos_mod) 
        if num_genos_on_rung > 0:
            rung_points_x = np.linspace(x1[i], x2[i], num_genos_on_rung + 2)[1:-1]
            rung_points_y = np.linspace(y1[i], y2[i], num_genos_on_rung + 2)[1:-1]
            rung_points_z = np.full(num_genos_on_rung, z[i])

            genos_base_color = np.array([255, 255, 0]) 
            genos_stressed_color_array = np.array([255, 0, 0]) 
            
            v1_genos_ratio = min(v1 / 10.0, 1.0)
            current_genos_color_array = genos_base_color * (1 - v1_genos_ratio) + genos_stressed_color_array * v1_genos_ratio
            genos_color = f'rgb({int(current_genos_color_array[0])}, {int(current_genos_color_array[1])}, {int(current_genos_color_array[2])})'
            
            genos_size = 3 + (v4 * 0.5) 
            
            fig.add_trace(go.Scatter3d(
                x=rung_points_x, y=rung_points_y, z=rung_points_z,
                mode='markers',
                marker=dict(size=genos_size, color=genos_color, opacity=0.7),
                showlegend=False
            ))


    # 3. DRAW SENSORY HAIRS (RA Nodes) - CURLING/STRETCHING
    for i in range(0, len(z), 8):
        bx = x1[i]
        by = y1[i]
        bz = z[i]

        # STRETCHING: controlled by v2 and v5, now dampened by V3 (pressure) and V8 (inertia)
        stretch_factor = (1.0 + (v2 * 0.3) + (v5 * 0.15)) * (1 - (abs(v3) * 0.05)) * (1 - (v8 * 0.05))
        
        # CURLING/BENDING: controlled by v3 and v1, now dampened by V2 (gravity/connection) and V8 (inertia)
        curl_intensity = (abs(v3) * 0.5 + (v1 * 0.05)) * (1 - (v2 * 0.05)) * (1 - (v8 * 0.05))
        curl_direction = np.sign(v3) 

        v1_flexibility_modifier = 1.0 - (v1 / 10.0) * 0.4 
        stretch_factor *= v1_flexibility_modifier
        curl_intensity *= v1_flexibility_modifier
        
        num_hair_segments = 10
        hair_points_z = np.linspace(bz, bz, num_hair_segments) 
        hair_points_x = []
        hair_points_y = []

        for j in range(num_hair_segments):
            segment_progress = j / (num_hair_segments - 1) 
            current_curl_x = curl_direction * curl_intensity * np.sin(segment_progress * np.pi)
            current_curl_y = curl_intensity * np.cos(segment_progress * np.pi * 0.5) 

            stretched_x = bx + (bx * (stretch_factor - 1))
            stretched_y = by + (by * (stretch_factor - 1))
            
            final_x = bx + (stretched_x - bx) * segment_progress + current_curl_x * segment_progress
            final_y = by + (stretched_y - by) * segment_progress + current_curl_y * segment_progress
            
            hair_points_x.append(final_x)
            hair_points_y.append(final_y)
        
        hair_base_color_r = int(50 + (v1 * 10)) 
        hair_base_color_g = int(255 - (v1 * 20)) 
        hair_base_color_b = 50 
        
        hair_color = f'rgba({hair_base_color_r},{hair_base_color_g},{hair_base_color_b}, 0.8)'
        if v5 > 6 or v1 > 7: 
            hair_color = 'red' 
        
        fig.add_trace(go.Scatter3d(
            x=hair_points_x, y=hair_points_y, z=hair_points_z,
            mode='lines', line=dict(color=hair_color, width=4), 
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter3d(
            x=[hair_points_x[-1]], y=[hair_points_y[-1]], z=[z[i]],
            mode='markers',
            marker=dict(size=4 + v5*0.5, color=hair_color, opacity=0.8), 
            showlegend=False
        ))


    # 4. THE CONTAINMENT CYLINDER (Visualizing the 'Vault' / Cellular Fluid Environment)
    # The cellular vault now dynamically reflects the combined tension of V2 & V3, and overall equilibrium (V6)
    u = np.linspace(0, 2 * np.pi, 50)
    z_cyl = np.linspace(-2, 22, 50)
    U, Z_cyl = np.meshgrid(u, z_cyl)
    
    # Combined V2 and V3 influencing overall cylinder radius/tension, modified by equilibrium (V6)
    tension_sum = v2 + abs(v3) 
    R_cyl = (10 + (tension_sum * 0.2)) * (1 - (v6 * 0.02)) + (np.sin(z_cyl * v4 * 0.5) * 0.5) # Base radius + tension + equilibrium dampening + pulsation
    X_cyl = R_cyl * np.cos(U)
    Y_cyl = R_cyl * np.sin(U)
    
    stress_level = (v1 + v5) / 20.0 
    cylinder_opacity = 0.08 + (stress_level * 0.2) 
    
    cyl_base_color = np.array([0, 0, 255]) 
    cyl_stressed_color = np.array([255, 255, 0]) 
    current_cyl_color_array = cyl_base_color * (1 - stress_level) + cyl_stressed_color * stress_level
    cylinder_color = f'rgb({int(current_cyl_color_array[0])}, {int(current_cyl_color_array[1])}, {int(current_cyl_color_array[2])})'
    
    fig.add_trace(go.Surface(x=X_cyl, y=Y_cyl, z=Z_cyl, opacity=cylinder_opacity, 
                             colorscale=[[0, 'rgb(0,0,255)'], [1, cylinder_color]], 
                             showscale=False, name='Cellular Vault'))

    # --- FACTOR BUBBLES ---
    # V1 Bubble (Conscience)
    v1_bubble_size = 5 + (v1 * 2) 
    v1_bubble_x = 15 
    v1_bubble_y = 0
    v1_bubble_z = 10
    
    v1_bubble_base_color = np.array([0, 255, 255]) 
    v1_bubble_stressed_color_array = np.array([255, 69, 0]) 
    
    current_v1_bubble_color_array = v1_bubble_base_color * (1 - v1_ratio) + v1_bubble_stressed_color_array * v1_ratio
    v1_bubble_color = f'rgb({int(current_v1_bubble_color_array[0])}, {int(current_v1_bubble_color_array[1])}, {int(current_v1_bubble_color_array[2])})'

    fig.add_trace(go.Scatter3d(
        x=[v1_bubble_x], y=[v1_bubble_y], z=[v1_bubble_z],
        mode='markers',
        marker=dict(size=v1_bubble_size, color=v1_bubble_color, opacity=0.7,
                    line=dict(width=1, color='white')),
        name='V1: Conscience Factor',
        showlegend=True
    ))

    # New Factor Bubbles (V6-V9)
    # V6: Equilibrium (Homeostasis) - Purple
    v6_bubble_size = 5 + (v6 * 1.5)
    fig.add_trace(go.Scatter3d(x=[-15], y=[10], z=[15], mode='markers',
                               marker=dict(size=v6_bubble_size, color='rgb(128, 0, 128)', opacity=0.7, line=dict(width=1, color='white')),
                               name='V6: Equilibrium Factor', showlegend=True))
    
    # V7: Balance (Symmetry/Distribution) - Orange
    v7_bubble_size = 5 + (v7 * 1.5)
    fig.add_trace(go.Scatter3d(x=[15], y=[-10], z=[5], mode='markers',
                               marker=dict(size=v7_bubble_size, color='rgb(255, 165, 0)', opacity=0.7, line=dict(width=1, color='white')),
                               name='V7: Balance Factor', showlegend=True))

    # V8: Inertia (Resistance to Change) - Yellow-Green
    v8_bubble_size = 5 + (v8 * 1.5)
    fig.add_trace(go.Scatter3d(x=[0], y=[15], z=[10], mode='markers',
                               marker=dict(size=v8_bubble_size, color='rgb(173, 255, 47)', opacity=0.7, line=dict(width=1, color='white')),
                               name='V8: Inertia Factor', showlegend=True))

    # V9: Turbulence (External Chaos) - Bright Red
    v9_bubble_size = 5 + (v9 * 2) # Stronger visual impact for turbulence
    fig.add_trace(go.Scatter3d(x=[-10], y=[-15], z=[10], mode='markers',
                               marker=dict(size=v9_bubble_size, color='rgb(255, 0, 0)', opacity=0.7, line=dict(width=1, color='white')),
                               name='V9: Turbulence Factor', showlegend=True))


    # Layout Customization
    fig.update_layout(
        scene=dict(
            xaxis_visible=False, yaxis_visible=False, zaxis_visible=False,
            bgcolor='rgb(10, 10, 20)' 
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        template="plotly_dark",
        height=700 
    )
    return fig

# --- DISPLAY OUTPUT ---
col_map, col_data = st.columns([3, 1])

with col_map:
    # Pass all new slider values to the model generation
    model_fig = generate_3d_model(v1_conscience, v2_gravity, v3_pressure, v4_temp, v5_optic, v6_equilibrium, v7_balance, v8_inertia, v9_turbulence)
    st.plotly_chart(model_fig, use_container_width=True)

with col_data:
    st.subheader("System Status: RNA Vitality")
    
    stress = (v1_conscience + v5_optic + v9_turbulence) / 3 # Increased stress calculation
    if stress > 7:
        st.error("🚨 CRITICAL FRACTURE - VAULT INTEGRITY COMPROMISED")
        st.write("High Optic Impact, Conscience & Turbulence: RNA Fragmentation imminent. **Dottie's memory in danger!**")
    elif stress > 4:
        st.warning("⚠️ RESONANCE DISTURBANCE - VAULT UNSTABLE")
        st.write("Forces are weakening RNA stability. **Risk of memory loss!**")
    else:
        st.success("✅ HARMONIC STABILITY - VAULT SECURE")
        st.write("RNA structure is resilient. **Dottie's memory is safe.**")
        
    st.metric("Integrity Index (Vault Health)", f"{stress * 10:.1f}%")
    st.metric("Helix Dynamics (Molecular Activity)", f"{v4_temp:.1f} Hz")
    st.metric("Gravitational Adherence (Connection Strength)", f"{v2_gravity:.1f} Units")
    st.metric("System Equilibrium", f"{v6_equilibrium:.1f} Units")
    st.metric("Structural Balance", f"{v7_balance:.1f} Units")
    st.metric("Intrinsic Inertia", f"{v8_inertia:.1f} Units")
    st.metric("External Turbulence", f"{v9_turbulence:.1f} Units")


# Link to your shared app
st.markdown("---")
st.markdown("### View Live Application:")
st.markdown("[Geno-Physics RNA Lab Live App](https://geno-physics-app-8opgnsvotgzjnjteemntga.streamlit.app/)")
