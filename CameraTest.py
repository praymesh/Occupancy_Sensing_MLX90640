import board
import busio
from adafruit_mlx90640 import MLX90640

def check_camera_connection():
    try:
        # Initialize I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)
        
        # Try to initialize the MLX90640 camera
        mlx = MLX90640(i2c)
        print("MLX90640 camera is connected and ready.")
        return True
    except Exception as e:
        print(f"Failed to connect to MLX90640 camera: {e}")
        return False

if __name__ == "__main__":
    check_camera_connection()