import streamlit as st
import pypdb
from stmol import showmol
import py3Dmol

st.set_page_config(layout="wide")
st.title("🧬 RNA RA Vector Lab: The 5 Human Stimuli")

# Sidebar - The 5 Human Vectors
st.sidebar.header("RA Vector Modulators")
gravity = st.sidebar.slider("1. Gravity (Vertical)", 0.0, 20.0, 9.8)
thermal = st.sidebar.slider("2. Thermal (Vibration)", 0, 100, 37)
light = st.sidebar.slider("3. Circadian (Light)", 0, 100, 50)
pressure = st.sidebar.slider("4. Pressure (Atmospheric)", 0.0, 5.0, 1.0)
ph_level = st.sidebar.slider("5. pH (Chemical)", 0.0, 14.0, 7.4)

st.sidebar.markdown("---")
inertia = st.sidebar.toggle("Inertial Momentum (Pool Push)")

# Logic for Visual Stimuli (Colors and Shapes)
color_scheme = "spectrum"
if light < 30: # Deep Sleep Mode
    color_scheme = "cyan"
    st.info("System State: Recovery (Deep Sleep)")

# 3D Render
view = py3Dmol.view(query='pdb:1EBQ')
view.setStyle({'cartoon': {'color': color_scheme}})

# ADDING THE VISUAL VECTORS (Stimuli)
# This adds a visual 'force' cylinder to represent the RA Vector
view.addCylinder({
    'start': {'x': 0, 'y': 0, 'z': 0},
    'end': {'x': 0, 'y': gravity, 'z': 0},
    'radius': 0.5,
    'fromCap': 1, 'toCap': 2,
    'color': 'red',
    'hoverable': True
})

if inertia:
    view.rotate(45, {'x': 1, 'y': 1, 'z': 0})

view.zoomTo()
showmol(view, height=600, width=800)

st.write(f"**Current Vector Matrix:** G:{gravity} | T:{thermal} | L:{light} | P:{pressure} | pH:{ph_level}")
