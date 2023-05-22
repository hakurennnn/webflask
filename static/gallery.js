function loadCapturedFrame() {
  const imageDataURL = localStorage.getItem('capturedFrame');
  const predictedEmotion = localStorage.getItem('predictedEmotion');

  if (imageDataURL) {
      const galleryContainer = document.getElementById('image-gallery');
      const capturedImage = document.createElement('img');
      capturedImage.src = imageDataURL;
      galleryContainer.appendChild(capturedImage);
  }

  if (predictedEmotion) {
      document.getElementById('predicted-emotion').textContent = predictedEmotion;
  }
}

window.addEventListener('DOMContentLoaded', loadCapturedFrame);
