from django.db import models
from zoneinfo import ZoneInfo

# Model for a fitness class session for the studio
class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    duration = models.DurationField()
    time=models.DateTimeField()
    capacity = models.PositiveIntegerField()
    instructor = models.ManyToManyField('Instructor',related_name="owned_classes")
    clients = models.ManyToManyField('Client', blank=True,related_name="booked_classes")

    def __str__(self):
        return self.name
    
    # Method to serialize the fitness class data, converting time to the specified timezone
    def serialize(self, time_zone=None):
        ist = ZoneInfo("Asia/Kolkata")
        ist_aware_time = self.time.replace(tzinfo=ist)  # Step 1: make it aware in IST

        if time_zone is None:
            local_time = ist_aware_time
        else:
            try:
                local_time = ist_aware_time.astimezone(ZoneInfo(time_zone))  
                print("hereeeeeee",local_time,ist_aware_time)
                      # Step 2: convert
            except Exception as e:
                print("here2222",e)
                local_time = ist_aware_time  # fallback to IST if invalid timezone

        return {
            "id": self.id,
            "name": self.name,
            "duration": str(self.duration),
            "time": local_time.isoformat(),
            "available_slot": self.capacity - self.clients.count(),
            "instructors": [instructor.name for instructor in self.instructor.all()],
        }
    #checks if the fitness class is valid for booking
    def is_valid(self):
        return (self.capacity > 0 and self.instructor.exists()) 

# Model for a client who can book fitness classes
class Client(models.Model):
    name= models.CharField(max_length=100)
    email = models.EmailField(unique=True)
   

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
# Model for an instructor who leads fitness classes
class Instructor(models.Model):
    name= models.CharField(max_length=100)
    email = models.EmailField(unique=True)
