import cv2
from keras.models import load_model
from PIL import ImageOps
import numpy as np

np.set_printoptions(suppress=True)

model = load_model("Desktop/keras_model.h5", compile=False)

class_names = open("Desktop/labels.txt", "r").readlines()

data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

cap = cv2.VideoCapture(0)

while True:
    # Read frame from the webcam
    ret, frame = cap.read()

    # Preprocess the frame
    image = ImageOps.fit(frame, (224, 224))
    image_array = np.array(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    # Predict the frame
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Display the prediction on the frame
    label = f"Class: {class_name[2:]} | Confidence Score: {confidence_score}"
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("AI Webcam", frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the windows
cap.release()
cv2.destroyAllWindows()
