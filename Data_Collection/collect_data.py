import time,board,busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt
import pandas as pd
# import keyboard
from tempfile import TemporaryFile

# Set up MLX90640
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ # set refresh rate
mlx_shape = (24,32)


# setup the figure for plotting
plt.ion() # enables interactive plotting
fig,ax = plt.subplots(figsize=(7,2))
therm1 = ax.imshow(np.zeros(mlx_shape),vmin=0,vmax=60) #start plot with zeros
cbar = fig.colorbar(therm1) # setup colorbar for temps
cbar.set_label('Temperature [$^{\circ}$C]',fontsize=14) # colorbar label

df = pd.DataFrame(columns=['Timestamp'])
numpyfile = TemporaryFile()
pixel_matrices = []

t_array = []
i = 0

while True:
    t1 = time.monotonic()
    try:
        frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures
        data_array = mlx.getFrame(frame) # read MLX temperatures into frame var
        data_array = (np.reshape(frame,mlx_shape)) # reshape to 24x32
        therm1.set_data(np.fliplr(data_array)) # flip left to right
        
        # Append pixel_matrix and timestamp values
        pixel_matrices.append(data_array)
        df.at[i,0] = t1
        i = i + 1
        
        
        # Save thermal image to directory
        therm1.set_clim(vmin=np.min(data_array),vmax=np.max(data_array)) # set bounds
        cbar.update_normal(therm1) # update colorbar range
        plt.pause(0.001) # required

        fig.savefig(r"/home/pi/Thermcam/Pixel_data/data_0/" + str(t1) + r".png", dpi=300,facecolor='#FCFCFC',
                    bbox_inches='tight') # comment out to speed up
        t_array.append(time.monotonic()-t1)
        
        # print('Sample Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))
        
        
    except KeyboardInterrupt:
        numpyfile = str(t1)
        pixel_array = np.stack(pixel_matrices)
        np.save(r"/home/pi/Thermcam/Pixel_data/data_0/" + numpyfile, pixel_array, allow_pickle = True)
        df.to_csv(r"/home/pi/Thermcam/Pixel_data/data_0/" + str(t1) + ".csv")
        break