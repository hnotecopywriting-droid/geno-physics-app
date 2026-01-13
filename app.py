import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set the page to wide mode for research viewing
st.set_page_config(layout="wide")

st.title("RNA RA Vector Lab")
st.write("Adjust the 5 vectors below to see the resultant 3D image.")

# 1. THE 5 VECTORS (Control Panel)
col1, col2 = st.columns([1, 2]) # Split screen: Controls on left, Image on right

with col1:
    st.header("Vector Inputs")
    v1 = st.slider('Vector 1: Structural (X)', 0.1, 10.0, 5.0)
    v2 = st.slider('Vector 2: Thermal (Y)', 0.1, 10.0, 5.0)
    v3 = st.slider('Vector 3: pH (Z)', 0.1, 10.0, 5.0)
    v4 = st.slider('Vector 4: Detail Density', 5, 50, 25)
    v5 = st.slider('Vector 5: Magnitude (Alpha)', 0.1, 1.0, 0.7)

# 2. THE 3D IMAGE RENDERING
with col2:
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create the grid based on Vector 4 (Detail)
    u = np.linspace(0, 2 * np.pi, v4)
    v = np.linspace(0, np.pi, v4)

    # Calculate coordinates using Vectors 1, 2, and 3
    x = v1 * np.outer(np.cos(u), np.sin(v))
    y = v2 * np.outer(np.sin(u), np.sin(v))
    z = v3 * np.outer(np.ones(np.size(u)), np.cos(v))

    # Plot the surface using Vector 5 (Alpha/Transparency)
    surf = ax.plot_surface(x, y, z, cmap='viridis', alpha=v5, edgecolor='k', linewidth=0.1)

    # Set fixed boundaries so the 'Home' stays stable
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-10, 10])
    
    ax.set_xlabel('X Vector')
    ax.set_ylabel('Y Vector')
    ax.set_zlabel('Z Vector')

    st.pyplot(fig)
