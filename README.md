# **Thermal Dataset YOLOv8 Occupancy Sensing**

**This project focuses on automatic labeling and training preparation for thermal images used for occupancy detection(number of people).** 

#Images are organized by the number of people, labeled using thermal blob detection, and formatted for use with YOLOv8.

#Custom Dataset is collected  using Raspberry Pi and **MLX90640 **Thermal Camera Module. 
Preprocessed and annotated the data.. 

I have also used Adaptive Blob Filtering Algorithm - ABFA, as mentioned in the paper : https://ieeexplore.ieee.org/document/10041292

Further, the model is quantized to be deployed on Edge devices like Raspberry Pi. 
Quantized using tflite(works better on resource constrained devices).

Though, after quantization the model accuracy got reduced. 
Future Work: To fine tune the quantized model for increasing the accuracy towards new seen data. 

Also the model works well upto 8 people(for 32*24 resolution images captured from a distance of 3m, nearly a standard ceiling height. )
Example_1 :

Here We can Identify 3 People . 
![image](https://github.com/user-attachments/assets/c9495877-ec20-487a-af18-ff7528cd90ae)

Example_2
![image](https://github.com/user-attachments/assets/88d6565b-a78d-4d79-9e1a-740ce752872c)


