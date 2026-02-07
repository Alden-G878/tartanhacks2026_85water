import serial
import time

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )
def remap(angle):
    source_span = 199
    source_min = 0
    target_span = 400
    target_min = 1500
    scale_factor = float(target_span) / float(source_span)
    remapped_value = target_min + (value - source_min) * scale_factor
    return remapped_value

def command(servo, angle):
    waveform = remap(angle)
    ser.write(bytes([servo]))
    time.sleep(0.1)
    ser.write(bytes([angle]))
