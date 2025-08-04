from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='employee_photos/', blank=True, null=True)
    face_encoding = models.TextField(blank=True, null=True)  # base64 encoded string of face

    def __str__(self):
        return self.name

class AttendanceLog(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} - {self.time.strftime('%Y-%m-%d %H:%M:%S')}"
