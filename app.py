import cv2
import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from flask import Flask, render_template, Response, request, jsonify
import base64
import re
from PIL import Image
import io

app = Flask(__name__)

# Load the model
model = load_model("best_model.h5")

# Load the face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

def gen():
    while True:
        ret, test_img = cap.read()

        if not ret:
            break

        gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
        faces_detected = face_cascade.detectMultiScale(gray_img, 1.32, 5)

        for (x, y, w, h) in faces_detected:
            cv2.rectangle(test_img, (x, y), (x + w, y + h), (255, 0, 0), thickness=7)
            roi_gray = gray_img[y:y + w, x:x + h]
            roi_gray = cv2.resize(roi_gray, (224, 224))
            img_pixels = img_to_array(roi_gray)
            img_pixels = cv2.cvtColor(roi_gray, cv2.COLOR_BGR2RGB)
            img_pixels = cv2.resize(img_pixels, (224, 224))
            img_pixels = np.expand_dims(img_pixels, axis=0)
            img_pixels = img_pixels.astype('float32')
            img_pixels /= 255

            predictions = model.predict(img_pixels)
            max_index = np.argmax(predictions[0])

            emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
            predicted_emotion = emotions[max_index]

            cv2.putText(test_img, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        ret, jpeg = cv2.imencode('.jpg', test_img)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/show_capture')
def show_capture():
    return render_template('capture.html')

@app.route('/gallery')
def show_gallery():
    return render_template('gallery.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    image_data = request.get_json().get('image')
    image_data = re.sub('^data:image/.+;base64,', '', image_data)
    image_data = base64.b64decode(image_data)

    # Load and preprocess the image
    img = Image.open(io.BytesIO(image_data)).convert('L')
    img = img.resize((224, 224))
    img_array = img_to_array(img)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)  # Convert to 3-channel (RGB)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255

    # Perform emotion prediction
    predictions = model.predict(img_array)
    emotion_index = np.argmax(predictions[0])
    emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    predicted_emotion = emotions[emotion_index]

    return jsonify({'emotion': predicted_emotion})

if __name__ == '__main__':
    app.run(debug=True)
