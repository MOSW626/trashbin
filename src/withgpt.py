import cv2
import numpy as np
from keras.models import load_model
import serial
import time

# Load the model
model = load_model('keras_model.h5')

# CAMERA can be 0 or 1 based on the default camera of your computer.
camera = cv2.VideoCapture(0)

# Grab the labels from the labels.txt file. This will be used later.
labels = open('labels.txt', 'r').readlines()

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

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

    if np.argmax(probabilities) == 0:  # Changed from '0' to 0
        ser.write(b"1\n")  # Changed '/n' to '\n'
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)
        ser.write(b"1\n")  # Changed '/n' to '\n'
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)
        break

    if np.argmax(probabilities) == 1:  # Changed from '1' to 1
        ser.write(b"2\n")  # Changed '/n' to '\n'
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)
        ser.write(b"2\n")  # Changed '/n' to '\n'
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)
        break

    # 27 is the ASCII code for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
