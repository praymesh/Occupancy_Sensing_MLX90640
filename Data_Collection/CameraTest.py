import smbus2

I2C_BUS = 1  
MLX90640_I2C_ADDR = 0x33  

try:
    print("Initializing I2C bus...")
    bus = smbus2.SMBus(I2C_BUS)

    # Try reading 2 bytes from a known register (e.g., 0x2400 - device ID register)
    register = 0x2400  
    result = bus.read_word_data(MLX90640_I2C_ADDR, register)

    print(f"MLX90640 detected at address {hex(MLX90640_I2C_ADDR)}!")
    print(f"Read from register {hex(register)}: {hex(result)}")

except Exception as e:
    print("MLX90640 not detected. Check wiring!")
    print(f"Error: {e}")
