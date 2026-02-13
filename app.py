import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="RNA Influence Matrix", layout="wide")

st.title("🧬 RNA-RNP 175,000 Influence Matrix")
st.markdown("### *Systems Counseling Approach to RNA Folding Architecture*")

# --- SIDEBAR: THE 10-SLIDER SYSTEM ---
st.sidebar.header("🌍 External Influences (Inputs)")
p_mech = st.sidebar.slider("Mechanical Pressure (P_mech)", 0.0, 1.0, 0.2)
t_rad = st.sidebar.slider("Thermal/Radiative (T_rad)", 0.0, 1.0, 0.3)
v_res = st.sidebar.slider("Vibrational Resonance (V_res)", 0.0, 1.0, 0.1)
c_temp = st.sidebar.slider("Temporal/Circadian (C_temp)", 0.0, 1.0, 0.5)
x_bio = st.sidebar.slider("Biodemographic/Unknown (X_bio)", 0.0, 1.0, 0.1)

st.sidebar.header("🧬 Internal RA Nodes (Responses)")
ra1 = st.sidebar.slider("RA Node 1 (Primary: Pressure)", 0.0, 1.0, 0.0)
ra2 = st.sidebar.slider("RA Node 2 (Primary: Thermal)", 0.0, 1.0, 0.0)
ra3 = st.sidebar.slider("RA Node 3 (Primary: Vibration)", 0.0, 1.0, 0.0)
e1 = st.sidebar.slider("Emergent Node 4", 0.0, 1.0, 0.0)
e2 = st.sidebar.slider("Emergent Node 5", 0.0, 1.0, 0.0)

# --- THE MATH: 100% REACTION RULE ---
# Calculating weighted response based on the "Outer" influences
# Filament 1 is 100% linked to Mechanical Pressure, etc.
weights = {'primary': 1.0, 'secondary': 0.25}

def calculate_response(primary_val, others):
    # R_n = (I_x * 1.0) + Σ(I_other * w)
    return (primary_val * weights['primary']) + (sum(others) * weights['secondary'])

# Updating response values based on matrix logic
res_ra1 = calculate_response(p_mech, [t_rad, v_res, c_temp, x_bio])
res_ra2 = calculate_response(t_rad, [p_mech, v_res, c_temp, x_bio])

# --- GENERATING THE 175k GLOBULE ---
@st.cache_data
def generate_base_globule(n_points=5000): # Using 5k for smooth web rendering, scaling to 175k for final
    # Creating a "Rockefeller" style bunching effect
    t = np.linspace(0, 50, n_points)
    x = t * np.sin(t)
    y = t * np.cos(t)
    z = np.linspace(0, 20, n_points)
    return x, y, z

x_base, y_base, z_base = generate_base_globule()

# Apply the "100% Reaction" to the 3D coordinates (Visual Fold)
# As Pressure (p_mech) increases, the globule "bunches" tighter (multiplied by 1-p_mech)
fold_factor = 1.0 - (p_mech * 0.5)
x_folded = x_base * fold_factor
y_folded = y_base * fold_factor
z_folded = z_base + (t_rad * 10) # Heat makes it "rise" or expand vertically

# --- 3D VISUALIZATION ---
fig = go.Figure(data=[go.Scatter3d(
    x=x_folded, y=y_folded, z=z_folded,
    mode='lines',
    line=dict(
        color=z_folded, # Color changes based on "energy/thermal" height
        colorscale='Viridis',
        width=4
    )
)])

fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=0),
    scene=dict(
        xaxis_title='Spatial X',
        yaxis_title='Spatial Y',
        zaxis_title='Dimensional Fold (Z)'
    ),
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# --- COUNSELING INSIGHT PANEL ---
st.info(f"**Counseling Insight:** The current structural alignment shows a reaction intensity of {res_ra1:.2f} to external pressure. This represents a highly adaptive state.")
