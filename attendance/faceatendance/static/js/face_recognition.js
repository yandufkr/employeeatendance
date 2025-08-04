window.addEventListener('load', async () => {
    const video = document.getElementById('video');
    const faceEncodingInput = document.getElementById('face_encoding');
    const capturedImage = document.getElementById('capturedImage');
    const captureButton = document.getElementById('captureButton');

    // Start webcam
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        alert("❌ Cannot access webcam: " + err);
        return;
    }

    // Load face-api.js models from static folder (adjust paths if needed)
    try {
        await Promise.all([
            faceapi.nets.tinyFaceDetector.loadFromUri('/static/models/tiny_face_detector'),
            faceapi.nets.faceLandmark68Net.loadFromUri('/static/models/face_landmark_68'),
            faceapi.nets.faceRecognitionNet.loadFromUri('/static/models/face_recognition'),
        ]);
        console.log("✅ Face-api.js models loaded");
    } catch (err) {
        alert("❌ Failed to load face detection models.");
        console.error(err);
        return;
    }

    // Capture face on button click
    captureButton.addEventListener('click', async () => {
        try {
            const detection = await faceapi
                .detectSingleFace(video, new faceapi.TinyFaceDetectorOptions())
                .withFaceLandmarks()
                .withFaceDescriptor();

            if (!detection) {
                alert('⚠️ No face detected. Please try again.');
                return;
            }

            // Store face descriptor as JSON string
            faceEncodingInput.value = JSON.stringify(Array.from(detection.descriptor));

            // Take snapshot from video for preview
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
    });

    // Prevent form submit without face encoding
    document.getElementById("registerForm").addEventListener("submit", e => {
        if (!faceEncodingInput.value) {
            e.preventDefault();
            alert("❗ Please capture face before submitting.");
        }
    });
});
