# admin.py
from django import forms
from django.contrib import admin
from .models import Employee
from django.utils.safestring import mark_safe

class EmployeeAdminForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'employee_id', 'face_encoding']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['face_encoding'].widget = forms.HiddenInput()

class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeAdminForm

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if not extra_context:
            extra_context = {}
        extra_context['custom_camera_script'] = mark_safe("""
            <script src="https://cdn.jsdelivr.net/npm/face-api.js"></script>
            <h3 style="text-align:center;">Capture Face</h3>
            <video id="videoInput" width="480" height="360" autoplay muted></video><br/>
            <button type="button" onclick="capture()">Capture Face</button>
            <canvas id="canvas" width="480" height="360" style="display:none;"></canvas>
            <script>
              const video = document.getElementById('videoInput');
              navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => { video.srcObject = stream; })
                .catch(err => alert("Camera error: " + err));

              Promise.all([
                faceapi.nets.tinyFaceDetector.loadFromUri('/static/models'),
                faceapi.nets.faceLandmark68Net.loadFromUri('/static/models'),
                faceapi.nets.faceRecognitionNet.loadFromUri('/static/models'),
              ]).then(() => console.log("Face API loaded"));

              async function capture() {
                const canvas = document.getElementById('canvas');
                const ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                const detection = await faceapi.detectSingleFace(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceDescriptor();
                if (!detection) return alert("No face detected");

                const encoding = Array.from(detection.descriptor);
                document.querySelector('[name=face_encoding]').value = JSON.stringify(encoding);

                // Submit the form after capturing
                document.querySelector('form').submit();
              }
            </script>
        """)
        return super().changeform_view(request, object_id, form_url, extra_context)

admin.site.register(Employee, EmployeeAdmin)