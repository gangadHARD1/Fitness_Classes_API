from django.test import TestCase, Client
from .models import FitnessClass, Instructor
from .models import Client  as FClient
from datetime import datetime,timedelta

# Create your tests here.
class FitnessStudioAppTests(TestCase):
    def setUp(self):
        # Create test data for FitnessClass  and Instructor
        i1 = Instructor.objects.create(name="John Doe", email="abc@xyz.com")
        i2 = Instructor.objects.create(name="Jane Smith", email="abc2@xyz.com")
        i3= Instructor.objects.create(name="Alice Johnson", email="abc3@xyz.com")
        time="2025-10-01T10:00:00"
        dtime=datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        fc1= FitnessClass.objects.create(
            name="Yoga",
            duration=timedelta(hours=1),
            time=dtime,
            capacity=10
        )
        fc1.instructor.set([i1])
        time="2025-10-01T10:00:00"
        dtime=datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        fc2=FitnessClass.objects.create(
            name="Zumba",
            duration=timedelta(hours=1),
            time=dtime,
            capacity=5
        )

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

    def test_instructor_count(self):
        
        # Test that the number of instructors is correct
        self.assertEqual(Instructor.objects.count(), 3)

    def test_fitness_class_count_and_validity(self): 
        # Test that the number of fitness classes is correct and classes are valid
        fc1=FitnessClass.objects.get(name="Yoga")
        self.assertEqual(FitnessClass.objects.count(), 3)
        self.assertEqual(fc1.is_valid(),True)
    
    def test_get_classes(self):
        # Test the classes endpoint
        client = Client()
        response = client.get('/fitness_studio/classes')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
    
    def test_get_class_with_timezone(self):
        client = Client()
        response = client.get('/fitness_studio/classes?timezone=America/New_York')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0]["time"],"2025-10-01T00:30:00-04:00")
    
    
    def test_book_class(self):
        # Test booking a class
        client = Client()
        response = client.post('/fitness_studio/book', {
            'class_id': 1,
            'client_name': 'Test User',
            'client_email': 'test@test.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Class booked successfully')
    
    


    def test_get_bookings(self):
        # Test retrieving bookings for a client
        client = Client()
        response = client.get('/fitness_studio/bookings?client_email=test1@test.com')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1) 
    
    def test_get_bookings_invalid_client(self):
        # Test retrieving bookings for a non-existent client
        client = Client()
        response = client.get('/fitness_studio/bookings?client_email=test2@test.com')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'Client not found')
    
    def test_get_bookings_no_bookings(self):
        # Test retrieving bookings for a client with no bookings
        client = Client()
        fitness_client= FClient.objects.create(name="No Bookings", email="nb@test.com")
        response = client.get(f'/fitness_studio/bookings?client_email={fitness_client.email}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    
    

    