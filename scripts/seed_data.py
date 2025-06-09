
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # adds project root to path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fitness_studio.settings")
django.setup()
from fitness_studio_app.models import FitnessClass, Instructor,Client as FClient
from datetime import datetime, timedelta

i1 = Instructor.objects.create(name="John Doe", email="abc@xyz.com")
i2 = Instructor.objects.create(name="Jane Smith", email="abc2@xyz.com")
i3= Instructor.objects.create(name="Alice Johnson", email="abc3@xyz.com")
time="2025-10-01T10:00:00"
dtime=datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
fc1= FitnessClass.objects.create(
            name="Yoga",
            duration=timedelta(hours=1),
            time=dtime,
            capacity=10)
fc1.instructor.set([i1])

time="2025-10-01T10:00:00"
dtime=datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
fc2=FitnessClass.objects.create(
name="Zumba",
            duration=timedelta(hours=1),
            time=dtime,
            capacity=5)

fc2.instructor.set([i2])

time="2025-10-01T10:00:00"
time=datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
fc3=FitnessClass.objects.create(
            name="HIIT",
            duration=timedelta(hours=1),
            time=time,
            capacity=8
        )
fc3.instructor.set([i3])
fc3.clients.set([FClient.objects.create(name="Test User", email="test1@test.com")])