import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 1. SETTING THE STAGE (The "Home" for the Image)
fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(122, projection='3d') # Right side: The 3D Image
plt.subplots_adjust(left=0.1, bottom=0.25) # Left side: Space for Sliders

# 2. THE INITIAL 5 VECTORS (Starting values)
v1_start, v2_start, v3_start, v4_start, v5_start = 1.0, 1.0, 1.0, 5.0, 0.5

# 3. THE IMAGE RENDERING FUNCTION
def render_image(v1, v2, v3, v4, v5):
    ax.clear()
    # v4 (Density) creates the level of detail
    density = int(v4 * 5) + 5
    u = np.linspace(0, 2 * np.pi, density)
    v = np.linspace(0, np.pi, density)
    
    # v1, v2, v3 act as the X, Y, Z dimensional stabilizers
    x = v1 * np.outer(np.cos(u), np.sin(v))
    y = v2 * np.outer(np.sin(u), np.sin(v))
    z = v3 * np.outer(np.ones(np.size(u)), np.cos(v))
    
    # v5 (Magnitude) controls the color intensity (The "Flash")
    ax.plot_surface(x, y, z, cmap='magma', alpha=v5, edgecolor='w', lw=0.5)
    
    # Keeping the view consistent
    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])
    ax.set_zlim([-5, 5])
    ax.set_title("3D Resultant Image (010 Truth)")
    fig.canvas.draw_idle()

# 4. CREATING THE 5 VECTOR NODES (Sliders)
ax_v1 = plt.axes([0.1, 0.2, 0.3, 0.03])
ax_v2 = plt.axes([0.1, 0.15, 0.3, 0.03])
ax_v3 = plt.axes([0.1, 0.1, 0.3, 0.03])
ax_v4 = plt.axes([0.1, 0.05, 0.3, 0.03])
ax_v5 = plt.axes([0.1, 0.01, 0.3, 0.03])

s_v1 = Slider(ax_v1, 'Vector 1 (X)', 0.1, 5.0, valinit=v1_start)
s_v2 = Slider(ax_v2, 'Vector 2 (Y)', 0.1, 5.0, valinit=v2_start)
s_v3 = Slider(ax_v3, 'Vector 3 (Z)', 0.1, 5.0, valinit=v3_start)
s_v4 = Slider(ax_v4, 'Vector 4 (Detail)', 1, 10, valinit=v4_start)
s_v5 = Slider(ax_v5, 'Vector 5 (Alpha)', 0.1, 1.0, valinit=v5_start)

# 5. THE UPDATE LOGIC (Connecting Sliders to Image)
def update(val):
    render_image(s_v1.val, s_v2.val, s_v3.val, s_v4.val, s_v5.val)

s_v1.on_changed(update)
s_v2.on_changed(update)
s_v3.on_changed(update)
s_v4.on_changed(update)
s_v5.on_changed(update)

# Initial Render
render_image(v1_start, v2_start, v3_start, v4_start, v5_start)

print("Application Running: The 3D Image is now visible.")
plt.show()
