import picamera2

camera = PiCamera()
camera.resolution = (256, 192)
camera.start_preview()
sleep(1)
camera.capture('pic.jpg')
img = open('pic.jpg', 'rb')
img = base64.b64encode(img.read())
client.publish('pic', img) # Send to Adafruit IO
print('Picture taken!')
