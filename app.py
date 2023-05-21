# app.py
from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
import warnings
warnings.filterwarnings("ignore")
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

app = Flask(__name__, static_url_path='/static')
model = load_model("static/best_model.h5")

face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def perform_facial_emotion_analysis(image_data):
    nparr = np.frombuffer(base64.b64decode(image_data.split(',')[1]), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)

    if len(faces_detected) > 0:
        (x, y, w, h) = faces_detected[0]
        roi_gray = gray_img[y:y + w, x:x + h]
        roi_gray = cv2.resize(roi_gray, (224, 224))
        img_pixels = img_to_array(roi_gray)
        img_pixels = np.expand_dims(img_pixels, axis=0)
        img_pixels = img_pixels.astype('float32') / 255

        predictions = model.predict(img_pixels)
        max_index = np.argmax(predictions[0])
        predicted_emotion = emotions[max_index]  # Get the emotion label
        return predicted_emotion
    return 'No faces detected'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/capture')
def capture():
    return render_template('capture.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.get_json()
    image_data = data['image']

    predicted_emotion = perform_facial_emotion_analysis(image_data)

    return jsonify({'emotion': predicted_emotion})

if __name__ == '__main__':
    app.run(debug=True)
