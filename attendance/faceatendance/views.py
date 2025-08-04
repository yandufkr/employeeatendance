from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
import json
import numpy as np
from datetime import datetime
import base64
import pickle
from .models import Employee, AttendanceLog
import logging

logger = logging.getLogger(__name__)


def get_known_faces():
    employees = Employee.objects.all()
    known_encodings = []
    known_names = []
    for emp in employees:
        if emp.face_encoding:
            try:
                encoding = pickle.loads(base64.b64decode(emp.face_encoding))
                known_encodings.append(encoding)
                known_names.append(emp.name)
            except Exception as e:
                logger.error(f"Error decoding face encoding for {emp.name}: {str(e)}")
    return known_encodings, known_names


@csrf_exempt
def recognize(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            face_encoding = np.array(data.get('face_encoding'))

            from face_recognition import compare_faces, face_distance
            known_face_encodings, known_face_names = get_known_faces()

            if not known_face_encodings:
                return JsonResponse({'status': 'no_known_faces'})

            matches = compare_faces(known_face_encodings, face_encoding)
            distances = face_distance(known_face_encodings, face_encoding)

            best_index = np.argmin(distances)
            if matches[best_index]:
                name = known_face_names[best_index]
                now = datetime.now()
                employee = Employee.objects.get(name=name)
                AttendanceLog.objects.create(employee=employee, time=now)
                return JsonResponse({
                    'status': 'success',
                    'name': name,
                    'time': now.strftime('%Y-%m-%d %H:%M:%S')
                })
            else:
                return JsonResponse({'status': 'no_match'})
        except Exception as e:
            logger.error(f"Error in recognize: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def capture_page(request):
    return render(request, 'faceatendance/capture.html')


def redirect_to_capture(request):
    return redirect('capture')  # Ensure you have `name="capture"` in urls.py


def register_employee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        employee_id = request.POST.get('employee_id')
        face_encoding_json = request.POST.get('face_encoding')

        missing = []
        if not name:
            missing.append("name")
        if not employee_id:
            missing.append("employee_id")
        if not face_encoding_json:
            missing.append("face_encoding")

        if missing:
            return HttpResponse(
                f"❌ Missing required field(s): {', '.join(missing)}",
                status=400
            )

        try:
            face_encoding = base64.b64encode(pickle.dumps(json.loads(face_encoding_json))).decode()
            employee = Employee(name=name, employee_id=employee_id, face_encoding=face_encoding)
            employee.save()
            return HttpResponse("✅ Employee registered successfully!")
        except Exception as e:
            logger.error(f"Error in register_employee: {str(e)}")
            return HttpResponse(f"❌ Error saving employee: {str(e)}", status=500)

    return render(request, 'faceatendance/register.html')

