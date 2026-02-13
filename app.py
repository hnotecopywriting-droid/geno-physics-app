import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="RNA Influence Matrix", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR "BAD ASS" STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMarkdown h1, h2, h3 { color: #00f2ff; }
    .stInfo { background-color: #1e2a3a; border-left: 5px solid #00f2ff; }
    </style>
    """, unsafe_content_usage=True)

# --- THE DATA DICTIONARY (Pearson & RNA Info) ---
parts_info = {
    "Hairpin Loop": {
        "desc": "A single strand of RNA that folds back upon itself. Critical for gene expression.",
        "fact": "As seen in the Wikipedia documentation, these loops provide structural stability."
    },
    "Ribose Sugar": {
        "desc": "The 'R' in RNA. Contains a 2'-hydroxyl group that makes it chemically more reactive than DNA.",
        "fact": "This reactivity allows RNA to act as an enzyme, not just an information carrier."
    },
    "Uracil Base": {
        "desc": "RNA’s unique base. Replaces Thymine found in DNA.",
        "fact": "Pairs with Adenine (A) via two hydrogen bonds. Key for the 'RNA World' theory."
    },
    "Pearson Alignment": {
        "desc": "The Pearson Correlation Coefficient measures spatial accuracy.",
        "fact": "In our model, this tracks how well external pressure aligns with internal structural responses."
    }
}

# --- SIDEBAR: THE 10-SLIDER CONTROL MATRIX ---
st.sidebar.title("🎮 Control Matrix")
st.sidebar.markdown("---")

st.sidebar.subheader("🌍 External Influences (Inputs)")
p_mech = st.sidebar.slider("Mechanical Pressure (P_mech)", 0.0, 1.0, 0.20)
t_rad = st.sidebar.slider("Thermal Stress (T_rad)", 0.0, 1.0, 0.35)
v_res = st.sidebar.slider("Vibrational Res (V_res)", 0.0, 1.0, 0.10)
c_temp = st.sidebar.slider("Temporal Flow (C_temp)", 0.0, 1.0, 0.50)
x_bio = st.sidebar.slider("Biodemographic (X_bio)", 0.0, 1.0, 0.15)

st.sidebar.markdown("---")
st.sidebar.subheader("🧬 Internal RA Nodes (Responses)")
# In the 5x5 Matrix, these are mapped to the influencers above
ra1 = st.sidebar.slider("RA Node 1 (Linked: P_mech)", 0.0, 1.0, p_mech)
ra2 = st.sidebar.slider("RA Node 2 (Linked: T_rad)", 0.0, 1.0, t_rad)
ra3 = st.sidebar.slider("RA Node 3 (Linked: V_res)", 0.0, 1.0, v_res)
ra4 = st.sidebar.slider("RA Node 4 (Linked: C_temp)", 0.0, 1.0, c_temp)
ra5 = st.sidebar.slider("RA Node 5 (Linked: X_bio)", 0.0, 1.0, x_bio)

# --- MATH: THE 100% REACTION LOGIC ---
def calculate_matrix_intensity(primary, others):
    # Rule: 100% reaction to primary slider + partial from others
    weights = 0.25 # "Weighted Sympathy"
    intensity = (primary * 1.0) + (sum(others) * weights)
    return min(intensity, 1.0) # Cap at 1.0 for UI

matrix_intensity = calculate_matrix_intensity(p_mech, [t_rad, v_res, c_temp, x_bio])

# --- MAIN LAYOUT ---
st.title("🧬 RNA-RNP 175,000 Influence Matrix")
st.markdown("### *Predicting Globular Folding via Environmental Interaction*")

col_main, col_sub = st.columns([2, 1])

with col_main:
    st.subheader("🌐 3D Structural Render (Rockefeller Model)")
    
    # GENERATE GLOBULE (Simplified representation of 175k residues)
    n_points = 3500 
    indices = np.arange(n_points)
    # Fibonacci Sphere mapping for a globular "bunched" look
    phi = np.arccos(1 - 2*indices/n_points)
    theta = np.pi * (1 + 5**0.5) * indices

    # APPLY SLIDER LOGIC TO COORDINATES
    # P_mech compresses radius, T_rad causes vibration/expansion
    base_radius = (1.5 - (p_mech * 0.7)) 
    vibration = np.sin(theta * 10) * (v_res * 0.2)
    radius = base_radius + vibration
    
    x = radius * np.cos(theta) * np.sin(phi)
    y = radius * np.sin(theta) * np.sin(phi)
    z = radius * np.cos(phi) + (t_rad * 0.5) # Heat makes it "rise"

    # BUILD 3D PLOT
    fig = go.Figure(data=[go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=3,
            color=z, # Height-based coloring
            colorscale='Hot' if t_rad > 0.5 else 'Viridis',
            opacity=0.7
        )
    )])

    fig.update_layout(
        template="plotly_dark",
        height=700,
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False)
        )
    )
    st.plotly_chart(fig, use_container_width=True)

with col_sub:
    st.subheader("🔍 Part Inspector")
    selection = st.selectbox("Pick a component to inspect:", list(parts_info.keys()))
    
    # INFO DISPLAY
    st.markdown(f"**Description:** {parts_info[selection]['desc']}")
    st.info(f"**Scientific Context:** {parts_info[selection]['fact']}")
    
    # MINI INTERACTIVE MODEL FOR SUB-PAGE
    st.markdown("---")
    st.write(f"**Dimensional Profile: {selection}**")
    
    # Create a small loop or helix depending on selection
    t_mini = np.linspace(0, 10, 100)
    if "Loop" in selection:
        xm, ym, zm = np.sin(t_mini), np.cos(t_mini), np.sin(t_mini/2)
    else:
        xm, ym, zm = np.cos(t_mini), np.sin(t_mini), t_mini/5

    mini_fig = go.Figure(data=[go.Scatter3d(x=xm, y=ym, z=zm, mode='lines', line=dict(color='#00f2ff', width=6))])
    mini_fig.update_layout(template="plotly_dark", height=300, margin=dict(l=0,r=0,b=0,t=0), showlegend=False)
    st.plotly_chart(mini_fig, use_container_width=True)

    # REACTION METRIC
    st.metric(label="Matrix Reaction Intensity", value=f"{matrix_intensity:.2%}")

# --- FOOTER: THE COUNSELING SELLING POINT ---
st.markdown("---")
st.subheader("🧠 Counseling & Systems Theory Application")
st.write(f"""
    **Current State Analysis:** This model demonstrates that a high value of **{selection}** under a Mechanical Pressure of **{p_mech:.2f}** results in a { "dense" if p_mech > 0.5 else "flexible" } structural alignment. 
    In counseling, this mirrors how individuals compact their internal 'blueprints' (DNA/RNA) 
    to survive high-pressure environments. Structural integrity is a negotiation with the outside world.
""")

st.caption("Developed for Stanford RNA 3D Folding Challenge Part 2 | Model: Rockefeller Rough RNP")
