import streamlit as st
from stmol import showmol
import py3Dmol

# Page Setup
st.set_page_config(page_title="Geno-Physics 3D", layout="wide")
st.title("🧬 Geno-Physics: 3D RNA Structural Ensemble")

# Sidebar for Logic & Controls
st.sidebar.header("Ground Truth Parameters")
st.sidebar.write(f"Ref Residues ($L_{{ref}}$): 29")
st.sidebar.write(f"Scaling Factor ($d_0$): 0.7")

# Selector for the 5 Truth Models
truth_choice = st.sidebar.selectbox("Select Structural Truth", 
    ["Truth 01: Core Stacking (F-INT)", 
     "Truth 02: Charge Potential (FE-Q)", 
     "Truth 03: High Kinetic (Q-MCT Hot)", 
     "Truth 04: Low Kinetic (Q-MCT Cold)", 
     "Truth 05: Environmental (F-EXT)"])

# Visualizer Logic
view = py3Dmol.view(query='pdb:1EBQ') # Using the HIV-1 RRE Ground Truth

if "Truth 02" in truth_choice:
    # FE-Q: Electrostatic Pos vs Neg
    view.setStyle({'cartoon': {'color': 'spectrum'}})
    view.addSurface(py3Dmol.VDW, {'opacity': 0.5, 'color': 'lightblue'})
    st.latex(r"F_e = k \frac{q_1 q_2}{r^2}")
elif "Truth 03" in truth_choice:
    # Q-MCT: Thermal Hot
    view.setStyle({'stick': {'color': 'orange'}})
    view.addSphere({'radius': 1.5, 'color': 'orange', 'opacity': 0.7})
    st.latex(r"Q = mc\Delta T")
elif "Truth 01" in truth_choice:
    # F-INT: Internal Force / Rigid
    view.setStyle({'cartoon': {'color': 'gold'}})
    st.latex(r"\sum F_{int} = 0")
else:
    view.setStyle({'cartoon': {'color': 'spectrum'}})

view.zoomTo()
showmol(view, height=500, width=800)

# Acknowledgements
st.markdown("---")
st.caption("randy hensley and with Gemini (Google AI) | Framework: US-align ($d_0=0.7$)")
