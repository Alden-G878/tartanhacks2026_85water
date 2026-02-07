import serial
import time

# Configure the serial port
# The device name is typically /dev/ttyAMA0 on the GPIO pins
# Ensure the baud rate matches your external device
ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=9600,  # Example baud rate, change as needed
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

try:
    while True:
        # Send data
        ser.write(b"Hello from Raspberry Pi!\n")
        print("Data sent")

        # Read data (example of non-blocking read, adjust as needed)
        if ser.in_waiting > 0:
            received_data = ser.readline().decode('utf-8').rstrip()
            print(f"Received: {received_data}")

        time.sleep(1)

except KeyboardInterrupt:
    ser.close()
    print("Serial port closed")

