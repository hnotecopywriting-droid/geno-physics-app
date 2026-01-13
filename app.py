import streamlit as st
from stmol import showmol
import py3Dmol

# Page Setup
st.set_page_config(page_title="RNA RA Vector Lab", layout="wide")
st.title("🧬 RNA RA Vector: Human Force Encoding")
st.subheader("Mapping Environmental Markers to the 29-Residue Helix")

# --- SIDEBAR: THE 5 HUMAN FUNCTIONS ---
st.sidebar.header("🕹️ Vector Modulators")

# 1. Gravity (Vertical Compression)
gravity = st.sidebar.slider("Gravity/G-Force (m/s²)", 0.0, 20.0, 9.8)

# 2. Thermal (Kinetic Jitter)
thermal = st.sidebar.slider("Thermal Kinetic (Q)", 0, 100, 25)

# 3. Circadian (Sleep/Wake State)
state = st.sidebar.select_slider("Circadian State", options=["Deep Sleep", "Awake"])

# 4. Inertia (The Pool Push)
inertia = st.sidebar.toggle("Inertial Momentum (Pool Push)")

# --- LOGIC: RENDERING THE VECTOR ---
view = py3Dmol.view(query='pdb:1EBQ') # The 29-residue RNA anchor

# Visualizing the State (Sleep vs Awake)
if state == "Deep Sleep":
    view.setStyle({'stick': {'color': 'cyan', 'radius': 0.5}})
    st.info("RA Vector: Low-Tension Recovery (Sleep Marker)")
else:
    view.setStyle({'cartoon': {'color': 'spectrum', 'arrows': True}})
    st.success("RA Vector: High-Tension Encoding (Awake Marker)")

# Applying Gravity (Zoom acts as axial compression)
view.zoom(1.0 + (gravity/20))

# Applying Inertia (Shear effect)
if inertia:
    view.rotate(45, {'x':1, 'y':1, 'z':0})

# Applying Thermal Jitter
if thermal > 70:
    view.spin(True)

showmol(view, height=600, width=900)

# --- THE VECTOR LOGIC ---
st.markdown("---")
st.latex(r"\vec{RA}_{vector} = f(\text{Gravity, Thermal, Circadian})")
