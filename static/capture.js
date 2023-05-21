async function startViewfinder() {
    const video = document.getElementById('video');
    const boundingBox = document.querySelector('.bounding-box');

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        video.play();
        boundingBox.appendChild(video);
        await tf.setBackend('webgl');
        facialEmotionAnalysis();
    } catch (error) {
        console.error('Error accessing the webcam:', error);
    }
}

function captureFrame() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('video-canvas');
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageDataURL = canvas.toDataURL('image/png');
    facialEmotionAnalysis(imageDataURL);
}

// facial emotions
async function facialEmotionAnalysis(imageDataURL) {
    const emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'];
    const response = await fetch('/process_frame', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageDataURL }),
    });
    const data = await response.json();
    const predictedEmotion = emotions[data.emotion];
    // Display
    document.getElementById('predicted-emotion').textContent = predictedEmotion;
}
