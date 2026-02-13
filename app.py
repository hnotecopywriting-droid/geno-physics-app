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
st
