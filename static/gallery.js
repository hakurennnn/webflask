function captureFrameAndSave() {
    // Access the video stream from the canvas element
    const video = document.getElementById('video');
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
  
    // Convert the captured frame to base64 data URL
    const imageDataURL = canvas.toDataURL('image/png');
  
    // Create a new image element to display the captured frame in the gallery
    const capturedImage = document.createElement('img');
    capturedImage.src = imageDataURL;
  
    // Append the captured image to the gallery container
    const galleryContainer = document.getElementById('gallery-container');
    galleryContainer.appendChild(capturedImage);
  }
  