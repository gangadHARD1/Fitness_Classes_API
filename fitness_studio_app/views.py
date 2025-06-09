from django.shortcuts import render
from django.http import JsonResponse
from .models import FitnessClass,Instructor,Client
from django.utils import timezone
from zoneinfo import ZoneInfo
import logging
from django.views.decorators.csrf import csrf_exempt

logger=logging.getLogger("view.logger")
# Endpoint to retrieve all fitness classes that are scheduled for the future
def classes(request):
    if request.method=="GET":
        logger.info('Received GET request for fitness classes.')

        # Get the current time in IST (Indian Standard Time)
        aware_time = timezone.now().astimezone(ZoneInfo("Asia/Kolkata"))  # Get the current time in IST
        time_now= aware_time.replace(tzinfo=None)  # Convert to naive datetime for comparison
        

        #fetch all fitness classes that are scheduled for the future
        classes=FitnessClass.objects.filter(time__gte=time_now)
        logger.debug('Retrieved %d fitness classes scheduled after %s', classes.count(), time_now)

        #serialize the classes to a list of dictionaries
        if request.GET.get("timezone"):
            timezone_str = request.GET.get("timezone")
            logger.debug('timezone given %s',timezone_str)
            classes_list = [fitness_class.serialize(timezone_str) for fitness_class in classes]
        else:
            logger.info('no explicit time zone given')
            classes_list = [fitness_class.serialize() for fitness_class in classes]
        return JsonResponse(classes_list, safe=False)
    else:
        logger.warning('Invalid request method: %s', request.method)
        return JsonResponse({"error": "Invalid request method"}, status=405)

# Endpoint to book a fitness class for a client  
@csrf_exempt  # Disable CSRF protection for this endpoint

def book_class(request):
    logger.info('Received request to book a fitness class.')

    if request.method=="POST":
        class_id= request.POST.get("class_id")
        client_name= request.POST.get("client_name")
        client_email= request.POST.get("client_email")

        logger.debug("client request parameters - class_id: %s, client_name: %s, client_email: %s", class_id, client_name, client_email)

        #input validation
        if class_id is None or client_name is None or client_email is None:
            logger.error("Missing required parameters")
            return JsonResponse({"error": "class_id, client_name, and client_email are required"}, status=400)
        
        try:
            fitness_class = FitnessClass.objects.get(id=class_id)
        except FitnessClass.DoesNotExist:
            logger.error("Missing fitness class with id %s", class_id)
            return JsonResponse({"error": "Fitness class not found"}, status=404)
        
        #check if the class is full
        if fitness_class.clients.count() >= fitness_class.capacity:
            logger.error("Booked class is full for class_id %s", class_id)
            return JsonResponse({"error": "Class is full"}, status=400)
        

        
        #check if the client already exists or create a new client
        client, created = Client.objects.get_or_create(email=client_email, defaults={"name": client_name})  
        
        if created==False:
            #checking if the client has another booking for the same time
            if client.booked_classes.filter(time=fitness_class.time).exists():
                logger.error("Client %s already booked for class at %s", client_email, fitness_class.time)
                return JsonResponse({"error": "Client already booked for this class"}, status=400)

        fitness_class.clients.add(client)
        return JsonResponse({"message": "Class booked successfully"}, status=200)
    else:
        logger.warning('Invalid request method: %s', request.method)
        return JsonResponse({"error": "Invalid request method"}, status=405)

# Endpoint to retrieve all bookings for a specific client    
def bookings(request):
        logger.info('Received request to retrieve bookings for a client.')

        # Check if the request method is GET
        if request.method == "GET":
            client_email = request.GET.get("client_email")
            if not client_email:
                logger.error("client_email parameter is missing")
                return JsonResponse({"error": "client_email is required"}, status=400)
            
            try:
                client = Client.objects.get(email=client_email)
            except Client.DoesNotExist:
                logger.error("Client with email %s not found", client_email)
                return JsonResponse({"error": "Client not found"}, status=404)
            
            bookings_list = [fitness_class.serialize() for fitness_class in client.booked_classes.all()]
            return JsonResponse(bookings_list, safe=False)
        logger.warning('Invalid request method: %s', request.method)
        return JsonResponse({"error": "Invalid request method"}, status=405)

        