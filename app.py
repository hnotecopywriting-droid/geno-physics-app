import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. PAGE SETUP
st.set_page_config(layout="wide", page_title="Geno-Physics Lab")
st.title("RNA/DNA Vector Reaction Research")
st.write("Visualizing how external environmental vectors cause structural damage and 'Incomplete' DNA states.")

# 2. THE 5 VECTORS (External Influences)
with st.sidebar:
    st.header("Vector Experiment Controls")
    v1 = st.slider('Vector 1: Vertical Pull (Gravity/Tension)', -5.0, 5.0, 0.0)
    v2 = st.slider('Vector 2: Thermal Expansion (Heat/Swelling)', 0.5, 5.0, 2.0)
    v3 = st.slider('Vector 3: pH Ionic Charge (Positive/Negative)', -2.0, 2.0, 0.0)
    v4 = st.slider('Vector 4: Frequency/Vibration', 0.0, 5.0, 1.0)
    v5 = st.slider('Vector 5: Critical Impact (Toxicity/Carcinogen)', 0.0, 10.0, 0.0)

# 3. THE 3D ENGINE
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Building the Helix Core
z = np.linspace(0, 15, 150)
theta = (1.0 + (v4 * 0.05)) * z  # Twist influenced by Frequency

# Helix strands react to V2 (Radius) and V3 (Shift)
x1, y1 = (v2 + v3) * np.cos(theta), (v2 + v3) * np.sin(theta)
x2, y2 = (v2 + v3) * np.cos(theta + np.pi), (v2 + v3) * np.sin(theta + np.pi)

# Applying V1 (Vertical) and V5 (Critical Damage)
z_distorted = z + (v1 * 0.2)
noise = np.random.normal(0, v5 * 0.05, 150) # The 'Damage' noise

# 4. RENDERING THE CORE
if v5 > 7.0: # Visualizing Critical Damage/Cancerous State
    ax.scatter(x1 + noise, y1 + noise, z_distorted, color='darkred', s=5, label="Damaged/Incomplete")
    ax.scatter(x2 + noise, y2 + noise, z_distorted, color='darkred', s=5)
else:
    ax.plot(x1 + noise, y1 + noise, z_distorted, color='black', lw=3, alpha=0.8)
    ax.plot(x2 + noise, y2 + noise, z_distorted, color='blue', lw=3, alpha=0.8)

# 5. RENDERING THE HAIRS (The Sensors)
for i in range(0, len(z), 6):
    # Hair tips respond to the vectors
    # They pull away or push in based on the Positive/Negative approach
    tip_x = x1[i] * (1.5 + v5*0.1) + v3
    tip_y = y1[i] * (1.5 + v5*0.1)
    
    # Color changes if the impact is 'Bad' (Red) or 'Good' (Cyan)
    hair_color = 'red' if v5 > 4.0 else 'cyan'
    
    ax.plot([x1[i], tip_x], [y1[i], tip_y], [z_distorted[i], z_distorted[i]], 
            color=hair_color, lw=1, alpha=0.6)
    
    # Repeat for second strand
    tip_x2 = x2[i] * (1.5 + v5*0.1) + v3
    ax.plot([x2[i], tip_x2], [y2[i], tip_y], [z_distorted[i], z_distorted[i]], 
            color=hair_color, lw=1, alpha=0.6)

# Aesthetics
ax.set_axis_off()
ax.view_init(elev=20, azim=45)
st.pyplot(fig)

# 6. RESEARCH DIAGNOSTICS
st.divider()
if v5 > 7.0:
    st.error(f"OBSERVATION: DNA integrity compromised. Vector 5 impact exceeds threshold. Result: Incomplete Record.")
else:
    st.success(f"OBSERVATION: Helix stable. Co-reaction within functional limits.")
