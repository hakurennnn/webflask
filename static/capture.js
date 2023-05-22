async function startViewfinder() {
    const video = document.getElementById('video');
    const boundingBox = document.querySelector('.bounding-box');
  
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      video.srcObject = stream;
      await video.play();
      boundingBox.appendChild(video);
    } catch (error) {
      console.error('Error accessing the webcam:', error);
    }
  }
  
  async function captureFrame() {
    const emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'];
    const video = document.getElementById('video');
  
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
  
    const imageDataURL = canvas.toDataURL('image/jpeg');
  
    const response = await fetch('/process_frame', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ image: imageDataURL })
    });
  
    const data = await response.json();
    const predictedEmotion = emotions[data.emotion];
    document.getElementById('predicted-emotion').textContent = predictedEmotion;
  
    saveCapturedFrame(imageDataURL, predictedEmotion);
    window.location.href = '/gallery';
  }
  
  function saveCapturedFrame(imageDataURL, predictedEmotion) {
    localStorage.setItem('capturedFrame', imageDataURL);
    localStorage.setItem('predictedEmotion', predictedEmotion);
  }
  
  document.querySelector('.start-viewfinder-button').addEventListener('click', startViewfinder);
  