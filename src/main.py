import cv2
import numpy as np
from keras.models import load_model
import serial
import time
import RPi.GPIO as GPIO

# Load the model
model = load_model('keras_model.h5')

# CAMERA can be 0 or 1 based on the default camera of your computer.
camera = cv2.VideoCapture(0)

# Grab the labels from the labels.txt file. This will be used later.
labels = open('labels.txt', 'r').readlines()

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()
ser.write(b"3\n")
line = ser.readline().decode('utf-8').rstrip()
print(line)
time.sleep(1)

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


while True:
    # Grab the webcam image.
    ret, image = camera.read()
    # Resize the raw image into (224-height,224-width) pixels.
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    # Show the image in a window
    cv2.imshow('Webcam Image', image)
    # Make the image a numpy array and reshape it to the model's input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    # Normalize the image array
    image = (image / 127.5) - 1
    # Have the model predict what the current image is. Model.predict
    # returns an array of percentages. Example: [0.2, 0.8] meaning it's 20% sure
    # it is the first label and 80% sure it's the second label.
    probabilities = model.predict(image)
    # Print the label with the highest probability
    print(labels[np.argmax(probabilities)])
    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    dist = distance()
    print("Measured Distance = %.1f cm" % dist)

    time.sleep(1)

    ser.reset_input_buffer()
    ser.write(b"3\n")
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    time.sleep(1)

    if dist <= 8:
        if np.argmax(probabilities) == 0:  # Changed from '0' to 0
            ser.write(b"1\n")  # Changed '/n' to '\n'
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            time.sleep(1)
            ser.write(b"1\n")  # Changed '/n' to '\n'
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            time.sleep(1)
            continue

        if np.argmax(probabilities) == 1:  # Changed from '1' to 1
            ser.write(b"2\n")  # Changed '/n' to '\n'
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            time.sleep(1)
            ser.write(b"2\n")  # Changed '/n' to '\n'
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            time.sleep(1)
            continue
        continue

    # 27 is the ASCII code for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
print("It's fin")
GPIO.cleanup()
cv2.destroyAllWindows()
