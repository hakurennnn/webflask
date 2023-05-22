import cv2
import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from flask import Flask, render_template, Response, request, jsonify
import base64

app = Flask(__name__, static_folder='static')

# Your existing routes
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/about')
def about():
    return render_template('about.html')


# Add the new '/capture' route
@app.route('/capture')
def capture():
    return render_template('capture.html')


# Add the '/video_feed' route for streaming video
def gen():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    emotion_label = ['angry', 'happy', 'neutral', 'sad', 'surprise'];
    model = load_model('best_model.h5')

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (224, 224), interpolation=cv2.INTER_AREA)
            roi_gray = cv2.cvtColor(roi_gray, cv2.COLOR_GRAY2RGB)
            roi_gray = np.expand_dims(roi_gray, axis=0)
            roi_gray = roi_gray.astype('float32')
            roi_gray /= 255.0

            preds = model.predict(roi_gray)[0]
            emotion_label = emotion_dict[np.argmax(preds)]
            cv2.putText(frame, emotion_label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    cap.release()


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Add the '/process_frame' route for processing the captured frame
@app.route('/process_frame', methods=['POST'])
def process_frame():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    emotion_dict = {0: 'angry', 1: 'happy', 2: 'neutral', 3: 'sad', 4: 'surprise'}
    model = load_model('best_model.h5')

    # Get the image data from the request
    image_data = request.json['image']
    image = cv2.imdecode(np.fromstring(base64.b64decode(image_data.split(',')[1]), np.uint8), cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (224, 224), interpolation=cv2.INTER_AREA)
        roi_gray = cv2.cvtColor(roi_gray, cv2.COLOR_GRAY2RGB)
        roi_gray = np.expand_dims(roi_gray, axis=0)
        roi_gray = roi_gray.astype('float32')
        roi_gray /= 255.0

        preds = model.predict(roi_gray)[0]
        emotion_label = emotion_dict[np.argmax(preds)]
        cv2.putText(image, emotion_label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Convert the processed image back to base64 encoded string
    _, encoded_image = cv2.imencode('.png', image)
    image_data = base64.b64encode(encoded_image.tobytes()).decode('utf-8')

    return jsonify({'emotion': emotion_label, 'image': image_data})


if __name__ == '__main__':
    app.run(debug=True)
