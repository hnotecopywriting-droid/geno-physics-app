import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="RA Photo-Real RNP", layout="wide", initial_sidebar_state="expanded")

# --- CLEAN UI ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stMarkdown h1, h2, h3 { color: #1a1a1a; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: 10 PHYSICS SLIDERS ---
st.sidebar.title("🎮 RA Control Matrix")
if st.sidebar.button("🔄 Reset to Equilibrium"):
    st.rerun()

st.sidebar.subheader("🌍 External Forces")
gravity = st.sidebar.slider("Gravity Pull", 0.0, 1.0, 0.20)
weight = st.sidebar.slider("Molecular Weight", 0.1, 2.0, 1.2)
inertia = st.sidebar.slider("Inertia", 0.0, 1.0, 0.3)
t_stress = st.sidebar.slider("Thermal Stress", 0.0, 1.0, 0.4)
p_mech = st.sidebar.slider("Mechanical Pressure", 0.0, 1.0, 0.2)

st.sidebar.subheader("🧬 Internal Nodes")
v_res = st.sidebar.slider("Vibrational Res", 0.0, 1.0, 0.1)
c_temp = st.sidebar.slider("Temporal Flow", 0.0, 1.0, 0.5)
x_bio = st.sidebar.slider("Biodemographic", 0.0, 1.0, 0.2)
density = st.sidebar.slider("Core Density", 0.5, 2.5, 1.5)
tension = st.sidebar.slider("Helix Tension", 0.0, 1.0, 0.5)

# --- PHOTO-REAL ENGINE ---

def generate_solid_helix(center, twists, length, color, radius=0.08):
    """Generates a solid 'Tube' look for the helices."""
    t = np.linspace(0, length, 150)
    # Physics modifiers
    d_twists = twists + (tension * 5)
    
    # Create a tube by wrapping a surface around a path
    x = center[0] + radius * np.sin(t * d_twists)
    y = center[1] + radius * np.cos(t * d_twists)
    z = center[2] + t - (gravity * 1.5)
    
    return go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(color=color, width=12), # Thick width for solid feel
        opacity=1.0,
        name="RA Helix Strand"
    )

def generate_protein_bonds(center, twists, length):
    """Adds those tiny white 'ladder rungs' across the helix."""
    t = np.linspace(0, length, 40)
    d_twists = twists + (tension * 5)
    radius = 0.08
    
    bx, by, bz = [], [], []
    for i in range(len(t)):
        x1 = center[0] + radius * np.sin(t[i] * d_twists)
        y1 = center[1] + radius * np.cos(t[i] * d_twists)
        # Offset for second side
        x2 = center[0] + radius * np.sin(t[i] * d_twists + np.pi/2)
        y2 = center[1] + radius * np.cos(t[i] * d_twists + np.pi/2)
        z = center[2] + t[i] - (gravity * 1.5)
        
        bx.extend([x1, x2, None])
        by.extend([y1, y2, None])
        bz.extend([z, z, None])
        
    return go.Scatter3d(x=bx, y=by, z=bz, mode='lines', 
                        line=dict(color='white', width=3), opacity=0.6, showlegend=False)

def generate_ribosome_body(center, size, color1, color2):
    """Generates a lumpy, two-part protein mass (Large/Small subunits)."""
    # Small Subunit
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:15j]
    x_s = (size*0.7) * np.cos(u) * np.sin(v) + center[0]
    y_s = (size*0.9) * np.sin(u) * np.sin(v) + center[1]
    z_s = (size*0.6) * np.cos(v) + center[2] - 0.3 - (gravity * 0.5)
    
    # Large Subunit (Offset slightly)
    x_l = (size*1.1) * np.cos(u) * np.sin(v) + center[0]
    y_l = (size*1.0) * np.sin(u) * np.sin(v) + center[1]
    z_l = (size*0.8) * np.cos(v) + center[2] + 0.3 - (gravity * 0.5)
    
    return [
        go.Mesh3d(x=x_s.flatten(), y=y_s.flatten(), z=z_s.flatten(), color=color1, opacity=1.0, flatshading=False),
        go.Mesh3d(x=x_l.flatten(), y=y_l.flatten(), z=z_l.flatten(), color=color2, opacity=1.0, flatshading=False)
    ]

# --- RENDER ---
st.title("🧬 RA-RNP Photo-Realistic Molecular Architecture")

fig = go.Figure()

# 1. THE PROTEIN BODY (Orange/Gold Solid Subunits)
# 
fig.add_traces(generate_ribosome_body([0,0,0], 1.2, "#ff8c00", "#cc5500"))

# 2. THE THICK HELICAL STRANDS (Solid Ribbons)
# 
# Purple mRNA
fig.add_trace(generate_solid_helix([0,0,-2.5], 14, 5, "#4b0082"))
fig.add_trace(generate_protein_bonds([0,0,-2.5], 14, 5))

# Red tRNA
fig.add_trace(generate_solid_helix([-0.4, -0.4, -1], 10, 3.5, "#b22222"))
fig.add_trace(generate_protein_bonds([-0.4, -0.4, -1], 10, 3.5))

# 3. OUTER CELL BOUNDARY
# 

[Image of the fluid mosaic model of a cell membrane]

u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
fig.add_trace(go.Mesh3d(
    x=2.5 * np.cos(u).flatten(), y=2.5 * np.sin(u).flatten(), z=(2.5 * np.cos(v).flatten() - gravity),
    color='skyblue', opacity=0.1, name="Cell Boundary"
))

fig.update_layout(
    scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False, aspectmode='cube'),
    height=800, template="plotly_white", margin=dict(l=0, r=0, b=0, t=0)
)

st.plotly_chart(fig, use_container_width=True)

st.info("**Counseling Integration:** This photo-real model visualizes the 'weight' of human experience. The solid ribosome core represents the established self, while the threaded strands represent the ongoing narratives being 'translated' in real-time.")
