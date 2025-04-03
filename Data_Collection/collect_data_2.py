import time
import os
import board
import busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt

# Ensure directories exist
image_dir = "/home/pi/Thermcam/Pixel_data/data_1_person"
data_dir = "/home/pi/Thermcam/Pixel_data/data_1_person_nmpy"
#os.makedirs(image_dir, exist_ok=True)
#os.makedirs(data_dir, exist_ok=True)

# Get the next available image number
existing_files = [int(f.split(".")[0]) for f in os.listdir(image_dir) if f.endswith(".png")]
next_image_num = max(existing_files, default=0) + 1  # Start from 1

# Set up MLX90640 sensor
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)  # Setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c)  # Initialize MLX90640
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ  # Set refresh rate
mlx_shape = (24, 32)

# Setup the figure for live display
plt.ion()  # Enable interactive mode (for live updates)
fig, ax = plt.subplots(figsize=(7, 2))
ax.axis('off')  # Hide axes
therm1 = ax.imshow(np.zeros(mlx_shape), vmin=0, vmax=60)  # Start with zeros

# Initialize storage
timestamps = []
pixel_matrices = []

try:
    while True:
        t1 = time.monotonic()
        frame = np.zeros((24 * 32,))  # Setup array for storing temperatures
        mlx.getFrame(frame)  # Read MLX temperatures into frame
        data_array = np.reshape(frame, mlx_shape)  # Reshape to 24x32
        
        # Update the display
        therm1.set_data(np.fliplr(data_array))  # Flip image left to right
        therm1.set_clim(vmin=np.min(data_array), vmax=np.max(data_array))  # Adjust colors
        plt.pause(0.001)  # Small delay for update

        # Save data
        timestamps.append(t1)
        pixel_matrices.append(data_array)

        # Save image with sequential numbering
        img_filename = os.path.join(image_dir, f"{next_image_num}.png")
        fig.savefig(img_filename, dpi=300, facecolor='#FCFCFC', bbox_inches='tight', pad_inches=0)

        # Save thermal data as NumPy array
        np.save(os.path.join(data_dir, f"{next_image_num}"), np.stack(pixel_matrices), allow_pickle=True)

        # Save timestamps to CSV
        np.savetxt(os.path.join(data_dir, f"{next_image_num}_timestamps.csv"), timestamps, delimiter=",")

        next_image_num += 1  # Increment image counter

except KeyboardInterrupt:
    print("\nLive capture stopped by user.")
    plt.ioff()  # Turn off interactive mode
    plt.close(fig)  # Close figure window
