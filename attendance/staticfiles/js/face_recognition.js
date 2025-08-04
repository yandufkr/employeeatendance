window.captureFace = async function () {
  const video = document.getElementById('video');
  const faceEncodingInput = document.getElementById('face_encoding');
  const capturedImage = document.getElementById('capturedImage');

  try {
    const detection = await faceapi
      .detectSingleFace(video, new faceapi.TinyFaceDetectorOptions())
      .withFaceLandmarks()
      .withFaceDescriptor();

    if (!detection) {
      alert('⚠️ No face detected. Please try again.');
      return;
    }

    const descriptor = Array.from(detection.descriptor);
    faceEncodingInput.value = JSON.stringify(descriptor);

    // Capture image from video
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    capturedImage.src = canvas.toDataURL('image/png');
    capturedImage.style.display = 'block';

    alert('✅ Face captured. You can now submit the form.');
  } catch (error) {
    alert('❌ Error capturing face: ' + error);
  }
};

(async () => {
  const video = document.getElementById('video');

  // Start webcam
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
  } catch (err) {
    alert('❌ Cannot access webcam: ' + err);
    return;
  }

  // Load face-api.js models from your static folders
  try {
    await Promise.all([
      faceapi.nets.tinyFaceDetector.loadFromUri('/static/models/tiny_face_detector'),
      faceapi.nets.faceLandmark68Net.loadFromUri('/static/models/face_landmark_68'),
      // If you prefer tiny landmarks, uncomment the next line and comment the above line
      // faceapi.nets.faceLandmark68TinyNet.loadFromUri('/static/models/face_landmark_68_tiny'),
      faceapi.nets.faceRecognitionNet.loadFromUri('/static/models/face_recognition'),
    ]);
    console.log('✅ Face-api.js models loaded successfully');
  } catch (err) {
    alert('❌ Failed to load face detection models.');
    console.error(err);
  }
})();
